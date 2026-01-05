import pandas as pd
import requests
import os
import xml.etree.ElementTree as ET
import json
import time
import logging
from datetime import datetime
from .config import YEARS, MONTHS, REQUEST_DELAY, MUNICIPALITY_DELAY, MAX_RETRIES, TIMEOUT_SECONDS, LOG_LEVEL

# Configure logging
log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DATA_DIR = "data/portaltp"
CONTROL_FILE = "data/control_portaltp.json"
LOGS_DIR = "logs"

# Enhanced endpoint configuration with metadata
ENDPOINTS = {
    "licitacoes": {
        "path": "transparencia.asmx/json_licitacoes",
        "params_obrigatorios": ["ano", "mes"],
        "params_opcionais": {"extra": "False", "situacao": ""},
        "iteracao": "mensal",
        "campos_obrigatorios": ["ano", "mes"],
        "campos_esperados": ["tipo_processo", "unidade_gestora", "modalidade", "licitacao", "objeto", "valor_homologado"]
    },
    "contratos": {
        "path": "transparencia.asmx/json_contratos",
        "params_obrigatorios": ["ano"],
        "params_opcionais": {},
        "iteracao": "anual",
        "campos_obrigatorios": ["ano"],
        "campos_esperados": ["unidade_gestora", "contrato", "nome_favorecido", "valor"]
    },
    "empenhos": {
        "path": "transparencia.asmx/json_empenhos",
        "params_obrigatorios": ["ano", "mes"],
        "params_opcionais": {},
        "iteracao": "mensal",
        "campos_obrigatorios": ["ano", "mes"],
        "campos_esperados": ["unidade_gestora", "empenho", "nome_favorecido", "valor"]
    },
    "liquidacoes": {
        "path": "transparencia.asmx/json_liquidacoes",
        "params_obrigatorios": ["ano", "mes"],
        "params_opcionais": {},
        "iteracao": "mensal",
        "campos_obrigatorios": ["ano", "mes"],
        "campos_esperados": ["unidade_gestora", "liquidacao", "nome_favorecido", "valor"]
    },
    "pagamentos": {
        "path": "transparencia.asmx/json_pagamentos",
        "params_obrigatorios": ["ano", "mes"],
        "params_opcionais": {},
        "iteracao": "mensal",
        "campos_obrigatorios": ["ano", "mes"],
        "campos_esperados": ["unidade_gestora", "pagamento", "nome_favorecido", "valor"]
    },
    "obras": {
        "path": "transparencia.asmx/json_obras",
        "params_obrigatorios": ["ano", "mes"],
        "params_opcionais": {},
        "iteracao": "mensal",
        "campos_obrigatorios": ["ano", "mes"],
        "campos_esperados": ["unidade_gestora", "obra", "nome_favorecido", "valor"]
    },
    "ordem_cronologica": {
        "path": "transparencia.asmx/json_ordem_cronologica_a_pagar",
        "params_obrigatorios": ["ano"],
        "params_opcionais": {},
        "iteracao": "anual",
        "campos_obrigatorios": ["ano_documento"],
        "campos_esperados": ["nro_liquidacao", "nom_pessoa", "vlr_liquidacao"]
    },
    "atas": {
        "path": "transparencia.asmx/json_atas",
        "params_obrigatorios": ["ano"],
        "params_opcionais": {},
        "iteracao": "anual",
        "campos_obrigatorios": ["ano"],
        "campos_esperados": ["unidade_gestora", "contrato", "nome_favorecido", "valor"]
    },
    "ordemcompras": {
        "path": "transparencia.asmx/json_ordemcompras",
        "params_obrigatorios": ["ano", "mes"],
        "params_opcionais": {},
        "iteracao": "mensal",
        "campos_obrigatorios": ["ano", "mes"],
        "campos_esperados": ["unidade_gestora", "ordem_compra", "nome_favorecido", "valor"]
    }
}

def get_prefeituras():
    """Reads the prefeituras.csv file and returns a pandas DataFrame."""
    return pd.read_csv("modules/portaltp/prefeituras.csv")

def ensure_directories():
    """Ensure required directories exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        os.makedirs(LOGS_DIR, exist_ok=True)
    except PermissionError:
        logger.warning(f"Cannot create logs directory: {LOGS_DIR}. Logs will only go to console.")
    os.makedirs(os.path.dirname(CONTROL_FILE), exist_ok=True)

def read_control_file():
    """Reads the control file and returns a dictionary."""
    if not os.path.exists(CONTROL_FILE):
        return {}
    try:
        with open(CONTROL_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        logger.warning("Control file corrupted or not found, starting fresh")
        return {}

def write_control_file(data):
    """Writes a dictionary to the control file."""
    ensure_directories()
    with open(CONTROL_FILE, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def normalizar_url_base(url):
    """Normalize base URL by ensuring it ends with /."""
    if not url.endswith('/'):
        url += '/'
    return url

def verificar_disponibilidade_endpoint(url_base, endpoint_config, params_teste):
    """
    Test if an endpoint is available before collecting historical data.
    Uses test parameters (current month/year) for validation.
    """
    url = f"{url_base}{endpoint_config['path']}"
    
    try:
        response = requests.get(url, params=params_teste, timeout=10)
        response.raise_for_status()
        
        # Check if response is valid JSON
        try:
            tree = ET.fromstring(response.content)
            json_string = tree.text
            dados = json.loads(json_string)
            # Even empty response [] indicates functional endpoint
            return True, "disponivel"
        except (json.JSONDecodeError, ET.ParseError):
            # Returned HTML or other format
            return False, "formato_invalido"
            
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return False, "nao_encontrado"
        return False, f"erro_http_{e.response.status_code}"
    except requests.exceptions.Timeout:
        return False, "timeout"
    except requests.exceptions.RequestException:
        return False, "erro_conexao"

def normalizar_registro(registro, schema_base, prefeitura_info, endpoint_nome):
    """
    Normalize a record to handle field variations between municipalities.
    """
    registro_normalizado = {}
    
    # Add metadata
    registro_normalizado.update({
        'prefeitura_id': prefeitura_info['id'],
        'municipio': prefeitura_info['municipio'],
        'prefeitura_nome': prefeitura_info['prefeitura'],
        'url_api': prefeitura_info['url'],
        'endpoint': endpoint_nome,
        'data_coleta': datetime.now().isoformat(),
        'status_code': 200
    })
    
    # Ensure mandatory fields exist (even if empty)
    for campo in schema_base['campos_obrigatorios']:
        registro_normalizado[campo] = registro.get(campo, None)
    
    # Add expected fields if they exist
    for campo in schema_base['campos_esperados']:
        registro_normalizado[campo] = registro.get(campo, None)
    
    # Include extra fields with prefix
    campos_conhecidos = set(schema_base['campos_obrigatorios'] + schema_base['campos_esperados'])
    for campo, valor in registro.items():
        if campo not in campos_conhecidos:
            registro_normalizado[f'extra_{campo}'] = valor
    
    return registro_normalizado

def converter_tipo_seguro(valor, tipo_esperado):
    """Safe type conversion with Brazilian format handling."""
    if valor is None or valor == '':
        return None
    
    try:
        if tipo_esperado == 'float':
            # Clean Brazilian formatting: 1.234,56 -> 1234.56
            if isinstance(valor, str):
                valor = valor.replace('.', '').replace(',', '.')
            return float(valor)
        elif tipo_esperado == 'date':
            # Try multiple date formats
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%dT%H:%M:%S']:
                try:
                    return datetime.strptime(valor, fmt)
                except:
                    continue
            return valor  # Keep as string if conversion fails
        elif tipo_esperado == 'int':
            return int(float(valor))  # float first to handle "123.0"
    except:
        return valor  # Return original value if conversion fails

def registrar_divergencia_schema(prefeitura_id, endpoint, campos_faltando, campos_extras):
    """Log schema divergences for audit purposes."""
    try:
        divergencia_file = os.path.join(LOGS_DIR, 'schema_divergencias.jsonl')
        ensure_directories()
        
        with open(divergencia_file, 'a', encoding='utf-8') as f:
            registro = {
                'timestamp': datetime.now().isoformat(),
                'prefeitura_id': prefeitura_id,
                'endpoint': endpoint,
                'campos_faltando': campos_faltando,
                'campos_extras': campos_extras
            }
            f.write(json.dumps(registro, ensure_ascii=False) + '\n')
    except (PermissionError, OSError):
        # If we can't write to file, just log to console
        logger.warning(f"Schema divergence - Prefeitura {prefeitura_id}, Endpoint {endpoint}: "
                      f"Missing: {campos_faltando}, Extra: {campos_extras}")

def get_data(url, endpoint_config, year, month=None, max_retries=MAX_RETRIES):
    """
    Fetches data from the API with enhanced error handling and retry logic.
    Returns tuple: (data, status_message)
    """
    # Build parameters
    params = {"ano": year}
    if month:
        params["mes"] = str(month)
    
    # Add optional parameters
    params.update(endpoint_config.get('params_opcionais', {}))
    
    url_completa = f"{url}{endpoint_config['path']}"
    
    for tentativa in range(max_retries):
        try:
            logger.debug(f"Tentativa {tentativa + 1}/{max_retries}: {url_completa} - {params}")
            
            response = requests.get(url_completa, params=params, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            
            # Handle XML response
            try:
                tree = ET.fromstring(response.content)
                json_string = tree.text
                data = json.loads(json_string)
                
                if isinstance(data, list):
                    return data, "sucesso" if len(data) > 0 else "sem_dados"
                else:
                    return None, "formato_inesperado"
                    
            except (ValueError, ET.ParseError) as e:
                logger.error(f"Erro ao processar resposta: {e}")
                return None, "erro_processamento"
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return None, "nao_encontrado"
            elif e.response.status_code == 500:
                if tentativa < max_retries - 1:
                    wait_time = 2 ** tentativa
                    logger.warning(f"Erro 500, tentando novamente em {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                return None, f"erro_http_{e.response.status_code}"
            else:
                return None, f"erro_http_{e.response.status_code}"
                
        except requests.exceptions.Timeout:
            if tentativa < max_retries - 1:
                logger.warning(f"Timeout, tentando novamente...")
                time.sleep(5)
                continue
            return None, "timeout"
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de requisição: {e}")
            return None, "erro_requisicao"
    
    return None, "max_tentativas_excedidas"


def save_to_parquet(data, municipio_name, endpoint_name):
    """Saves normalized data to Parquet files with proper handling."""
    if not data:
        return

    df = pd.DataFrame(data)
    
    ensure_directories()
    
    # Use municipality-specific filename
    parquet_filename = os.path.join(DATA_DIR, f"{municipio_name}_{endpoint_name}.parquet")
    
    if os.path.exists(parquet_filename):
        try:
            existing_df = pd.read_parquet(parquet_filename)
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df.to_parquet(parquet_filename, engine='pyarrow')
            logger.debug(f"Dados anexados ao arquivo existente: {parquet_filename}")
        except Exception as e:
            logger.error(f"Erro ao anexar dados: {e}")
            # Fallback: save with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = os.path.join(DATA_DIR, f"{municipio_name}_{endpoint_name}_{timestamp}.parquet")
            df.to_parquet(backup_filename, engine='pyarrow')
            logger.warning(f"Dados salvos em arquivo backup: {backup_filename}")
    else:
        df.to_parquet(parquet_filename, engine='pyarrow')
        logger.debug(f"Novo arquivo criado: {parquet_filename}")

def is_task_completed(control_data, municipio_name, endpoint_name, year, month=None):
    """Check if a specific task has been completed."""
    if municipio_name not in control_data:
        return False
    if endpoint_name not in control_data[municipio_name]:
        return False
    if str(year) not in control_data[municipio_name][endpoint_name]:
        return False
    
    if month is None:
        # Annual endpoint - check if year is marked as complete (0)
        return 0 in control_data[municipio_name][endpoint_name][str(year)]
    else:
        # Monthly endpoint - check if specific month is complete
        return month in control_data[municipio_name][endpoint_name][str(year)]

def mark_task_completed(control_data, municipio_name, endpoint_name, year, month=None):
    """Mark a specific task as completed in control data."""
    if municipio_name not in control_data:
        control_data[municipio_name] = {}
    if endpoint_name not in control_data[municipio_name]:
        control_data[municipio_name][endpoint_name] = {}
    if str(year) not in control_data[municipio_name][endpoint_name]:
        control_data[municipio_name][endpoint_name][str(year)] = []
    
    if month is None:
        # Annual endpoint
        if 0 not in control_data[municipio_name][endpoint_name][str(year)]:
            control_data[municipio_name][endpoint_name][str(year)].append(0)
    else:
        # Monthly endpoint
        if month not in control_data[municipio_name][endpoint_name][str(year)]:
            control_data[municipio_name][endpoint_name][str(year)].append(month)

def run():
    """
    Enhanced main function with two-phase approach:
    Phase 1: Check endpoint availability
    Phase 2: Collect historical data
    """
    logger.info("=== Iniciando coleta de dados PortalTP ===")
    
    ensure_directories()
    prefeituras = get_prefeituras()
    control_data = read_control_file()
    
    # Filter only PortalTP municipalities
    df_portaltp = prefeituras[prefeituras['empresa'] == 'portaltp'].copy()
    logger.info(f"Encontradas {len(df_portaltp)} prefeituras PortalTP")
    
    # PHASE 1: Check endpoint availability
    logger.info("=== FASE 1: Verificando disponibilidade de endpoints ===")
    endpoints_disponiveis = {}
    
    for idx, row in df_portaltp.iterrows():
        prefeitura_id = row['id']
        municipio = row['municipio']
        url_base = normalizar_url_base(row['url'])
        
        endpoints_disponiveis[prefeitura_id] = {}
        logger.info(f"Testando endpoints para {municipio}...")
        
        for endpoint_nome, endpoint_config in ENDPOINTS.items():
            # Test with recent data
            params_teste = ({'ano': '2025', 'mes': '12'} if endpoint_config['iteracao'] == 'mensal' 
                           else {'ano': '2025'})
            params_teste.update(endpoint_config.get('params_opcionais', {}))
            
            disponivel, motivo = verificar_disponibilidade_endpoint(url_base, endpoint_config, params_teste)
            endpoints_disponiveis[prefeitura_id][endpoint_nome] = disponivel
            
            status_msg = "✓ Disponível" if disponivel else f"✗ {motivo}"
            logger.info(f"  {endpoint_nome}: {status_msg}")
            
            time.sleep(REQUEST_DELAY)  # Rate limiting between endpoint tests
    
    # Save endpoint availability mapping
    try:
        availability_file = os.path.join(LOGS_DIR, 'endpoints_disponiveis.json')
        with open(availability_file, 'w', encoding='utf-8') as f:
            json.dump(endpoints_disponiveis, f, indent=2, ensure_ascii=False)
        logger.info(f"Mapeamento de disponibilidade salvo em: {availability_file}")
    except (PermissionError, OSError):
        logger.warning("Não foi possível salvar o mapeamento de disponibilidade em arquivo")
    
    # PHASE 2: Historical data collection
    logger.info("=== FASE 2: Coleta de dados históricos ===")
    
    total_municipios = len(df_portaltp)
    municipios_processados = 0
    
    for idx, row in df_portaltp.iterrows():
        municipios_processados += 1
        prefeitura_id = row['id']
        municipio = row['municipio']
        municipio_name = municipio.replace(' ', '_')
        url_base = normalizar_url_base(row['url'])
        
        logger.info(f"[{municipios_processados}/{total_municipios}] Processando: {row['prefeitura']}")
        
        prefeitura_info = {
            'id': prefeitura_id,
            'municipio': municipio,
            'prefeitura': row['prefeitura'],
            'url': url_base
        }
        
        for endpoint_nome, endpoint_config in ENDPOINTS.items():
            # Skip if endpoint not available
            if not endpoints_disponiveis[prefeitura_id].get(endpoint_nome, False):
                logger.info(f"  {endpoint_nome}: PULADO (indisponível)")
                continue
            
            logger.info(f"  Coletando {endpoint_nome}...")
            registros_coletados = 0
            registros_novos = 0
            
            # Generate parameter combinations
            if endpoint_config['iteracao'] == 'mensal':
                for year in YEARS:
                    for month in MONTHS:
                        # Check if already processed
                        if is_task_completed(control_data, municipio_name, endpoint_nome, year, month):
                            logger.debug(f"    {year}/{month:02d}: já processado")
                            continue
                        
                        data, status = get_data(url_base, endpoint_config, year, month)
                        
                        if status == "sucesso" and data:
                            # Normalize records
                            dados_normalizados = []
                            for registro in data:
                                reg_normalizado = normalizar_registro(
                                    registro, endpoint_config, prefeitura_info, endpoint_nome
                                )
                                dados_normalizados.append(reg_normalizado)
                            
                            # Check for schema divergences
                            if dados_normalizados:
                                primeiro_registro = data[0]
                                campos_esperados = set(endpoint_config['campos_obrigatorios'] + endpoint_config['campos_esperados'])
                                campos_presentes = set(primeiro_registro.keys())
                                
                                campos_faltando = list(campos_esperados - campos_presentes)
                                campos_extras = list(campos_presentes - campos_esperados)
                                
                                if campos_faltando or campos_extras:
                                    registrar_divergencia_schema(prefeitura_id, endpoint_nome, campos_faltando, campos_extras)
                            
                            # Save data
                            save_to_parquet(dados_normalizados, municipio_name, endpoint_nome)
                            registros_coletados += len(dados_normalizados)
                            registros_novos += len(dados_normalizados)
                            
                            # Mark as completed
                            mark_task_completed(control_data, municipio_name, endpoint_nome, year, month)
                            
                            logger.debug(f"    {year}/{month:02d}: {len(dados_normalizados)} registros")
                        
                        elif status == "sem_dados":
                            # Mark as completed even with no data
                            mark_task_completed(control_data, municipio_name, endpoint_nome, year, month)
                            logger.debug(f"    {year}/{month:02d}: sem dados")
                        
                        else:
                            logger.warning(f"    {year}/{month:02d}: {status}")
                        
                        time.sleep(REQUEST_DELAY)  # Rate limiting between requests
            
            elif endpoint_config['iteracao'] == 'anual':
                for year in YEARS:
                    # Check if already processed
                    if is_task_completed(control_data, municipio_name, endpoint_nome, year):
                        logger.debug(f"    {year}: já processado")
                        continue
                    
                    data, status = get_data(url_base, endpoint_config, year)
                    
                    if status == "sucesso" and data:
                        # Normalize records
                        dados_normalizados = []
                        for registro in data:
                            reg_normalizado = normalizar_registro(
                                registro, endpoint_config, prefeitura_info, endpoint_nome
                            )
                            dados_normalizados.append(reg_normalizado)
                        
                        # Save data
                        save_to_parquet(dados_normalizados, municipio_name, endpoint_nome)
                        registros_coletados += len(dados_normalizados)
                        registros_novos += len(dados_normalizados)
                        
                        # Mark as completed
                        mark_task_completed(control_data, municipio_name, endpoint_nome, year)
                        
                        logger.debug(f"    {year}: {len(dados_normalizados)} registros")
                    
                    elif status == "sem_dados":
                        # Mark as completed even with no data
                        mark_task_completed(control_data, municipio_name, endpoint_nome, year)
                        logger.debug(f"    {year}: sem dados")
                    
                    else:
                        logger.warning(f"    {year}: {status}")
                    
                    time.sleep(REQUEST_DELAY)  # Rate limiting between requests
            
            if registros_novos > 0:
                logger.info(f"    Total coletado: {registros_novos} novos registros")
            else:
                logger.info(f"    Nenhum registro novo coletado")
        
        # Save control file after each municipality
        write_control_file(control_data)
        
        logger.info(f"Concluído: {row['prefeitura']}")
        
        # Delay between municipalities to avoid overloading servers
        if municipios_processados < total_municipios:
            logger.debug(f"Aguardando {MUNICIPALITY_DELAY} segundos antes da próxima prefeitura...")
            time.sleep(MUNICIPALITY_DELAY)
    
    logger.info("=== Coleta finalizada com sucesso ===")
    logger.info(f"Arquivo de controle salvo em: {CONTROL_FILE}")
    logger.info(f"Dados salvos em: {DATA_DIR}")
    logger.info(f"Logs disponíveis em: {LOGS_DIR}")

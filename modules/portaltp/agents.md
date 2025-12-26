# Guia para Agentes: Automação de Coleta de Dados das APIs PortalTP

Este documento fornece todas as informações necessárias para criar uma ferramenta de automação que coleta dados dos portais de transparência das prefeituras do Espírito Santo que utilizam a plataforma PortalTP.

## Objetivo

Criar uma ferramenta que:
1. Identifique todas as prefeituras que usam PortalTP
2. Itere pelos métodos/endpoints disponíveis na API
3. Faça requisições para cada combinação prefeitura + endpoint
4. Salve os dados JSON retornados em formato tabular (CSV, Parquet, ou banco de dados)

---

## 1. Estrutura dos Dados de Entrada

### 1.1 Arquivo `prefeituras.csv`

Localização: `portal_lists/prefeituras.csv`

**Colunas relevantes:**
- `id`: Identificador único da prefeitura
- `prefeitura`: Nome oficial completo
- `municipio`: Nome do município (normalizado, lowercase)
- `url`: URL base da API (ex: `https://afonsoclaudio-es.portaltp.com.br/api/`)
- `empresa`: Fornecedor da plataforma (filtrar por `"portaltp"`)
- `unidadegestora`: ID da unidade gestora (pode estar vazio, necessário para algumas APIs como Tectrilha)

**Filtro necessário:**
```python
df_portaltp = df[df['empresa'] == 'portaltp']
```

Isso resultará em aproximadamente 60+ prefeituras que usam PortalTP.

### 1.2 Arquivo `method_list.txt`

Localização: `portal_lists/api_metodos/method_list.txt`

Contém a documentação completa dos endpoints disponíveis, incluindo:
- Descrição de cada método
- Parâmetros obrigatórios e opcionais
- Estrutura de retorno (campos)
- Exemplos de URLs

---

## 2. Endpoints Disponíveis na API PortalTP

### 2.1 Categoria: Compras

#### **Licitações**
- **Endpoint:** `/transparencia.asmx/json_licitacoes`
- **Parâmetros obrigatórios:**
  - `ano` (texto): Ano do exercício (ex: "2025")
  - `mes` (texto): Mês do exercício (ex: "12")
- **Parâmetros opcionais:**
  - `extra` (boolean): Mostrar vencedores (default: False)
  - `situacao` (texto): Filtrar por situação (default: ".")
- **Exemplo de URL:**
  ```
  https://afonsoclaudio-es.portaltp.com.br/api/transparencia.asmx/json_licitacoes?ano=2025&mes=12&extra=False&situacao=.
  ```
- **Campos retornados:** ano, mes, tipo_processo, unidade_gestora, modalidade, licitacao, processo, objeto, abertura, homologacao, conclusao, situacao, valor_homologado

#### **Contratos e Aditivos**
- **Endpoint:** `/transparencia.asmx/json_contratos`
- **Parâmetros obrigatórios:**
  - `ano` (texto): Ano do exercício
- **Exemplo de URL:**
  ```
  https://afonsoclaudio-es.portaltp.com.br/api/transparencia.asmx/json_contratos?ano=2025
  ```
- **Campos retornados:** ano, unidade_gestora, contrato, ano_contrato, processo, assinatura, documento_favorecido, nome_favorecido, categoria, objeto, situacao, valor

#### **Termos de Compromisso/Atas**
- **Endpoint:** `/transparencia.asmx/json_atas`
- **Parâmetros obrigatórios:**
  - `ano` (texto): Ano do exercício
- **Exemplo de URL:**
  ```
  https://afonsoclaudio-es.portaltp.com.br/api/transparencia.asmx/json_atas?ano=2025
  ```
- **Campos retornados:** ano, unidade_gestora, contrato, processo, assinatura, documento_favorecido, nome_favorecido, categoria, objeto, situacao, valor

#### **Ordem de Compras**
- **Endpoint:** `/transparencia.asmx/json_ordemcompras`
- **Parâmetros obrigatórios:**
  - `ano` (texto): Ano do exercício
  - `mes` (texto): Mês do exercício
- **Exemplo de URL:**
  ```
  https://afonsoclaudio-es.portaltp.com.br/api/transparencia.asmx/json_ordemcompras?ano=2025&mes=12
  ```
- **Campos retornados:** ano, mes, chave, unidade_gestora, ordem_compra, secretaria, data_ordem, documento_favorecido, nome_favorecido, valor

### 2.2 Categoria: Despesas

#### **Empenhos e Favorecidos**
- **Endpoint:** `/transparencia.asmx/json_empenhos`
- **Parâmetros obrigatórios:**
  - `ano` (texto): Ano do exercício
  - `mes` (texto): Mês do exercício
- **Exemplo de URL:**
  ```
  https://afonsoclaudio-es.portaltp.com.br/api/transparencia.asmx/json_empenhos?ano=2025&mes=12
  ```
- **Campos retornados:** ano, mes, unidade_gestora, data, especie, empenho, tipo_empenho, elemento_despesa, subtitulo, funcao, subfuncao, programa, fonte_recurso, grupo_despesa, documento_favorecido, nome_favorecido, valor

#### **Liquidações e Favorecidos**
- **Endpoint:** `/transparencia.asmx/json_liquidacoes`
- **Parâmetros obrigatórios:**
  - `ano` (texto): Ano do exercício
  - `mes` (texto): Mês do exercício
- **Exemplo de URL:**
  ```
  https://afonsoclaudio-es.portaltp.com.br/api/transparencia.asmx/json_liquidacoes?ano=2025&mes=12
  ```
- **Campos retornados:** ano, mes, unidade_gestora, data, especie, empenho, liquidacao, tipo_liquidacao, elemento_despesa, subtitulo, funcao, subfuncao, programa, fonte_recurso, grupo_despesa, documento_favorecido, nome_favorecido, valor

#### **Pagamentos e Favorecidos**
- **Endpoint:** `/transparencia.asmx/json_pagamentos`
- **Parâmetros obrigatórios:**
  - `ano` (texto): Ano do exercício
  - `mes` (texto): Mês do exercício
- **Exemplo de URL:**
  ```
  https://afonsoclaudio-es.portaltp.com.br/api/transparencia.asmx/json_pagamentos?ano=2025&mes=12
  ```
- **Nota:** A documentação indica que este endpoint pode retornar lista vazia

#### **Ordem Cronológica dos Pagamentos**
- **Endpoint:** `/transparencia.asmx/json_ordem_cronologica_a_pagar`
- **Parâmetros obrigatórios:**
  - `ano_documento` (texto): Ano do exercício (nota: parâmetro diferente!)
- **Exemplo de URL:**
  ```
  https://afonsoclaudio-es.portaltp.com.br/api/transparencia.asmx/json_ordem_cronologica_a_pagar?ano=2025
  ```
- **Campos retornados:** ano_documento, nom_contrato_tipo, nom_fonte_recurso_tce, nro_ordem_fila, nro_liquidacao, dat_liquidacao, dat_liquidacao_vencimento, nro_empenho, nro_pagamento_ordem, nom_pessoa, sld_liquidacao_ordem_final, vlr_liquidacao, nda_liquidacao, nda_licitacao, motivo_quebra_ordem_cronologica

#### **Despesas com Obras**
- **Endpoint:** `/transparencia.asmx/json_obras`
- **Parâmetros obrigatórios:**
  - `ano` (texto): Ano do exercício
  - `mes` (texto): Mês do exercício
- **Exemplo de URL:**
  ```
  https://afonsoclaudio-es.portaltp.com.br/api/transparencia.asmx/json_obras?ano=2025&mes=12
  ```
- **Campos retornados:** ano, mes, unidade_gestora, data, especie, pagamento, tipo_pagamento, elemento_despesa, subtitulo, documento_favorecido, nome_favorecido, valor

---

## 3. Estrutura da Ferramenta de Automação

### 3.1 Fluxo Principal

```
1. Carregar prefeituras.csv
2. Filtrar empresa == "portaltp"
3. Para cada prefeitura:
   a. Para cada endpoint:
      i. Para cada combinação de parâmetros (ano, mês):
         - Construir URL completa
         - Fazer requisição HTTP GET
         - Validar resposta
         - Processar JSON
         - Adicionar metadados (prefeitura_id, municipio, data_coleta)
         - Salvar em tabela/arquivo
      ii. Implementar retry logic e error handling
   b. Log do progresso
```

### 3.2 Construção de URLs

**Padrão geral:**
```
{url_base}{endpoint}?{parametros}
```

**Exemplo:**
```python
url_base = "https://afonsoclaudio-es.portaltp.com.br/api/"
endpoint = "transparencia.asmx/json_licitacoes"
params = {"ano": "2025", "mes": "12", "extra": "False", "situacao": "."}

# URL final:
# https://afonsoclaudio-es.portaltp.com.br/api/transparencia.asmx/json_licitacoes?ano=2025&mes=12&extra=False&situacao=.
```

**Importante:** Algumas URLs já incluem `/api/` no final, outras não. Normalizar antes de concatenar.

### 3.3 Definição de Endpoints

Criar uma estrutura de configuração para cada endpoint:

```python
ENDPOINTS = {
    "licitacoes": {
        "path": "transparencia.asmx/json_licitacoes",
        "params": {
            "obrigatorios": ["ano", "mes"],
            "opcionais": {
                "extra": "False",
                "situacao": "."
            }
        },
        "iteracao": "mensal"  # precisa iterar ano e mês
    },
    "contratos": {
        "path": "transparencia.asmx/json_contratos",
        "params": {
            "obrigatorios": ["ano"],
            "opcionais": {}
        },
        "iteracao": "anual"  # apenas ano
    },
    # ... outros endpoints
}
```

### 3.4 Estratégia de Iteração Temporal

Para maximizar a coleta de dados históricos:

**Endpoints mensais** (licitacoes, empenhos, liquidacoes, pagamentos, ordemcompras, obras):
- Iterar de Janeiro/2015 até Dezembro/2025 (ou ano atual)
- Total: ~132 requisições por endpoint por prefeitura

**Endpoints anuais** (contratos, atas):
- Iterar de 2015 até 2025
- Total: ~11 requisições por endpoint por prefeitura

**Cálculo estimado:**
- 60 prefeituras PortalTP
- 6 endpoints mensais × 132 meses = 792 requisições/prefeitura
- 2 endpoints anuais × 11 anos = 22 requisições/prefeitura
- Total: ~48.840 requisições

---

## 4. Processamento e Armazenamento

### 4.1 Adição de Metadados

Cada registro coletado deve incluir:
```python
{
    "prefeitura_id": 1,
    "municipio": "afonso claudio",
    "prefeitura_nome": "Prefeitura Municipal de Afonso Cláudio",
    "url_api": "https://afonsoclaudio-es.portaltp.com.br/api/",
    "endpoint": "json_licitacoes",
    "data_coleta": "2025-12-26T10:30:00",
    "status_code": 200,
    # ... dados originais do JSON ...
}
```

### 4.2 Estrutura de Armazenamento

**Opção 1: Arquivos CSV/Parquet por endpoint**
```
data/
  licitacoes/
    afonso_claudio_2025_12.parquet
    aguia_branca_2025_12.parquet
  contratos/
    afonso_claudio_2025.parquet
```

**Opção 2: Banco de dados relacional**
```sql
CREATE TABLE licitacoes (
    id SERIAL PRIMARY KEY,
    prefeitura_id INT,
    municipio VARCHAR(100),
    ano VARCHAR(4),
    mes VARCHAR(2),
    tipo_processo TEXT,
    -- ... outros campos ...
    data_coleta TIMESTAMP,
    FOREIGN KEY (prefeitura_id) REFERENCES prefeituras(id)
);
```

**Opção 3: Arquivo consolidado por endpoint**
```
data/
  licitacoes_completo.parquet
  contratos_completo.parquet
  empenhos_completo.parquet
```

### 4.3 Normalização de Dados

Ao processar JSON para tabela:

1. **Achatamento de estruturas aninhadas** (se houver)
2. **Conversão de tipos:**
   - Datas: converter strings para datetime
   - Valores numéricos: converter para float/decimal
   - Documentos: manter como string, mas validar formato CPF/CNPJ
3. **Tratamento de valores ausentes:**
   - `null` → `None` ou `NaN`
   - Strings vazias → considerar como ausente
4. **Padronização de nomes:**
   - Campos: snake_case, lowercase
   - Valores categóricos: normalizar capitalização

---

## 5. Tratamento de Erros e Boas Práticas

### 5.1 HTTP Status Codes

- **200 OK:** Sucesso, processar JSON
- **404 Not Found:** Endpoint pode não estar disponível para essa prefeitura/período
- **500 Internal Server Error:** Erro no servidor, tentar novamente após delay
- **Timeout:** Aumentar timeout ou skip após X tentativas

### 5.2 Respostas Vazias

Muitas requisições podem retornar `[]` (lista vazia):
- Não há dados para aquele período
- Endpoint não implementado
- Dados ainda não publicados

**Ação:** Registrar em log, marcar como "sem dados", não considerar erro.

### 5.3 Divergências de Schema entre Prefeituras

**IMPORTANTE:** Nem todas as prefeituras PortalTP retornam os mesmos campos, mesmo usando o mesmo endpoint.

**Problemas comuns:**

1. **Campos ausentes:** Algumas prefeituras podem não retornar todos os campos documentados
2. **Campos extras:** Algumas podem incluir campos adicionais não documentados
3. **Nomes diferentes:** Pequenas variações nos nomes dos campos (ex: `valor_homologado` vs `valor_homologacao`)
4. **Tipos diferentes:** Campo que é string em uma prefeitura pode ser numérico em outra
5. **Estruturas aninhadas:** Algumas podem retornar objetos aninhados onde outras retornam strings

**Estratégias de tratamento:**

```python
# 1. Schema flexível com campos opcionais
ESQUEMA_BASE_LICITACOES = {
    'obrigatorios': ['ano', 'mes'],  # Campos que DEVEM existir
    'esperados': ['tipo_processo', 'unidade_gestora', 'modalidade', 
                  'licitacao', 'objeto', 'valor_homologado'],
    'opcionais': []  # Aceitar qualquer campo adicional
}

# 2. Normalização de dados
def normalizar_registro(registro, schema_base):
    registro_normalizado = {}
    
    # Garantir campos obrigatórios existem (mesmo que vazios)
    for campo in schema_base['obrigatorios']:
        registro_normalizado[campo] = registro.get(campo, None)
    
    # Adicionar campos esperados se existirem
    for campo in schema_base['esperados']:
        registro_normalizado[campo] = registro.get(campo, None)
    
    # Incluir campos extras com prefixo
    campos_conhecidos = set(schema_base['obrigatorios'] + schema_base['esperados'])
    for campo, valor in registro.items():
        if campo not in campos_conhecidos:
            registro_normalizado[f'extra_{campo}'] = valor
    
    return registro_normalizado

# 3. Validação de tipos com conversão segura
def converter_tipo_seguro(valor, tipo_esperado):
    if valor is None or valor == '':
        return None
    
    try:
        if tipo_esperado == 'float':
            # Limpar formatação brasileira: 1.234,56 -> 1234.56
            if isinstance(valor, str):
                valor = valor.replace('.', '').replace(',', '.')
            return float(valor)
        elif tipo_esperado == 'date':
            # Tentar múltiplos formatos de data
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%dT%H:%M:%S']:
                try:
                    return datetime.strptime(valor, fmt)
                except:
                    continue
            return valor  # Manter como string se não conseguir converter
        elif tipo_esperado == 'int':
            return int(float(valor))  # float primeiro para lidar com "123.0"
    except:
        return valor  # Retornar valor original se conversão falhar

# 4. Registro de divergências para auditoria
def registrar_divergencia_schema(prefeitura_id, endpoint, campos_faltando, campos_extras):
    with open('logs/schema_divergencias.jsonl', 'a') as f:
        registro = {
            'timestamp': datetime.now().isoformat(),
            'prefeitura_id': prefeitura_id,
            'endpoint': endpoint,
            'campos_faltando': campos_faltando,
            'campos_extras': campos_extras
        }
        f.write(json.dumps(registro) + '\n')
```

### 5.4 Endpoints Indisponíveis

Nem todas as prefeituras implementam todos os endpoints PortalTP.

**Sinais de endpoint não disponível:**
- Status 404 (Not Found)
- Status 500 com mensagem de erro específica
- Retorno de HTML de erro em vez de JSON
- Timeout consistente (endpoint pode não existir)

**Estratégia de detecção:**

```python
def verificar_disponibilidade_endpoint(url_base, endpoint, params_teste):
    """
    Testa se um endpoint está disponível antes de coletar dados históricos.
    Usa parâmetros de teste (mês/ano atual) para validar.
    """
    url = f"{url_base}{endpoint['path']}"
    
    try:
        response = requests.get(url, params=params_teste, timeout=10)
        
        # Verificar se resposta é JSON válido
        try:
            dados = response.json()
            # Mesmo resposta vazia [] indica endpoint funcional
            return True, "disponivel"
        except json.JSONDecodeError:
            # Retornou HTML ou outro formato
            return False, "formato_invalido"
            
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return False, "nao_encontrado"
        return False, f"erro_http_{e.response.status_code}"
    except requests.exceptions.Timeout:
        return False, "timeout"
    except requests.exceptions.RequestException as e:
        return False, f"erro_conexao"

# Uso:
ENDPOINTS_DISPONIVEIS = {}

for idx, row in df_portaltp.iterrows():
    prefeitura_id = row['id']
    ENDPOINTS_DISPONIVEIS[prefeitura_id] = {}
    
    for endpoint_nome, endpoint_config in ENDPOINTS.items():
        # Testar com dados recentes
        params_teste = {'ano': '2025', 'mes': '12'} if endpoint_config['iteracao'] == 'mensal' else {'ano': '2025'}
        
        disponivel, motivo = verificar_disponibilidade_endpoint(
            row['url'], endpoint_config, params_teste
        )
        
        ENDPOINTS_DISPONIVEIS[prefeitura_id][endpoint_nome] = {
            'disponivel': disponivel,
            'motivo': motivo
        }
        
        if not disponivel:
            logger.warning(f"{row['municipio']} - {endpoint_nome}: {motivo}")

# Salvar mapeamento para referência
import json
with open('logs/endpoints_disponiveis.json', 'w') as f:
    json.dump(ENDPOINTS_DISPONIVEIS, f, indent=2)
```

**Ação recomendada:**
- Fazer varredura inicial de disponibilidade antes da coleta completa
- Salvar mapeamento de quais endpoints cada prefeitura suporta
- Skip automático de endpoints indisponíveis durante coleta
- Revisar periodicamente (trimestral) pois endpoints podem ser adicionados

### 5.5 Rate Limiting

Para evitar sobrecarga nos servidores:
- **Delay entre requisições:** 1-2 segundos
- **Delay entre prefeituras:** 5-10 segundos
- **Horário de coleta:** Preferir horários de menor tráfego (madrugada, fins de semana)
- **Paralelização:** Limitar threads/workers (máximo 3-5 simultâneos)

### 5.6 Retry Logic

```python
def fazer_requisicao(url, max_retries=3):
    for tentativa in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None  # Sem dados
            else:
                time.sleep(2 ** tentativa)  # Exponential backoff
        except requests.Timeout:
            if tentativa == max_retries - 1:
                raise
            time.sleep(5)
    return None
```

### 5.7 Logging Detalhado

Registrar:
- Início e fim de cada prefeitura
- Cada requisição (URL, status, tempo de resposta)
- Erros e exceções
- Total de registros coletados por endpoint
- Estatísticas finais

Exemplo de log:
```
[2025-12-26 10:30:15] INFO: Iniciando coleta para Afonso Cláudio
[2025-12-26 10:30:16] INFO: GET json_licitacoes?ano=2025&mes=12 - 200 OK - 245 registros - 1.2s
[2025-12-26 10:30:18] WARNING: GET json_pagamentos?ano=2025&mes=12 - 200 OK - 0 registros
[2025-12-26 10:30:20] ERROR: GET json_contratos?ano=2024 - 500 Server Error - Retry 1/3
```

---

## 6. Validação de Dados

### 6.1 Checks Pós-Coleta

Para cada endpoint coletado:
1. **Completude:** Verificar se todos os anos/meses esperados foram coletados
2. **Consistência:** Valores numéricos não negativos (exceto saldos)
3. **Duplicatas:** Identificar e remover registros duplicados
4. **Campos obrigatórios:** Verificar se campos-chave não estão vazios

### 6.2 Validações Específicas

- **CPF/CNPJ:** Validar formato e dígitos verificadores
- **Datas:** Verificar se estão dentro do período esperado (não futuros)
- **Valores:** Verificar se são razoáveis (não tem valores absurdamente altos sem justificativa)

### 6.3 Análise de Schemas por Prefeitura

Após coleta inicial, analisar divergências:

```python
def analisar_schemas_coletados(df):
    """
    Analisa os schemas reais retornados por cada prefeitura/endpoint.
    """
    analise = {}
    
    for endpoint in df['endpoint'].unique():
        df_endpoint = df[df['endpoint'] == endpoint]
        analise[endpoint] = {}
        
        for prefeitura in df_endpoint['prefeitura_id'].unique():
            df_pref = df_endpoint[df_endpoint['prefeitura_id'] == prefeitura]
            
            # Identificar colunas presentes
            colunas = set(df_pref.columns) - {'prefeitura_id', 'municipio', 
                                               'endpoint', 'data_coleta'}
            
            # Analisar preenchimento
            preenchimento = {}
            for col in colunas:
                nao_nulos = df_pref[col].notna().sum()
                total = len(df_pref)
                preenchimento[col] = (nao_nulos / total) * 100
            
            analise[endpoint][prefeitura] = {
                'total_registros': len(df_pref),
                'colunas': list(colunas),
                'preenchimento': preenchimento
            }
    
    return analise

# Gerar relatório de compatibilidade
def gerar_relatorio_compatibilidade(analise):
    """
    Identifica campos que são comuns vs específicos de algumas prefeituras.
    """
    for endpoint, prefeituras in analise.items():
        print(f"\n=== {endpoint} ===")
        
        # Coletar todos os campos únicos
        todos_campos = set()
        for pref_id, dados in prefeituras.items():
            todos_campos.update(dados['colunas'])
        
        # Identificar campos presentes em todas vs algumas prefeituras
        campos_universais = set(todos_campos)
        for pref_id, dados in prefeituras.items():
            campos_universais &= set(dados['colunas'])
        
        campos_parciais = todos_campos - campos_universais
        
        print(f"Campos universais ({len(campos_universais)}): {sorted(campos_universais)}")
        print(f"Campos parciais ({len(campos_parciais)}): {sorted(campos_parciais)}")
        
        # Mostrar distribuição dos campos parciais
        for campo in sorted(campos_parciais):
            prefeituras_com_campo = []
            for pref_id, dados in prefeituras.items():
                if campo in dados['colunas']:
                    prefeituras_com_campo.append(pref_id)
            print(f"  - {campo}: presente em {len(prefeituras_com_campo)}/{len(prefeituras)} prefeituras")
```

---

## 7. Exemplo de Código Python (Pseudocódigo)

```python
import pandas as pd
import requests
import time
from datetime import datetime
import logging
import json

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar prefeituras
df_prefeituras = pd.read_csv('portal_lists/prefeituras.csv', encoding='utf-8')
df_portaltp = df_prefeituras[df_prefeituras['empresa'] == 'portaltp']

# Definir endpoints com schemas esperados
ENDPOINTS = {
    'licitacoes': {
        'path': 'transparencia.asmx/json_licitacoes',
        'params_obrigatorios': ['ano', 'mes'],
        'iteracao': 'mensal',
        'campos_obrigatorios': ['ano', 'mes'],
        'campos_esperados': ['tipo_processo', 'unidade_gestora', 'modalidade', 
                            'licitacao', 'objeto', 'valor_homologado']
    },
    'contratos': {
        'path': 'transparencia.asmx/json_contratos',
        'params_obrigatorios': ['ano'],
        'iteracao': 'anual',
        'campos_obrigatorios': ['ano'],
        'campos_esperados': ['unidade_gestora', 'contrato', 'nome_favorecido', 'valor']
    },
    # ... outros endpoints
}

# Função para normalizar URL base
def normalizar_url_base(url):
    if not url.endswith('/'):
        url += '/'
    return url

# Função para fazer requisição com validação de schema
def coletar_dados(url_base, endpoint_config, params):
    url = f"{url_base}{endpoint_config['path']}"
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        # Validar que é JSON
        try:
            dados = response.json()
        except json.JSONDecodeError:
            logger.error(f"Resposta não é JSON válido: {url}")
            return None, "formato_invalido"
        
        # Se retornou lista vazia, é OK (sem dados)
        if isinstance(dados, list) and len(dados) == 0:
            return [], "sem_dados"
        
        # Se retornou dados, validar schema básico
        if isinstance(dados, list) and len(dados) > 0:
            # Verificar campos obrigatórios no primeiro registro
            primeiro = dados[0]
            campos_faltando = []
            for campo in endpoint_config['campos_obrigatorios']:
                if campo not in primeiro:
                    campos_faltando.append(campo)
            
            if campos_faltando:
                logger.warning(f"Campos obrigatórios ausentes: {campos_faltando}")
            
            return dados, "sucesso"
        
        return None, "formato_inesperado"
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao coletar {url}: {e}")
        return None, "erro_requisicao"

# FASE 1: Verificar disponibilidade de endpoints
logger.info("=== FASE 1: Verificando disponibilidade de endpoints ===")
endpoints_disponiveis = {}

for idx, row in df_portaltp.iterrows():
    prefeitura_id = row['id']
    endpoints_disponiveis[prefeitura_id] = {}
    
    for endpoint_nome, endpoint_config in ENDPOINTS.items():
        params_teste = ({'ano': '2025', 'mes': '12'} if endpoint_config['iteracao'] == 'mensal' 
                       else {'ano': '2025'})
        
        dados, status = coletar_dados(row['url'], endpoint_config, params_teste)
        disponivel = status in ['sucesso', 'sem_dados']
        
        endpoints_disponiveis[prefeitura_id][endpoint_nome] = disponivel
        logger.info(f"{row['municipio']} - {endpoint_nome}: {status}")
        time.sleep(1)

# Salvar mapeamento
with open('logs/endpoints_disponiveis.json', 'w') as f:
    json.dump(endpoints_disponiveis, f, indent=2)

# FASE 2: Coleta completa (apenas endpoints disponíveis)
logger.info("=== FASE 2: Coleta de dados históricos ===")

for idx, row in df_portaltp.iterrows():
    logger.info(f"Iniciando coleta: {row['prefeitura']}")
    
    url_base = normalizar_url_base(row['url'])
    prefeitura_id = row['id']
    
    for endpoint_nome, endpoint_config in ENDPOINTS.items():
        # Skip se endpoint não disponível
        if not endpoints_disponiveis[prefeitura_id].get(endpoint_nome, False):
            logger.info(f"  {endpoint_nome}: SKIPPED (indisponível)")
            continue
        
        logger.info(f"  Endpoint: {endpoint_nome}")
        registros_coletados = 0
        
        # Gerar combinações de parâmetros
        if endpoint_config['iteracao'] == 'mensal':
            for ano in range(2015, 2026):
                for mes in range(1, 13):
                    params = {'ano': str(ano), 'mes': str(mes).zfill(2)}
                    dados, status = coletar_dados(url_base, endpoint_config, params)
                    
                    if dados and len(dados) > 0:
                        # Normalizar registros para lidar com divergências
                        dados_normalizados = []
                        for registro in dados:
                            reg_normalizado = registro.copy()
                            reg_normalizado['prefeitura_id'] = row['id']
                            reg_normalizado['municipio'] = row['municipio']
                            reg_normalizado['endpoint'] = endpoint_nome
                            reg_normalizado['data_coleta'] = datetime.now().isoformat()
                            dados_normalizados.append(reg_normalizado)
                        
                        # Salvar
                        df_temp = pd.DataFrame(dados_normalizados)
                        registros_coletados += len(df_temp)
                        # ... salvar em arquivo/BD ...
                    
                    time.sleep(1)  # Rate limiting
        
        elif endpoint_config['iteracao'] == 'anual':
            for ano in range(2015, 2026):
                params = {'ano': str(ano)}
                dados, status = coletar_dados(url_base, endpoint_config, params)
                
                if dados and len(dados) > 0:
                    # Mesma normalização...
                    registros_coletados += len(dados)
                
                time.sleep(1)
        
        logger.info(f"    Total coletado: {registros_coletados} registros")
    
    logger.info(f"Concluído: {row['prefeitura']}")
    time.sleep(5)  # Delay entre prefeituras
```

---

## 8. Considerações Finais

### 8.1 Qualidade dos Dados

- Nem todas as prefeituras publicam dados regularmente
- Algumas podem ter períodos com dados ausentes
- A qualidade e completude variam entre municípios

### 8.2 Aspectos Legais

- Os dados são públicos (Lei de Acesso à Informação)
- Respeitar os Termos de Uso dos portais
- Não fazer scraping agressivo que possa prejudicar o serviço

### 8.3 Manutenção

- APIs podem mudar ao longo do tempo
- Novos campos podem ser adicionados
- Endpoints podem ser descontinuados
- Implementar versionamento dos schemas

### 8.4 Performance

- Para coleta completa, estimar 8-12 horas de execução
- Considerar execução em background/servidor
- Implementar checkpoint/resume para retomar coletas interrompidas

### 8.5 Próximos Passos

Após criar a ferramenta de coleta:
1. Análise exploratória dos dados coletados
2. Identificação de padrões e anomalias
3. Criação de dashboards e visualizações
4. Análises comparativas entre municípios
5. Detecção de inconsistências ou possíveis irregularidades

---

## 9. Checklist para o Agente

Ao construir a ferramenta, garantir:

**Básico:**
- [ ] Leitura correta do CSV com encoding UTF-8
- [ ] Filtro correto por empresa = "portaltp"
- [ ] Normalização das URLs base (remover/adicionar barra final)
- [ ] Implementação de todos os endpoints documentados
- [ ] Iteração correta de períodos (mensal vs anual)

**Tratamento de divergências:**
- [ ] Schema flexível que aceita campos variáveis
- [ ] Validação de disponibilidade de endpoints antes da coleta completa
- [ ] Mapeamento de quais endpoints cada prefeitura suporta
- [ ] Normalização de campos com nomes diferentes
- [ ] Conversão segura de tipos (datas, valores, etc.)
- [ ] Tratamento de campos ausentes vs extras
- [ ] Registro de divergências de schema para auditoria

**Robustez:**
- [ ] Adição de metadados em cada registro (prefeitura_id, endpoint, data_coleta)
- [ ] Tratamento de erros HTTP (404, 500, timeout)
- [ ] Validação de formato JSON (evitar HTML de erro)
- [ ] Retry logic com exponential backoff
- [ ] Rate limiting entre requisições (1-2s)
- [ ] Delay maior entre prefeituras (5-10s)
- [ ] Skip automático de endpoints indisponíveis

**Qualidade:**
- [ ] Logging detalhado de progresso e erros
- [ ] Validação básica dos dados coletados
- [ ] Análise de compatibilidade de schemas entre prefeituras
- [ ] Relatório de campos universais vs parciais
- [ ] Salvamento em formato eficiente (Parquet preferível)

**Processo:**
- [ ] Coleta em 2 fases: (1) verificação de disponibilidade, (2) coleta histórica
- [ ] Checkpoint/resume para retomar coletas interrompidas
- [ ] Documentação do código
- [ ] Testes com pelo menos 2-3 prefeituras antes de rodar completo
- [ ] Gerar arquivo de mapeamento de endpoints disponíveis
- [ ] Gerar relatório de divergências de schema

---

**Documento criado em:** 26 de dezembro de 2025  
**Versão:** 1.0  
**Objetivo:** Guiar agentes na criação de ferramentas de automação para coleta de dados de transparência pública

```
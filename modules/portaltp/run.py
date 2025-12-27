import pandas as pd
import requests
import os
import xml.etree.ElementTree as ET
import json
from .config import YEARS, MONTHS

DATA_DIR = "data/portaltp"
CONTROL_FILE = "data/control_portaltp.json"
ENDPOINTS = {
    "licitacoes": "transparencia.asmx/json_licitacoes",
    "contratos": "transparencia.asmx/json_contratos",
    "empenhos": "transparencia.asmx/json_empenhos",
    "liquidacoes": "transparencia.asmx/json_liquidacoes",
    "pagamentos": "transparencia.asmx/json_pagamentos",
    "obras": "transparencia.asmx/json_obras",
    "ordem_cronologica": "transparencia.asmx/json_ordem_cronologica_a_pagar",
    "atas": "transparencia.asmx/json_atas",
    "ordemcompras": "transparencia.asmx/json_ordemcompras",
}

def get_prefeituras():
    """Reads the prefeituras.csv file and returns a pandas DataFrame."""
    return pd.read_csv("modules/portaltp/prefeituras.csv")

def read_control_file():
    """Reads the control file and returns a dictionary."""
    if not os.path.exists(CONTROL_FILE):
        return {}
    with open(CONTROL_FILE, "r") as f:
        return json.load(f)

def write_control_file(data):
    """Writes a dictionary to the control file."""
    os.makedirs(os.path.dirname(CONTROL_FILE), exist_ok=True)
    with open(CONTROL_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_data(url, endpoint, year, month=None):
    """Fetches data from the API and returns a list of dictionaries."""
    params = {"ano": year}
    if month:
        params["mes"] = str(month)
    if "licitacoes" in endpoint:
        params["extra"] = "False"
        params["situacao"] = ""

    try:
        response = requests.get(f"{url}{endpoint}", params=params, timeout=10)
        response.raise_for_status()
        # Handle XML response
        tree = ET.fromstring(response.content)
        json_string = tree.text
        data = json.loads(json_string)
        return data
    except requests.exceptions.RequestException:
        return None
    except (ValueError, ET.ParseError):
        return None


def save_to_parquet(data, prefeitura_name, endpoint_name):
    """Appends a list of dictionaries to a Parquet file for the endpoint."""
    if not data:
        return

    df = pd.DataFrame(data)
    df["prefeitura"] = prefeitura_name
    
    os.makedirs(DATA_DIR, exist_ok=True)
    
    parquet_filename = os.path.join(DATA_DIR, f"{endpoint_name}.parquet")
    if os.path.exists(parquet_filename):
        existing_df = pd.read_parquet(parquet_filename)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_parquet(parquet_filename, engine='pyarrow')
    else:
        df.to_parquet(parquet_filename, engine='pyarrow')

def run():
    """Main function to fetch and save data for the portaltp module."""
    prefeituras = get_prefeituras()
    control_data = read_control_file()

    for _, prefeitura in prefeituras.iterrows():
        municipio_name = prefeitura["municipio"].replace(' ', '_')
        prefeitura_name = prefeitura["prefeitura"]
        url = prefeitura["url"]
        
        if municipio_name not in control_data:
            control_data[municipio_name] = {}

        print(f"Processing {municipio_name}...")
        for endpoint_name, endpoint_path in ENDPOINTS.items():
            if endpoint_name not in control_data[municipio_name]:
                control_data[municipio_name][endpoint_name] = {}

            print(f"  Fetching {endpoint_name}...")
            for year in YEARS:
                if year not in control_data[municipio_name][endpoint_name]:
                    control_data[municipio_name][endpoint_name][year] = []

                if "licitacoes" in endpoint_name or "empenhos" in endpoint_name or "liquidacoes" in endpoint_name or "pagamentos" in endpoint_name or "obras" in endpoint_name or "ordemcompras" in endpoint_name:
                    for month in MONTHS:
                        if month not in control_data[municipio_name][endpoint_name][year]:
                            data = get_data(url, endpoint_path, year, month)
                            if data:
                                save_to_parquet(data, prefeitura_name, endpoint_name)
                                control_data[municipio_name][endpoint_name][year].append(month)
                else:
                    if 0 not in control_data[municipio_name][endpoint_name][year]: # 0 represents the whole year
                        data = get_data(url, endpoint_path, year)
                        if data:
                            save_to_parquet(data, prefeitura_name, endpoint_name)
                            control_data[municipio_name][endpoint_name][year].append(0)

    write_control_file(control_data)
    print("\n--- Finished processing portaltp module ---")

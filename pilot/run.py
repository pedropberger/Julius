
import pandas as pd
import requests
import os
import xml.etree.ElementTree as ET
import json

# Configuration
MUNICIPALITIES = ["afonso claudio", "sao gabriel da palha"]
YEAR = "2025"
ENDPOINTS = {
    "licitacoes": "transparencia.asmx/json_licitacoes",
    "contratos": "transparencia.asmx/json_contratos",
}
DATA_DIR = "pilot/data/parquet"

def get_prefeituras():
    """Reads the prefeituras.csv file and returns a pandas DataFrame."""
    return pd.read_csv("modules/portaltp/prefeituras.csv")

def get_data(url, endpoint, year):
    """Fetches data from the API and returns a list of dictionaries."""
    all_data = []
    
    # Common parameters for both endpoints
    params = {"ano": year}

    # The 'licitacoes' endpoint requires the 'mes' parameter
    if "licitacoes" in endpoint:
        for month in range(1, 13):
            params["mes"] = str(month).zfill(2)
            params["extra"] = "False"
            params["situacao"] = "."
            try:
                response = requests.get(f"{url}{endpoint}", params=params)
                response.raise_for_status()
                # Handle XML response
                tree = ET.fromstring(response.content)
                json_string = tree.text
                data = json.loads(json_string)
                if data:
                    all_data.extend(data)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching data from {url}{endpoint} for month {month}: {e}")
            except (ValueError, ET.ParseError):
                print(f"Could not decode JSON from {url}{endpoint} for month {month}. Response text: {response.text}")
    else: # For 'contratos' and other endpoints that do not require 'mes'
        try:
            response = requests.get(f"{url}{endpoint}", params=params)
            response.raise_for_status()
            # Handle XML response
            tree = ET.fromstring(response.content)
            json_string = tree.text
            data = json.loads(json_string)
            if data:
                all_data.extend(data)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}{endpoint}: {e}")
        except (ValueError, ET.ParseError):
            print(f"Could not decode JSON from {url}{endpoint}. Response text: {response.text}")


    return all_data

def save_to_parquet(data, municipality, year, endpoint_name):
    """Saves a list of dictionaries to a Parquet file in a structured directory."""
    if not data:
        print(f"No data to save for {municipality} - {endpoint_name}")
        return

    df = pd.DataFrame(data)
    
    # Create directory structure
    output_dir = os.path.join(DATA_DIR, municipality, year)
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to Parquet
    parquet_filename = os.path.join(output_dir, f"{endpoint_name}.parquet")
    df.to_parquet(parquet_filename)
    print(f"Data saved to {parquet_filename}")

def main():
    """Main function for the pilot project."""
    prefeituras = get_prefeituras()
    target_prefeituras = prefeituras[prefeituras["municipio"].isin(MUNICIPALITIES)]

    for _, prefeitura in target_prefeituras.iterrows():
        municipio = prefeitura["municipio"].replace(' ', '_')
        url = prefeitura["url"]
        for endpoint_name, endpoint_path in ENDPOINTS.items():
            print(f"Fetching {endpoint_name} for {municipio}...")
            data = get_data(url, endpoint_path, YEAR)
            save_to_parquet(data, municipio, YEAR, endpoint_name)
            print("-" * 50)

if __name__ == "__main__":
    main()

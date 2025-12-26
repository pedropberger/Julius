
import pandas as pd
import requests
import os
import xml.etree.ElementTree as ET
import json

# Configuration
MUNICIPALITIES = ["afonso claudio", "sao gabriel da palha"]
YEARS = ["2024", "2025"]
ENDPOINTS = {
    "licitacoes": "transparencia.asmx/json_licitacoes",
    "contratos": "transparencia.asmx/json_contratos",
}
DATA_DIR = "pilot/data/parquet"
CONTROL_FILE = "pilot/data/control.json"

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
        response = requests.get(f"{url}{endpoint}", params=params)
        response.raise_for_status()
        # Handle XML response
        tree = ET.fromstring(response.content)
        json_string = tree.text
        data = json.loads(json_string)
        return data
    except requests.exceptions.RequestException as e:
        # print(f"Error fetching data from {url}{endpoint} for year {year} and month {month}: {e}")
        return None
    except (ValueError, ET.ParseError):
        # print(f"Could not decode JSON from {url}{endpoint} for year {year} and month {month}. Response text: {response.text}")
        return None


def save_to_parquet(data, municipality_name, prefeitura_name, endpoint_name):
    """Appends a list of dictionaries to a Parquet file for the municipality."""
    if not data:
        return

    df = pd.DataFrame(data)
    df["prefeitura"] = prefeitura_name
    
    # Create directory structure
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Save to Parquet
    parquet_filename = os.path.join(DATA_DIR, f"{municipality_name}_{endpoint_name}.parquet")
    if os.path.exists(parquet_filename):
        existing_df = pd.read_parquet(parquet_filename)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_parquet(parquet_filename, engine='pyarrow')
    else:
        df.to_parquet(parquet_filename, engine='pyarrow')

def main():
    """Main function for the pilot project."""
    prefeituras = get_prefeituras()
    target_prefeituras = prefeituras[prefeituras["municipio"].isin(MUNICIPALITIES)]

    control_data = read_control_file()

    for _, prefeitura in target_prefeituras.iterrows():
        municipio_name = prefeitura["municipio"].replace(' ', '_')
        prefeitura_name = prefeitura["prefeitura"]
        url = prefeitura["url"]
        
        if municipio_name not in control_data:
            control_data[municipio_name] = {}

        for endpoint_name, endpoint_path in ENDPOINTS.items():
            if endpoint_name not in control_data[municipio_name]:
                control_data[municipio_name][endpoint_name] = {}

            print(f"Fetching {endpoint_name} for {municipio_name}...")
            for year in YEARS:
                if year not in control_data[municipio_name][endpoint_name]:
                    control_data[municipio_name][endpoint_name][year] = []

                if "licitacoes" in endpoint_name:
                    for month in range(1, 13):
                        if month not in control_data[municipio_name][endpoint_name][year]:
                            data = get_data(url, endpoint_path, year, month)
                            if data:
                                save_to_parquet(data, municipio_name, prefeitura_name, endpoint_name)
                                control_data[municipio_name][endpoint_name][year].append(month)
                                print(f"  Data found for {year}/{month}")
                            else:
                                print(f"  No data for {year}/{month}")
                else:
                    if 0 not in control_data[municipio_name][endpoint_name][year]: # 0 represents the whole year
                        data = get_data(url, endpoint_path, year)
                        if data:
                            save_to_parquet(data, municipio_name, prefeitura_name, endpoint_name)
                            control_data[municipio_name][endpoint_name][year].append(0)
                            print(f"  Data found for {year}")
                        else:
                            print(f"  No data for {year}")

    write_control_file(control_data)
    print("\n--- Pilot finished ---")


if __name__ == "__main__":
    main()

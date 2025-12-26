
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

def get_prefeituras():
    """Reads the prefeituras.csv file and returns a pandas DataFrame."""
    return pd.read_csv("modules/portaltp/prefeituras.csv")

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
        print(f"Error fetching data from {url}{endpoint} for year {year} and month {month}: {e}")
        return None
    except (ValueError, ET.ParseError):
        print(f"Could not decode JSON from {url}{endpoint} for year {year} and month {month}. Response text: {response.text}")
        return None


def save_to_parquet(data, municipality, year, endpoint_name, month=None):
    """Saves a list of dictionaries to a Parquet file in a structured directory."""
    if not data:
        # print(f"No data to save for {municipality} - {endpoint_name} for year {year} and month {month}")
        return

    df = pd.DataFrame(data)
    
    # Create directory structure
    output_dir = os.path.join(DATA_DIR, municipality, year)
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to Parquet
    if month:
        parquet_filename = os.path.join(output_dir, f"{endpoint_name}_{month}.parquet")
    else:
        parquet_filename = os.path.join(output_dir, f"{endpoint_name}.parquet")
    df.to_parquet(parquet_filename)
    # print(f"Data saved to {parquet_filename}")
    return True

def main():
    """Main function for the pilot project."""
    prefeituras = get_prefeituras()
    target_prefeituras = prefeituras[prefeituras["municipio"].isin(MUNICIPALITIES)]

    results = {}

    for _, prefeitura in target_prefeituras.iterrows():
        municipio_name = prefeitura["municipio"].replace(' ', '_')
        results[municipio_name] = {}
        url = prefeitura["url"]
        for endpoint_name, endpoint_path in ENDPOINTS.items():
            results[municipio_name][endpoint_name] = {"2024": [], "2025": []}
            print(f"Fetching {endpoint_name} for {municipio_name}...")
            for year in YEARS:
                if "licitacoes" in endpoint_name:
                    for month in range(1, 13):
                        data = get_data(url, endpoint_path, year, month)
                        if save_to_parquet(data, municipio_name, year, endpoint_name, month):
                            results[municipio_name][endpoint_name][year].append(month)
                else:
                    data = get_data(url, endpoint_path, year)
                    if save_to_parquet(data, municipio_name, year, endpoint_name):
                        results[municipio_name][endpoint_name][year].append(0) # 0 represents the whole year
    
    print("\n--- Summary ---")
    for municipio, endpoints in results.items():
        print(f"\n{municipio}:")
        for endpoint, years in endpoints.items():
            print(f"  {endpoint}:")
            for year, months in years.items():
                if months:
                    if 0 in months:
                        print(f"    {year}: Success")
                    else:
                        print(f"    {year}: Months with data: {sorted(months)}")
                else:
                    print(f"    {year}: No data found")


if __name__ == "__main__":
    main()

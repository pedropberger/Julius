
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import json

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
YEAR = "2024"
MONTH = "1"

def get_prefeituras():
    """Reads the prefeituras.csv file and returns a pandas DataFrame."""
    return pd.read_csv("modules/portaltp/prefeituras.csv")

def test_api(url, endpoint):
    """Tests a single API endpoint and returns 'Success' or an error message."""
    params = {"ano": YEAR}
    if "licitacoes" in endpoint or "empenhos" in endpoint or "liquidacoes" in endpoint or "pagamentos" in endpoint or "obras" in endpoint or "ordemcompras" in endpoint:
        params["mes"] = MONTH
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
        return "Success"
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {e.response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}"
    except (ValueError, ET.ParseError):
        return "JSON Decode Error"

def main():
    """Main function for the API testing script."""
    prefeituras = get_prefeituras()
    results = []

    for _, prefeitura in prefeituras.iterrows():
        municipio = prefeitura["municipio"]
        url = prefeitura["url"]
        
        result_row = {"municipio": municipio, "url": url}

        print(f"Testing APIs for {municipio}...")
        for endpoint_name, endpoint_path in ENDPOINTS.items():
            result = test_api(url, endpoint_path)
            result_row[endpoint_name] = result
        
        results.append(result_row)

    df = pd.DataFrame(results)
    df.to_csv("api_test_results.csv", index=False)
    print("\nAPI test results saved to api_test_results.csv")

if __name__ == "__main__":
    main()

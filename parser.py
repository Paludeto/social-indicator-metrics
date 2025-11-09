import requests, sys, json
from dataclasses import dataclass, asdict

@dataclass
class Country:
    iso2_id: str
    name: str
    region: str
    subregion: str
    education_expenses: float
    health_expenses: float
    literacy_rate: float
    mortality_rate: float

def get_url_data(url, retries=10):

    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            if attempt == retries - 1:
                print(f"Couldn't access API data after {attempt} attempts: {e}")
                sys.exit(1)

def check_fields(output):

    for i in range(0, len(output)):
        series = output[i].get("series")
        if not series or not series[0].get("serie"):
            return False
        
    return True

def extract_recent_data(output):

    recent_values = []

    for indicator in output:

        series_list = indicator.get("series", [])
        if not series_list:
            recent_values.append(None)
            continue

        serie_entries = series_list[0].get("serie", [])
        if not serie_entries:
            recent_values.append(None)
            continue

        # {year: value} conversion
        data = {}
        for entry in serie_entries:
            for key, value in entry.items():
                if key.isdigit():
                    data[int(key)] = value

        # most recent non-null
        value = next((data[y] for y in sorted(data.keys(), reverse=True) if data[y] is not None), None)
        recent_values.append(value)

    return recent_values

def parse_countries():

    output = get_url_data('https://servicodados.ibge.gov.br/api/v1/paises/').json()
    country_list = []

    for country_data in output:
        
        iso2_id = country_data['id']['ISO-3166-1-ALPHA-2']
        name = country_data['nome']['abreviado']
        region = country_data.get("localizacao", {}).get("regiao", {}).get("nome", "Desconhecido")
        subregion = country_data.get("localizacao", {}).get("sub-regiao", {}).get("nome", "Desconhecido")

        print(name)
        
        r = get_url_data(f'https://servicodados.ibge.gov.br/api/v1/paises/{iso2_id}/indicadores/77850|77836|77820|77819')
        output = r.json()

        if (check_fields(output)):
            education_expenses, health_expenses, literacy_rate, mortality_rate = extract_recent_data(output)    
            country_list.append(Country(iso2_id, name, region, subregion, education_expenses, health_expenses, literacy_rate, mortality_rate))

    countries_dict = [asdict(country) for country in country_list]

    with open("countries.json", "w", encoding="utf-8") as f:
        json.dump(countries_dict, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    parse_countries()
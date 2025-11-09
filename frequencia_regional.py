import pandas as pd
import requests

try:
    df = pd.read_json('countries.json')
except:
    print("ERRO: 'countries.json' não encontrado.")
    exit()

try:
    url = "https://servicodados.ibge.gov.br/api/v1/paises/"
    dados_paises = requests.get(url).json()
    mapa = {p['id']['ISO-3166-1-ALPHA-2']: p['localizacao']['regiao']['nome'] for p in dados_paises}
    df['regiao'] = df['iso2_id'].map(mapa)
except:
    print("Erro na API do IBGE.")
    exit()

freq_absoluta = df['regiao'].value_counts()
freq_relativa = df['regiao'].value_counts(normalize=True) * 100
freq_acumulada = freq_relativa.cumsum()

tabela_freq = pd.DataFrame({
    'Frequência Absoluta': freq_absoluta,
    'Frequência Relativa (%)': freq_relativa.round(2),
    'Frequência Acumulada (%)': freq_acumulada.round(2)
})

print("\n=== Tabela de Frequência por Região ===\n")
print(tabela_freq)
print("\n=======================================")
tabela_freq.to_csv('tabela_frequencia_regiao.csv')
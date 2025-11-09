import pandas as pd
import requests

print("Carregando dados e obtendo regiões...")
try:
    df = pd.read_json('countries.json')
    df.set_index('name', inplace=True)
except FileNotFoundError:
    print("ERRO: 'countries.json' não encontrado.")
    exit()

try:
    url = "https://servicodados.ibge.gov.br/api/v1/paises/"
    dados_paises = requests.get(url, timeout=10).json()
    mapa = {p['id']['ISO-3166-1-ALPHA-2']: p['localizacao']['regiao']['nome'] for p in dados_paises}
    df['regiao'] = df['iso2_id'].map(mapa)
except Exception as e:
    print(f"Erro na API do IBGE: {e}")
    exit()

variaveis = {
    'education_expenses': 'Gastos Educação (% PIB)',
    'health_expenses': 'Gastos Saúde (% PIB)',
    'literacy_rate': 'Alfabetização (%)',
    'mortality_rate': 'Mortalidade (por 1000)'
}
for col in variaveis.keys():
    df[col] = pd.to_numeric(df[col], errors='coerce')

df_clean = df.dropna(subset=list(variaveis.keys()) + ['regiao'])

def calcular_stats(dataframe):
    stats = {}
    for col_orig, col_nome in variaveis.items():
        dados = dataframe[col_orig]
        media = dados.mean()
        moda = dados.mode().iloc[0] if not dados.mode().empty else 'N/A'
        std = dados.std()
        stats[col_nome] = {
            'Média': media,
            'Mediana (Q2)': dados.median(),
            'Moda': moda,
            'Variância': dados.var(),
            'Desvio Padrão': std,
            'CV (%)': (std / media * 100) if media != 0 else 0,
            'Amplitude': dados.max() - dados.min(),
            'Q1 (25%)': dados.quantile(0.25),
            'Q2 (50%)': dados.quantile(0.50),
            'Q3 (75%)': dados.quantile(0.75),
            'IQR': dados.quantile(0.75) - dados.quantile(0.25),
            'P10 (10%)': dados.quantile(0.10),
            'P90 (90%)': dados.quantile(0.90),
            'N (Países)': len(dados)
        }
    return pd.DataFrame(stats)

regioes = df_clean['regiao'].unique()

for regiao in regioes:
    print(f"\nGenerating stats for region: {regiao}...")
    df_regiao = df_clean[df_clean['regiao'] == regiao]
    
    tabela_regiao = calcular_stats(df_regiao)
    
    tabela_regiao = tabela_regiao.round(2)
    tabela_regiao = tabela_regiao.astype(object)
    tabela_regiao.loc['N (Países)'] = tabela_regiao.loc['N (Países)'].astype(int)
    
    print(f"\n=== Estatísticas: {regiao} ===")
    print(tabela_regiao)
    tabela_regiao.to_csv(f'estatisticas_{regiao}.csv')

print("\n\nSucesso! Todas as tabelas regionais foram criadas.")
import pandas as pd

try:
    df = pd.read_json('countries.json')
except FileNotFoundError:
    print("ERRO: 'countries.json' não encontrado.")
    exit()

variaveis = {
    'education_expenses': 'Gastos Educação (% PIB)',
    'health_expenses': 'Gastos Saúde (% PIB)',
    'literacy_rate': 'Alfabetização (%)',
    'mortality_rate': 'Mortalidade (por 1000)'
}

for col in variaveis.keys():
    df[col] = pd.to_numeric(df[col], errors='coerce')

df_clean = df.dropna(subset=list(variaveis.keys()))

tabela_stats = {}

for col_original, col_nome in variaveis.items():
    dados = df_clean[col_original]

    media = dados.mean()
    mediana = dados.median()
    moda = dados.mode().iloc[0] if not dados.mode().empty else 'N/A'
    var = dados.var()
    std = dados.std()
    cv = (std / media) * 100
    amplitude = dados.max() - dados.min()
    q1 = dados.quantile(0.25)
    q2 = dados.quantile(0.50)
    q3 = dados.quantile(0.75)
    iqr = q3 - q1
    p10 = dados.quantile(0.10)
    p90 = dados.quantile(0.90)

    tabela_stats[col_nome] = {
        'Média': media,
        'Mediana (Q2)': mediana,
        'Moda': moda,
        'Variância': var,
        'Desvio Padrão': std,
        'CV (%)': cv,
        'Amplitude': amplitude,
        'Q1 (25%)': q1,
        'Q2 (50%)': q2,
        'Q3 (75%)': q3,
        'IQR': iqr,
        'P10 (10%)': p10,
        'P90 (90%)': p90,
        'N (Países)': len(dados)
    }

df_tabela = pd.DataFrame(tabela_stats)
df_tabela = df_tabela.round(2)
df_tabela = df_tabela.astype(object)
df_tabela.loc['N (Países)'] = df_tabela.loc['N (Países)'].astype(int)

print("\n=== Tabela de Estatísticas Descritivas ===\n")
print(df_tabela)
print("\n=====================================================")

df_tabela.to_csv('tabela_estatisticas_completa.csv')
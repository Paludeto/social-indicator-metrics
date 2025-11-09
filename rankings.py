import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    df = pd.read_json('countries.json')
    df.set_index('name', inplace=True)
except FileNotFoundError:
    print("ERRO: 'countries.json' não encontrado.")
    exit()

variaveis = {
    'education_expenses': 'Gastos com Educação (% do PIB)',
    'health_expenses': 'Gastos com Saúde (% do PIB)',
    'literacy_rate': 'Taxa de Alfabetização (%)',
    'mortality_rate': 'Taxa de Mortalidade (por 1000 hab.)'
}

for col in variaveis.keys():
    df[col] = pd.to_numeric(df[col], errors='coerce')

df.dropna(subset=list(variaveis.keys()), how='all', inplace=True)

sns.set_theme(style="whitegrid")

for col_id, col_nome in variaveis.items():
    print(f"Gerando rankings para: {col_nome}...")
    df_sorted = df.sort_values(by=col_id).dropna(subset=[col_id])

    plt.figure(figsize=(10, 6))
    top_10_menor = df_sorted.head(10)
    sns.barplot(x=top_10_menor[col_id], y=top_10_menor.index, color='steelblue')
    plt.title(f'Top 10 Menores: {col_nome}')
    plt.xlabel(col_nome)
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(f"ranking_menor_{col_id}.png")
    plt.close()

    plt.figure(figsize=(10, 6))
    top_10_maior = df_sorted.tail(10).iloc[::-1]
    sns.barplot(x=top_10_maior[col_id], y=top_10_maior.index, color='red')
    plt.title(f'Top 10 Maiores: {col_nome}')
    plt.xlabel(col_nome)
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(f"ranking_maior_{col_id}.png")
    plt.close()

print("\nSucesso! Gráficos regerados.")
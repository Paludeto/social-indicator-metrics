import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ARQ_DADOS = "countries.json"
ARQ_FIG = "BOXPLOTS_por_regiao.png"
ARQ_TABELA = "estatisticas_por_regiao.csv"

COLS_NUM = ["education_expenses", "health_expenses", "literacy_rate", "mortality_rate"]
TITULOS = {
    "mortality_rate": "Taxa de Mortalidade por Região (‰)",
    "education_expenses": "Gastos com Educação (% do PIB)",
    "health_expenses": "Gastos com Saúde (% do PIB)",
    "literacy_rate": "Taxa de Alfabetização (%)",
}

def carregar_dados(filepath: str) -> pd.DataFrame:
    try:
        df = pd.read_json(filepath)
    except Exception as e:
        raise SystemExit(f"Erro ao ler '{filepath}': {e}")

    # Converte colunas numéricas
    df[COLS_NUM] = df[COLS_NUM].apply(pd.to_numeric, errors="coerce")

    # Ordena regiões num padrão útil para leitura (opcional)
    ordem_regioes = ["Europa", "América", "Ásia", "África", "Oceania"]
    if "region" in df.columns:
        df["region"] = pd.Categorical(df["region"], categories=ordem_regioes, ordered=True)
    else:
        raise SystemExit("Coluna 'region' não encontrada no dataset.")

    return df

def gerar_boxplots(df: pd.DataFrame, caminho_fig: str = ARQ_FIG) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    pares = [
        ("mortality_rate", axes[0, 0]),
        ("education_expenses", axes[0, 1]),
        ("health_expenses", axes[1, 0]),
        ("literacy_rate", axes[1, 1]),
    ]

    for col, ax in pares:
        df.boxplot(column=col, by="region", ax=ax, grid=False)
        ax.set_title(TITULOS[col])
        ax.set_xlabel("Região")
        ax.tick_params(axis="x", rotation=0)

    plt.suptitle("Distribuição dos Indicadores Sociais por Região")
    plt.tight_layout()
    try:
        fig._suptitle.set_y(0.98)
    except Exception:
        pass
    plt.savefig(caminho_fig, dpi=200, bbox_inches="tight")
    plt.close(fig)

def gerar_estatisticas(df: pd.DataFrame, caminho_csv: str = ARQ_TABELA) -> pd.DataFrame:
    stats = df.groupby("region")[COLS_NUM].agg(["mean", "std"]).round(2)
    stats.to_csv(caminho_csv, encoding="utf-8")
    return stats

def main():
    base = Path(".")
    df = carregar_dados(str(base / ARQ_DADOS))

    gerar_boxplots(df, str(base / ARQ_FIG))
    stats = gerar_estatisticas(df, str(base / ARQ_TABELA))
    
    print(stats.head())

if __name__ == "__main__":
    main()

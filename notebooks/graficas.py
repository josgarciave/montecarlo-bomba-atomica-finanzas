"""Gráficas del notebook de VaR con la estética de la charla (Semillero Aperture).

Uso desde el notebook:

    import graficas
    graficas.aplicar_estilo()
    graficas.precio(precios["AMZN"])

Cada función dibuja la figura, la guarda como PNG en ``figuras/`` (para las
diapositivas) y la muestra.
"""

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
from scipy import stats

# Paleta de la charla
TURQUESA, AMBAR, CORAL = "#0E7C86", "#E5A50A", "#E8685A"
TINTA, GRIS, LINEA = "#0F1B2A", "#4A6072", "#DCE4EA"

# Carpeta de gráficas para las diapositivas (raíz del repositorio)
FIGURAS = Path(__file__).resolve().parent.parent / "figuras"

usd = FuncFormatter(lambda x, _: f"{x:,.0f}")


def aplicar_estilo():
    """Configura matplotlib con la tipografía y la paleta de la charla."""
    try:
        from matplotlib_inline.backend_inline import set_matplotlib_formats
        set_matplotlib_formats("retina")
    except ImportError:
        pass

    plt.rcParams.update({
        "font.family": ["JetBrains Mono", "Courier New", "DejaVu Sans Mono"],
        "font.size": 10,
        "text.color": TINTA,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "figure.dpi": 110,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "axes.edgecolor": LINEA,
        "axes.linewidth": 1,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "grid.color": LINEA,
        "grid.linewidth": 1,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 12,
        "axes.labelcolor": GRIS,
        "axes.labelsize": 9,
        "xtick.color": GRIS,
        "ytick.color": GRIS,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "lines.linewidth": 2,
        "lines.solid_capstyle": "round",
        "lines.solid_joinstyle": "round",
        "legend.frameon": False,
        "legend.fontsize": 9,
        "axes.prop_cycle": plt.cycler(color=[TURQUESA, AMBAR, CORAL]),
    })


def _guardar_y_mostrar(fig, nombre):
    FIGURAS.mkdir(exist_ok=True)
    fig.savefig(FIGURAS / f"{nombre}.png")
    plt.show()


def _histograma(ax, datos, color=TURQUESA, etiqueta=None, bins=60, rango=None, densidad=True):
    """Histograma como línea escalonada de 2px con un relleno suave del mismo color."""
    alturas, bordes = np.histogram(datos, bins=bins, range=rango, density=densidad)
    ax.stairs(alturas, bordes, color=color, linewidth=2, label=etiqueta)
    ax.stairs(alturas, bordes, fill=True, color=color, alpha=0.10)
    return alturas, bordes


def precio(serie: pd.Series):
    """Serie de precios con el último valor marcado."""
    fig, ax = plt.subplots(figsize=(9, 3.4))
    ax.plot(serie.index, serie.values, color=TURQUESA)
    ax.plot(serie.index[-1], serie.iloc[-1], "o", ms=8, color=TURQUESA, mec="white", mew=2)
    ax.annotate(f"USD {serie.iloc[-1]:,.2f}", (serie.index[-1], serie.iloc[-1]),
                xytext=(10, 0), textcoords="offset points", va="center", fontsize=9)
    ax.set_xlim(serie.index[0], serie.index[-1] + pd.Timedelta(days=110))
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.yaxis.set_major_formatter(usd)
    ax.set_title(f"Precio de cierre ajustado de {serie.name} (USD)")
    _guardar_y_mostrar(fig, "var_00_precio")


def uniformes(u):
    """Paso 01: histograma de las uniformes frente a la densidad teórica U(0, 1)."""
    fig, ax = plt.subplots(figsize=(9, 3.2))
    _histograma(ax, u, etiqueta="Simulado", bins=50, rango=(0, 1))
    ax.axhline(1, color=AMBAR, label="Densidad teórica U(0, 1)")
    ax.set_ylim(0, 1.35)
    ax.set_xlabel("u")
    ax.set_ylabel("densidad")
    ax.set_title(f"{len(u):,} números uniformes: la densidad es plana")
    ax.legend(loc="upper right", ncols=2)
    _guardar_y_mostrar(fig, "var_01_uniformes")


def normales(z):
    """Paso 02: histograma de norm.ppf(U) frente a la densidad N(0, 1)."""
    x = np.linspace(-4.5, 4.5, 400)
    fig, ax = plt.subplots(figsize=(9, 3.2))
    _histograma(ax, z, etiqueta="Simulado: norm.ppf(U)", bins=90, rango=(-4.5, 4.5))
    ax.plot(x, stats.norm.pdf(x), color=AMBAR, label="N(0, 1) teórica")
    ax.set_xlabel("z")
    ax.set_ylabel("densidad")
    ax.set_title("Transformada inversa: de uniformes a normales estándar")
    ax.legend(loc="upper right")
    _guardar_y_mostrar(fig, "var_02_normales")


def shocks_vs_historico(shocks, rendimientos: pd.Series):
    """Paso 05: rendimientos simulados vs históricos y QQ-plot de los históricos."""
    hist = rendimientos.values * 100
    sim = np.asarray(shocks) * 100
    lim = np.abs(hist).max() * 1.05
    bordes = np.linspace(-lim, lim, 71)   # mismos intervalos para comparar ambas distribuciones

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw={"width_ratios": [3, 2]})

    _histograma(ax1, sim, TURQUESA, "Simulado (normal)", bins=bordes)
    _histograma(ax1, hist, AMBAR, "Histórico", bins=bordes)
    ax1.set_xlabel("rendimiento diario (%)")
    ax1.set_ylabel("densidad")
    ax1.set_title("Rendimiento diario: simulado vs histórico")
    ax1.legend(loc="upper right")

    (teorico, observado), (pendiente, intercepto, _) = stats.probplot(hist, dist="norm")
    ax2.plot(teorico, observado, "o", ms=5, color=AMBAR, mew=0, label="Histórico")
    ax2.plot(teorico, pendiente * teorico + intercepto, color=TURQUESA, label="Normal ajustada")
    ax2.set_xlabel("cuantil teórico N(0, 1)")
    ax2.set_ylabel("rendimiento (%)")
    ax2.set_title("QQ-plot: colas más pesadas que la normal")
    ax2.legend(loc="upper left")

    fig.tight_layout(w_pad=3)
    _guardar_y_mostrar(fig, "var_05_shocks")


def pnl_simulado(pnl, ticker):
    """Paso 06: distribución del P&L simulado."""
    fig, ax = plt.subplots(figsize=(9, 3.4))
    _histograma(ax, pnl, bins=90, densidad=False)
    ax.axvline(0, color=GRIS, linewidth=1)
    ax.xaxis.set_major_formatter(usd)
    ax.yaxis.set_major_formatter(usd)
    ax.set_xlabel("P&L a 1 día (USD)")
    ax.set_ylabel("escenarios")
    ax.set_title(f"P&L simulado de la posición en {ticker} ({len(pnl):,} escenarios)")
    _guardar_y_mostrar(fig, "var_06_pnl")


def var_montecarlo(pnl, var, k, confianza):
    """Paso 07: cola del P&L más allá del VaR y los peores escenarios ordenados."""
    pnl_ordenado = np.sort(pnl)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8))

    # Izquierda: distribución completa con la cola más allá del VaR en coral
    conteo, bordes = _histograma(ax1, pnl, bins=90, densidad=False, etiqueta="P&L simulado")
    cola, _ = np.histogram(pnl[pnl <= -var], bins=bordes)
    ax1.stairs(cola, bordes, fill=True, color=CORAL, alpha=0.35,
               label=f"Peor {1 - confianza:.0%} de escenarios")
    ax1.axvline(-var, color=CORAL)
    ax1.annotate(f"VaR {confianza:.0%}\nUSD {var:,.0f}", (-var, conteo.max() * 0.45),
                 xytext=(-8, 0), textcoords="offset points", ha="right", fontsize=9)
    ax1.xaxis.set_major_formatter(usd)
    ax1.yaxis.set_major_formatter(usd)
    ax1.set_xlabel("P&L a 1 día (USD)")
    ax1.set_ylabel("escenarios")
    ax1.set_title("Distribución del P&L y VaR")
    ax1.set_ylim(0, conteo.max() * 1.4)   # espacio para la leyenda
    ax1.legend(loc="upper right")

    # Derecha: los peores escenarios ordenados y el k-ésimo peor caso
    m = 3 * k
    ax2.plot(np.arange(1, m + 1), pnl_ordenado[:m], color=TURQUESA)
    ax2.plot(k, pnl_ordenado[k - 1], "o", ms=9, color=CORAL, mec="white", mew=2, zorder=3)
    ax2.annotate(f"escenario k = {k:,}\nUSD {pnl_ordenado[k - 1]:,.0f}", (k, pnl_ordenado[k - 1]),
                 xytext=(12, -24), textcoords="offset points", fontsize=9)
    ax2.xaxis.set_major_formatter(usd)
    ax2.yaxis.set_major_formatter(usd)
    ax2.set_xlabel("posición (1 = peor escenario)")
    ax2.set_ylabel("P&L (USD)")
    ax2.set_title(f"Los {m:,} peores escenarios, ordenados")

    fig.tight_layout(w_pad=3)
    _guardar_y_mostrar(fig, "var_07_var")

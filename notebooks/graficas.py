"""Gráficas del notebook de VaR con la estética de la charla (Semillero Aperture).

Uso desde el notebook:

    import graficas
    graficas.aplicar_estilo()
    graficas.uniformes(U[:, 0])

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
COLORES = [TURQUESA, AMBAR, CORAL]   # un color fijo por activo, en el orden de TICKERS

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


def _plazo(horizonte):
    """Texto del horizonte: "diario" o "a 5 días"."""
    return "diario" if horizonte == 1 else f"a {horizonte} días"


def _separar(valores, separacion):
    """Posiciones de etiquetas cercanas a ``valores`` con al menos ``separacion`` entre sí."""
    orden = np.argsort(valores)
    pos = np.asarray(valores, dtype=float).copy()
    for a, b in zip(orden[:-1], orden[1:]):
        pos[b] = max(pos[b], pos[a] + separacion)
    return pos


def precios(tabla: pd.DataFrame):
    """Precios de varios activos en base 100 (un solo eje), con el último valor marcado."""
    base = tabla / tabla.iloc[0] * 100
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.axhline(100, color=GRIS, linewidth=1)
    for col, color in zip(base.columns, COLORES):
        ax.plot(base.index, base[col], color=color, label=col)
        ax.plot(base.index[-1], base[col].iloc[-1], "o", ms=8, color=color, mec="white", mew=2)

    finales = base.iloc[-1].values
    alto = base.values.max() - min(base.values.min(), 100)
    x_texto = base.index[-1] + pd.Timedelta(days=14)   # etiquetas a la derecha del último punto
    for col, y, y_texto in zip(base.columns, finales, _separar(finales, alto * 0.08)):
        ax.text(x_texto, y_texto, f"{col} {y:,.0f}", va="center", fontsize=9)

    ax.set_xlim(base.index[0], base.index[-1] + pd.Timedelta(days=150))
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.set_ylabel("base 100")
    ax.set_title(f"Precio de cierre ajustado, base 100 = {base.index[0]:%Y-%m-%d}")
    ax.legend(loc="upper left", ncols=len(base.columns))
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


def shocks_vs_historico(shocks, rendimientos: pd.Series, nombre="", horizonte=1):
    """Paso 05: rendimientos simulados vs históricos al mismo horizonte y QQ-plot de los históricos.

    ``rendimientos`` son los logarítmicos diarios; se suman en ventanas móviles de
    ``horizonte`` días para compararlos con los shocks simulados.
    """
    hist = pd.Series(rendimientos).rolling(horizonte).sum().dropna().values * 100
    sim = np.asarray(shocks) * 100
    lim = np.abs(hist).max() * 1.05
    bordes = np.linspace(-lim, lim, 71)   # mismos intervalos para comparar ambas distribuciones

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw={"width_ratios": [3, 2]})

    _histograma(ax1, sim, TURQUESA, "Simulado (normal)", bins=bordes)
    _histograma(ax1, hist, AMBAR, "Histórico", bins=bordes)
    ax1.set_xlabel(f"rendimiento {_plazo(horizonte)} (%)")
    ax1.set_ylabel("densidad")
    ax1.set_title(f"Rendimiento {_plazo(horizonte)}{' ' + nombre if nombre else ''}: simulado vs histórico")
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


def pnl_simulado(pnl, nombre, horizonte=1):
    """Paso 06: distribución del P&L simulado."""
    fig, ax = plt.subplots(figsize=(9, 3.4))
    _histograma(ax, pnl, bins=90, densidad=False)
    ax.axvline(0, color=GRIS, linewidth=1)
    ax.xaxis.set_major_formatter(usd)
    ax.yaxis.set_major_formatter(usd)
    ax.set_xlabel(f"P&L {_plazo(horizonte)} (USD)")
    ax.set_ylabel("escenarios")
    ax.set_title(f"P&L simulado de {nombre} ({len(pnl):,} escenarios)")
    _guardar_y_mostrar(fig, "var_06_pnl")


def diversificacion(var_individual, var_portafolio, tickers):
    """VaR de cada posición apilado (si se midieran por separado) frente al VaR del portafolio."""
    var_individual = np.asarray(var_individual, dtype=float)
    suma = var_individual.sum()
    beneficio = suma - var_portafolio
    ancho = 0.5

    fig, ax = plt.subplots(figsize=(9, 4.2))

    # Barra 1: VaR individuales apilados; el borde blanco separa los segmentos
    base = 0.0
    for ticker, var, color in zip(tickers, var_individual, COLORES):
        ax.bar(0, var, ancho, bottom=base, color=color, edgecolor="white", linewidth=2, label=ticker)
        ax.text(ancho / 2 + 0.04, base + var / 2, f"{ticker}  USD {var:,.0f}", va="center", fontsize=9)
        base += var
    ax.text(0, suma, f"USD {suma:,.0f}", ha="center", va="bottom", fontsize=10, fontweight="bold")

    # Barra 2: VaR conjunto y, encima, el hueco que ahorra la diversificación
    ax.bar(1, var_portafolio, ancho, color=TINTA, edgecolor="white", linewidth=2)
    ax.text(1, var_portafolio / 2, f"USD {var_portafolio:,.0f}", ha="center", va="center",
            fontsize=10, fontweight="bold", color="white")
    ax.bar(1, beneficio, ancho, bottom=var_portafolio, color="white", edgecolor=CORAL,
           linewidth=2, linestyle=(0, (4, 3)))
    ax.text(1 + ancho / 2 + 0.04, var_portafolio + beneficio / 2,
            f"Beneficio de la\ndiversificación\nUSD {beneficio:,.0f} ({beneficio / suma:.0%})",
            va="center", fontsize=9)
    ax.plot([ancho / 2, 1 - ancho / 2], [suma, suma], color=GRIS, linewidth=1, linestyle=":")

    ax.set_xticks([0, 1], ["Cada posición\npor separado", "Portafolio\nconjunto"])
    ax.set_xlim(-0.5, 1.95)
    ax.set_ylim(0, suma * 1.28)   # espacio para el total y la leyenda
    ax.yaxis.set_major_formatter(usd)
    ax.set_ylabel("VaR (USD)")
    ax.set_title("La diversificación reduce el VaR")
    ax.legend(loc="upper left", ncols=len(tickers))
    _guardar_y_mostrar(fig, "var_08_diversificacion")


def var_montecarlo(pnl, var, k, confianza, horizonte=1):
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
    ax1.set_xlabel(f"P&L {_plazo(horizonte)} (USD)")
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

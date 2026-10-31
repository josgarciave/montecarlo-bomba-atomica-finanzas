# Monte Carlo, de la bomba atómica a las finanzas

Material de la charla sobre el método Monte Carlo, desde su origen en el Proyecto Manhattan hasta sus aplicaciones en riesgo financiero y valoración de opciones.

Por Jose Miguel García Vélez, estudiante de Estadística en la Universidad Nacional de Colombia.

## Contenido

| Notebook | Tema |
|---|---|
| `01_var_cvar.ipynb` | Valor en Riesgo (VaR) y Valor en Riesgo Condicional (CVaR) de un portafolio |
| `02_opciones.ipynb` | Valoración de opciones por simulación |

## Cómo ejecutarlo

```bash
git clone https://github.com/josgarciave/montecarlo-bomba-atomica-finanzas.git
cd montecarlo-bomba-atomica-finanzas
python -m venv .venv
source .venv/bin/activate        # en Windows usar .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook
```

## Estructura

```
notebooks/   notebooks de la charla
figuras/     gráficas exportadas para las diapositivas
```

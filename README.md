# Monte Carlo, de la bomba atómica a las finanzas

Material de la charla sobre el método Monte Carlo, desde su origen en el Proyecto Manhattan hasta sus aplicaciones en riesgo financiero y valoración de opciones.

Por Jose Miguel García Vélez, estudiante de Estadística en la Universidad Nacional de Colombia.

## Contenido

| Notebook | Tema |
|---|---|
| `01_var.ipynb` | Valor en Riesgo (VaR) de un portafolio |
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

## Exportar a HTML

Los notebooks se exportan con la plantilla `aperture`, que les da la misma estética de las diapositivas de la charla. Desde la raíz del repositorio:

```bash
jupyter nbconvert --to html --execute --template aperture --TemplateExporter.extra_template_basedirs=templates --output-dir html notebooks/*.ipynb
```

`--execute` corre cada notebook antes de exportarlo para que el HTML incluya los resultados. En Windows, si `jupyter` no está en el PATH, usar `python -m jupyter nbconvert ...`. Los HTML quedan en `html/`.

## Estructura

```
notebooks/            notebooks de la charla
html/                 notebooks exportados a HTML
templates/aperture/   plantilla de nbconvert con la estética de la charla
figuras/              gráficas exportadas para las diapositivas
```

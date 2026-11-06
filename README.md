# Monte Carlo, de la bomba atómica a las finanzas

Material de la charla sobre el método Monte Carlo, desde su origen en el Proyecto Manhattan hasta sus aplicaciones en riesgo financiero, valoración de opciones y pensiones.

Por Jose Miguel García Vélez, estudiante de Estadística en la Universidad Nacional de Colombia.

## Contenido

| Notebook | Tema |
|---|---|
| `01_var.ipynb` | Valor en Riesgo (VaR) de un portafolio |
| `02_opciones.ipynb` | Valoración de opciones por simulación |
| `03_pensiones.ipynb` | Simulación del ahorro pensional y probabilidad de alcanzar una meta |

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

### Ver los HTML

La estética de la charla solo se ve en el HTML exportado, abierto en el navegador (no dentro de Jupyter ni del editor de VS Code). Para abrir cada notebook:

```bash
# Windows (PowerShell)
start html/01_var.html
start html/02_opciones.html
start html/03_pensiones.html

# macOS
open html/01_var.html

# Linux
xdg-open html/01_var.html
```

Si en Windows los `.html` se abren con otra aplicación (por ejemplo Word), se puede forzar el navegador desde PowerShell:

```powershell
Start-Process chrome (Resolve-Path html/01_var.html).Path
```

O cambiar la aplicación predeterminada en Configuración → Aplicaciones → Aplicaciones predeterminadas → `.html`.


## Estructura

```
notebooks/            notebooks de la charla
notebooks/graficas.py gráficas con la estética de la charla, usadas por los notebooks
html/                 notebooks exportados a HTML
templates/aperture/   plantilla de nbconvert con la estética de la charla
figuras/              gráficas exportadas para las diapositivas
```

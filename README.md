# figure_style

Small matplotlib helpers for making publication and poster panels that drop into Adobe Illustrator at true scale, with editable text and consistent strokes and fonts across every panel.

## Install

```bash
pip install git+https://github.com/aidapiccato/figure-style.git
# or, for local development
git clone https://github.com/aidapiccato/figure-style.git && pip install -e figure-style
```

Requires matplotlib, seaborn and numpy.

## Usage

```python
from pathlib import Path
from figure_style import set_paper_style, new_panel, export_for_illustrator

set_paper_style()                      # once per notebook; or set_poster_style()

FIGURE_DIR = Path('my_figure')
FIGURE_DIR.mkdir(exist_ok=True)

fig, ax = new_panel()                  # 2 x 2 in panel from the active profile
ax.plot([0, 1], [0, 1])
export_for_illustrator(fig, 'my_figure', outdir=str(FIGURE_DIR))
# -> my_figure/paper/my_figure.pdf
```

## What's in it

| Function | What it does |
|---|---|
| `set_paper_style()` / `set_poster_style()` | Set rcParams for the whole notebook: 8 pt vs 20 pt Arial, stroke widths, tick sizes, TrueType font embedding (`pdf.fonttype = 42`) so text stays editable in Illustrator. |
| `new_panel(width_in, height_in, ncols, nrows)` | `plt.subplots` sized from the active profile; `width_in`/`height_in` are per panel. |
| `export_for_illustrator(fig, name, outdir, formats, rasterize_artists)` | Saves a transparent, tightly cropped PDF into `outdir/<profile>/`, so paper and poster versions sit side by side. Optionally rasterizes only dense artists. |
| `extend_log_ticks(ax, values)` / `extend_linear_ticks(ax, values)` | Extend ticks to bracket the data so `sns.despine(trim=True)` doesn't cut the spine short. |

---
name: figure-style
description: Use when creating or editing matplotlib figure-generation notebooks/scripts that should use the figure_style package (set_paper_style/set_poster_style, new_panel, export_for_illustrator) for Illustrator-ready panels — e.g. work under analysis/figures, or any request to "make a figure", "add a panel", "export for Illustrator/paper/poster".
---

# figure-style

Conventions for generating publication/poster figures with the `figure_style`
package (source: `/Users/aidapiccato/figure-style/figure_style/`). The goal
is panels that import into Illustrator at true scale, with editable text and
consistent strokes/fonts across all panels of a paper or poster.

## Standard notebook/script header

```python
from figure_style import set_paper_style, new_panel, export_for_illustrator
# from figure_style import set_poster_style  # use instead for poster/talk figures

set_paper_style()   # call exactly once, before creating any panels

FIGURE_DIR = Path('<figure_name>')   # one subdir per figure, matches notebook name
FIGURE_DIR.mkdir(exist_ok=True)
```

- `set_paper_style()`: 8pt fonts, thin (0.75-1.0pt) strokes, 2x2in default panels.
- `set_poster_style()`: 20pt fonts, thick (1.75-2.5pt) strokes, 6x6in default panels.
- Pick based on where the figure will be used, not habit — never mix styles within one figure/notebook.

## Creating panels

Use `new_panel()` instead of `plt.subplots()` directly — it reads the active
profile's default physical size so strokes/fonts land at the intended scale
after Illustrator placement:

```python
fig, ax = new_panel(width_in=2, height_in=2)          # single axes
fig, axes = new_panel(ncols=2, nrows=1, width_in=2, height_in=2)  # grid; total size scales
```

Only pass `width_in`/`height_in` explicitly when a panel needs to deviate
from the profile default — prefer leaving them unset so panels stay
consistent across the figure set.

## Exporting

```python
export_for_illustrator(fig, '<panel_name>', outdir=str(FIGURE_DIR))
```

- Filename stem (`<panel_name>`) should match the panel's role, e.g. the
  same name as the figure dir for a single-panel figure, or
  `<figure_name>_<subpanel>` / a separate `legend` file for multi-part figures.
- `export_for_illustrator` automatically nests output under a subdirectory
  named after the active style profile (`paper/` or `poster/`) inside
  `outdir`, so `outdir=str(FIGURE_DIR)` with `set_poster_style()` active
  writes to `<FIGURE_DIR>/poster/<panel_name>.pdf`. This lets paper and
  poster exports of the same figure coexist under one `FIGURE_DIR` without
  clobbering each other. It raises if called before `set_paper_style()`/
  `set_poster_style()`.
- Default `formats=("pdf",)` — PDF is primary (better transparency/layering
  in Illustrator). Leave it at the default (pdf-only); don't add `"png"`
  unless the user explicitly asks for a raster preview. Many older notebooks
  under `analysis/figures/<name>/` pass `formats=('pdf', 'png')` — that's
  legacy, not something to replicate in new figure code.
- For panels with thousands of points (dense scatter), pass
  `rasterize_artists=[scatter_artist]` so only that artist rasterizes at
  `raster_dpi` while axes/labels/text stay vector.

## Legends

Prefer a standalone legend figure over an in-panel legend for any figure
with more than one panel sharing the same color/style mapping — put the
legend in every panel and it has to be checked for consistency and
re-exported N times; a separate legend panel is placed once in Illustrator
next to the group it labels.

- Never rely on `sns.histplot`/`sns.scatterplot`'s `legend=True` for the
  figure's actual legend — pass `legend=False` on every panel-producing call
  and build the legend separately, once, from explicit handles matching the
  same palette dict already used for the panels (don't recompute
  colors/labels — reuse the same `PALETTE`/`LABELS` dict).
- Use `mpatches.Patch(color=..., label=...)` for fill/histogram-style
  legends (bars, filled areas) and `plt.Line2D([0], [0], color=..., marker=...,
  linewidth=0, label=...)` for scatter/point-style legends.
- Build the standalone legend the same way as any other panel:

```python
handles = [
    mpatches.Patch(color=PALETTE[key], label=LABELS[key])
    for key in PALETTE
]

fig_leg, ax_leg = new_panel(width_in=1, height_in=1)  # small — just fits the handles
ax_leg.legend(handles=handles, frameon=False, fontsize=7, loc='center')
ax_leg.set_axis_off()

fig_leg.tight_layout()
export_for_illustrator(fig_leg, '<figure_name>_legend', outdir=str(FIGURE_DIR))
plt.show()
```

- Name the exported file `<panel_name>_legend` (or just `legend` when the
  figure has a single panel group), so it sits next to the panel(s) it
  labels in `FIGURE_DIR`.
- If a panel already has a legend for an unrelated purpose (e.g. a fit-line
  annotation), leave that one in place — this convention is about not
  duplicating the *same* color/style mapping across every panel.

## Log-scaled axes

`sns.despine(trim=True)` trims the spine to whatever ticks matplotlib
auto-generated, which on a log axis can end short of the data's actual
min/max and make points look like they fall outside the axis. Call
`extend_log_ticks(ax, values)` before `despine(trim=True)` to set ticks at
every power of ten that fully brackets `values`:

```python
ax.tick_params(axis='x', which='minor', bottom=False)
extend_log_ticks(ax, rec_vals)   # values = the data actually plotted
sns.despine(fig=fig, trim=True, offset=5)
```

Pass `axis='y'` for a log-scaled y-axis.

## Rules

- Never call `plt.rcParams.update(...)` or set fonts/spines manually in
  figure code — that's what `set_paper_style`/`set_poster_style` are for.
  Manual overrides fight the profile and desync panels.
- Never hardcode `figsize=` in `plt.subplots()` for figure panels — use
  `new_panel()` so sizes stay tied to the active profile.
- Don't call `set_paper_style()`/`set_poster_style()` more than once per
  notebook/script, and don't call both — the second call silently replaces
  the first, which is a likely source of subtle inconsistency if noticed
  mid-notebook.
- Keep each figure's outputs in its own `FIGURE_DIR` subdirectory (mkdir with
  `exist_ok=True`), mirroring the pattern already used under
  `analysis/figures/<figure_name>/`.


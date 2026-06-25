# Project Webpage

Static project page for the BRIDGE / DM-UMI paper, intended to be hosted via
GitHub Pages from this directory.

## Local preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

The page pulls Bulma, FontAwesome, Academicons, and MathJax from CDNs; no
build step is required.

## Assets to drop in before publishing

The page references the following files. Some are committed; the rest are
binary hero assets to be added once final.

Already committed:

- `static/images/paper_strip.jpg` &mdash; horizontally-concatenated render of
  every page of the paper (currently 19 pages from `corl26_bridge.pdf`).
  Regenerate after a paper rebuild with Ghostscript + Pillow (ImageMagick is
  not required):
  ```bash
  # render pages, then concatenate at 700px tall, JPEG quality 85
  gs -dBATCH -dNOPAUSE -sDEVICE=png16m -r150 -dTextAlphaBits=4 \
     -dGraphicsAlphaBits=4 -sOutputFile=/tmp/page-%03d.png corl26_bridge.pdf
  python3 - <<'PY'
  import glob; from PIL import Image
  H=700; ims=[Image.open(p).convert('RGB') for p in sorted(glob.glob('/tmp/page-*.png'))]
  ims=[i.resize((round(i.width*H/i.height),H), Image.LANCZOS) for i in ims]
  gap=4; W=sum(i.width for i in ims)+gap*(len(ims)-1)
  s=Image.new('RGB',(W,H),'white'); x=0
  for i in ims: s.paste(i,(x,0)); x+=i.width+gap
  s.save('static/images/paper_strip.jpg','JPEG',quality=85,optimize=True)
  PY
  ```
  Also update the page count in the "Paper" section of `index.html`.
- `static/images/action_validity.png` &mdash; observed-vs-desired action
  validity figure (copy of `corl26_bridge/figures/cmd_obs_delta_figure_side.png`).
- `static/images/pipeline.png` &mdash; dual-mode data collection pipeline,
  rendered from `corl26_bridge/figures/pipeline.pdf` (Ghostscript at 300dpi,
  then auto-trimmed of surrounding whitespace and downscaled to 1800px wide).
- `static/images/model_arch.png` &mdash; BRIDGE model architecture
  (copy of `corl26_bridge/figures/arch.png`).
- `static/images/router_analysis.png` &mdash; router PR curve + t-SNE
  (copy of `corl26_bridge/figures/gate_pr_tsne.png`).
- `static/images/task_pulley.jpg`, `task_pipe.jpg`, `task_battery.jpg` &mdash;
  representative rollout frames for the three tasks (copies from
  `corl26_bridge/figures/{pulley_task,pipe_insertion,battery_insertion}/`).
- `static/videos/teaser.mp4` &mdash; overview video (copy of repo-root
  `video.mp4`), with poster frame `static/images/teaser_poster.jpg`.

The figure sources above live in `corl26_bridge/figures/`; some are rendered
from `.pdf` originals (e.g. `pipeline.pdf`). Re-render/re-copy the PNG/JPG
variants after a paper rebuild if the figures change.

Note: only `index.html`, `README.md`, and `static/` are deployed. The
`corl26_bridge/` LaTeX sources, `corl26_bridge.pdf`, and the repo-root
`video.mp4` are not served.

## Hosting

Point GitHub Pages at `/webpage` on the `main` branch (Settings &rarr; Pages
&rarr; Source: `main` / `/webpage`). The page will then be served from
`https://rai-inst.github.io/umi-dual-mode/`.

## Attribution

The HTML layout is adapted from the
[Nerfies project page](https://github.com/nerfies/nerfies.github.io), used
under a Creative Commons Attribution-ShareAlike 4.0 International License.
The CSS and HTML content authored here are released under the repository's
MIT License (see `../LICENSE`).

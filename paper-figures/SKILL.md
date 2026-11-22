---
name: paper-figures
description: "The user's standing rules for research-paper figures (drawn in HTML, rendered to vector PDF), covering style, how examples are picked and checked, captions, speed, and putting figures into the Overleaf paper. Use it whenever you draw, revise, re-render, pick examples for, caption or push a paper, supplement or proposal figure (teaser, method/pipeline, qualitative comparison, ablation, exploration or architecture figures)."
---

# Paper figures

The user gave these rules while making the figures of a conference paper, most of them more than once. Apply them without waiting to be reminded.

## 1. How a figure is built

- **Format.** Each figure is one HTML file per version. Use an absolute-px canvas (2000–2100 px wide for a `figure*`), real images, an HTML or SVG overlay, and KaTeX for math. No python-pptx or matplotlib block diagrams; the user rejected them.
- **Layout block.** Keep every position and size in a layout block `P` at the top of the script; the page reads `?key=value` overrides. A layout request then becomes a one-line edit.
- **Assets.** Images come from a `build_assets.py` next to the HTML, which reads the runs, crops frames and renders point clouds. Never paste in hand-edited images.
- **Rendering.** `python3 outputs/paper_figures/fig_dev.py FIG.html` writes a 1× PNG to `dev/` in about a second.
  - Options: `--set k=v` tries a value, `--debug` adds a grid with element outlines, `--watch` re-renders on save.
  - `--final` writes a 2× PNG and a vector PDF into the figure's folder, and fails on Type 3 fonts.
  - For text halos use CSS `text-shadow`, never SVG `paint-order: stroke`, which turns into Type 3 fonts.
- **Folders.** Use one folder per figure (`outputs/paper_figures/<n>_<name>/`).
  - The current finals and builders sit at its root; superseded versions go in `old/`.
  - Previews and contact sheets stay in outputs, not the scratchpad.
  - Never delete old versions without asking.

## 2. Style

**Type**
- `figure*` is 6.875 in wide (cvpr.sty `\textwidth`). On a 2000 px canvas the sizes are:
  - smallest text, badge digits included: ≥ 25 px (≈ 6.2 pt);
  - panel titles: 31 px;
  - column and method names: 28 px;
  - tags, box names and notes: 25 px.
- Use one font in every figure: Source Sans 3. For →, ↔ and †, use its latin-ext face or inline SVG.
- All figures share one type scale and the same components. The user checks this ("不同图的字体是统一的吗").

**Colour.** Use few colours ("颜色是不是稍微有点多"). Each colour means the same thing in every figure:
- orange: ours / generated;
- layout gold: #94720f;
- green: memory;
- blue: references;
- slate #33414c: number badges;
- black: text prompts, in every figure.

Further colour rules:
- Symbols such as 𝒫 and 𝒞 do not get their own colours.
- Check line-chart palettes with the dataviz validator.
- Step numbers 1/2/3 use one muted dark colour everywhere: never bright, never a different colour per row. Centre each on its image.
- Arrows are plain black, thin and short, and end at the middle of what they point to. If an arrow needs a detour, drop it.

**Layout**
- Keep it compact and balanced: no large white areas, and no crowded top above an empty bottom. After deleting something, refill the space ("删的太多了反而很空白").
- Size parts by importance:
  - the novel parts (the layout and the VLM planner) are large;
  - the video model is not tiny;
  - the memory is not the biggest element.
  - When the user names a reference paper (e.g. ArtiFixer Fig. 2), copy its proportions.
- Keep the groupings the user approved. Never spread a group to line it up with something else; that only opens gaps. Prefer small edits to the approved version over re-layouts.
- Align rows and columns. Leave a few px at the bottom so no text is clipped, and check that no crop cuts off part of an image.
- Rotate method or row names vertically when horizontal names waste width. Draw no coloured underline under "Ours" or any method name.

**Text inside the figure**
- Keep text short ("字有点多"). Leave out:
  - headers and token names such as `<Video 1>` or `<Picture 2-4>`;
  - "chunk k" labels and scene ids;
  - numbers that don't make the point.
- Name things in place. Add no legend the figure can do without; in particular, no box-colour legend.
- Names follow the paper's current method text. Read `sec/3_method.tex` before naming anything.
- No white text written over images ("图片上加白色写字有点丑"). Put short semi-transparent tags, such as a room name or "N frames later", in the image's top-right corner.
- Capitalise "Inputs". No black frame around the input photo, and no borders on image tiles.

**By figure type**
- **Teaser**
  - Show one integrated scene, or the bands the user picked, with little text. Take layout ideas from other papers' teasers (VMem, WorldCrafter).
  - Use layout + generated-frame pairs, plus an out-and-back pair at the same camera.
  - The input photo must not hide the memory view.
  - Don't emphasise hand edits in the teaser caption.
- **Method / pipeline**
  - Follow the method section step by step.
  - Schematic boxes are fine ("直接用示意框就行，不需要和inference一模一样"), but everything shown must agree: the layout video must match the generated chunk.
  - Put the prefix frame and the text prompt in one background box; draw no other background boxes.
  - Show the point cloud and the boxes in separate panels and keep both ("把点云和box分开" ≠ remove the points).
- **Comparisons**
  - Put the input image and the camera trajectory at the far left, with the cameras of the shown frames bold and numbered.
  - Draw the trajectory as a top view: the path coloured by time on a muted gradient, thin wedges, and no point cloud behind it.
  - Use the same baseline set in every figure (pick it once and keep it).
  - Pick interesting scenes: not standard RE10K-like rooms, never bathrooms. Each scene appears in only one figure.
- **Pills.** Show numbers on tiles only when the user asks.
  - The default pill is the DINOv2 similarity of the two visits.
  - Round it once from the raw score and explain it in the caption.

## 3. Content must hold up ("不然放上去审稿人肯定会骂")

- **Runs.** Show the runs that the tables report, with the same rows and settings (e.g. chunk-by-chunk vs. planned once). Otherwise re-render, or state the difference in the caption.
- **Choosing examples.** Pick cameras and examples by a rule written down before looking.
  - Example rule: the full method is highest among the non-privileged columns; ablation gaps go in the table's direction; the smaller planner is within 0.04; coverage is ≥ 10%.
  - Keep the record (`pick.py` / json) and bring the top alternatives.
- **Boxes.** Every box drawn with a name must hold its object in the frames shown.
  - Check with SAM 3 per box at both visits, plus 2× crops. The score decides, not the eye.
  - If no camera passes, say so and show the best options with their failures.
  - Label only boxes that the planner placed and the frame shows, at most 3 per tile, without overlaps.
- **Inputs.** Keep the inputs (input image, layout, cameras) unless the user says 删/去掉 about them. "不用加X" means "don't add X", not "delete X".
- **Approved content.** Never swap content the user approved. Render the alternative beside it and ask.
- **Captions**
  - Numbers must match the figure: "frames later" = return frame − outbound frame, and the pills match the figure.
  - Check every claim against the scores; drop or soften claims that fail.
  - Describe provenance exactly: hand-added boxes are not "user edits", and annotated layouts are marked as privileged (†).
  - Keep captions short.

## 4. Speed and communication

- Do layout and style edits yourself: edit the HTML, render with fig_dev.py, and show the result within minutes.
  - No multi-agent draft / critique / revise workflows for them ("挪动一下位置不是应该很快完成吗").
  - Use agents or workflows only for data work: searching runs, box audits, generation.
  - If a visual agent is needed, brief one at max effort, on Fable 5.2.
- Show results immediately: the absolute PNG path, plus a before/after sheet when replacing a figure. Don't publish drafts to the shared project page unless asked.
- Say when a figure is done without waiting to be asked ("图画好了吗" means you were late).
- For open choices (camera, scene, variant):
  - ask once, with a recommendation, and put the question on the task board as `waiting`;
  - in the daytime, go ahead with the recommendation after 30 min without a reply;
  - at night, decide yourself.
- If the user says "先给我看一下再推", show the figure before pushing. Otherwise push requested figure and caption updates directly, and report afterwards with the exact caption diff.

## 5. Into the paper (Overleaf)

- Work in a fresh worktree of the clone's `origin/main`, because the clone may hold the user's uncommitted edits. Run `git fetch` and rebase right before pushing.
- To replace a figure PDF, rename the old one (`figures/<name>_before_<tag>.pdf`) unless told to delete it.
- Caption text:
  - wrap new or changed text in `\red{}`;
  - remove `\HT{}` and other review notes once they are addressed;
  - add a `%` provenance comment above the figure: runs, scene, cameras, scores, and what was there before.
- Compile with TeX Live 2026, which breaks pages like Overleaf; an older local TeX Live may not.
  - Order: `pdflatex -output-directory=$B main.tex`, then `bibtex main` inside `$B` with `BIBINPUTS=$W: BSTINPUTS=$W:`, then pdflatex twice.
  - Check the page count, 0 errors and 0 undefined refs.
  - Render the changed pages (`gs -sDEVICE=png16m`) and look for gaps. The usual causes are a section that doesn't fit under a top float, and footnotes.
- The commit message says what changed: the figure, runs, camera and caption. End it with the Co-Authored-By line.

## Project paths

Fill these in per project (keep them out of a public copy of this skill):

- Figures folder, with a `README.md` version table and a `CAPTIONS.md` of caption drafts.
- Style references folder.
- The Overleaf clone.
- The TeX Live 2026 `bin` directory to put on `PATH`.
- The Playwright environment that `fig_dev.py` runs in.

## Checklist before showing a figure

- [ ] Smallest text ≥ 25 px at 2000 px wide; Source Sans 3 only; no Type 3 fonts in the PDF.
- [ ] Colours follow the shared code; prompts are black; badges use one dark colour.
- [ ] No empty areas, clipped text or cut-off images; rows and columns aligned.
- [ ] Inputs present; names match the paper text.
- [ ] Runs match the tables; the example was picked by a written rule, and the alternatives are at hand.
- [ ] Every named box passes SAM 3 at both visits, or the failure is reported.
- [ ] Caption numbers and claims match the figure.
- [ ] Old version kept; before/after sheet made.

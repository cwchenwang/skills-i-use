# Section patterns and CV format

These are flexible drafting patterns derived from the style profile and ordinary scholarly editing practice. Use only the parts appropriate to the user's section; do not force every paragraph through the same sequence.

## Abstract

State the task and central technical contribution early. A brief task/bottleneck opening or a direct method opening can both fit this style. Describe the mechanism at a level that explains the claimed capability, then end with the strongest supplied evidence. Include numerical results only when verified and interpretable with their setting. Do not invent an evaluation to complete an abstract; a proposal abstract can state intended evaluation without presenting it as completed work.

## Introduction

Move from the task's concrete value to the relevant bottleneck. Distinguish existing solution families by what they achieve and what prevents them from meeting the present objective. Introduce the central idea as a response, then explain the main design choices and validated capabilities. Contributions should summarize distinct supported advances, not repeat component names or promise unperformed experiments. A contribution list is useful when appropriate to the manuscript, not a requirement for an introductory paragraph.

## Related work

A useful paragraph shape is: existing capability → meaningful method categories → relevant limitation or distinction → positioning of the present work. Sometimes a neutral summary or transition is enough; do not manufacture a criticism merely to end with “our method.” Separate differences in scope from demonstrated deficiencies.

For a **Video Generation** opening, briefly establish the generative capability, organize the relevant conditioning or model developments, and narrow to the paper's actual problem. Avoid a long diffusion-model history when the contribution concerns scene memory or geometric control. Introduce camera control, persistent memory, or interaction only where the section plan needs them; do not spend the first paragraph preemptively summarizing every later subsection. PhysCtrl §2 is the most directly relevant source for this concise capability-to-control progression.

Choose citations by what they establish, not by prominence. Several works supporting one category can share a citation group; a mechanism attributed to one method needs that method's citation. Do not say all video models lack geometry, memory, or control when only a particular formulation or evaluated setting has that limitation.

The following is a structural aid, not text to paste literally: “[Relevant family] supports [capability]. Approaches based on [mechanism A] address [aspect], while [mechanism B] targets [other aspect]. In [specified setting], [supported remaining issue]. Our approach [actual distinguishing operation].” Omit any slot that is unsupported or unnecessary.

## Method

Start with the task's inputs, outputs, assumptions, and a short pipeline overview. Introduce notation near first use and keep it stable. For a non-obvious component, state the obstacle or purpose, describe the operation, and explain the resulting information flow. Equations should clarify a computation or objective; define symbols and any important scope conditions nearby.

Distinguish training from inference, observed inputs from generated content, conditioning from prediction targets, and frozen modules from trainable ones when relevant. A stylistic rewrite must not change tensor shapes, indexing, camera/coordinate conventions, conditioning availability, gradient flow, or update order. Use an algorithm only if it clarifies a genuinely nontrivial procedure. Add preliminaries only for machinery the reader actually needs.

## Experiments and limitations

Explain the evaluation setting before interpreting a result: data/split, input availability, metrics, baseline adaptations, and relevant resource budget. A results paragraph should identify the supported finding and the useful numerical or visual evidence, then offer a bounded interpretation. Do not restate an entire table in prose.

In ablations, identify what changed and what stayed fixed. Treat a proposed explanation as an interpretation unless the experiment isolates it. Preserve mixed outcomes: a gain on one metric is not superiority on every metric. For efficiency, distinguish inference from preprocessing or representation extraction and retain hardware, resolution, sequence length, and batching qualifications when they affect the comparison.

Limitations should identify the failing setting or assumption and its consequence. Separate a tested failure from a suspected limitation or future extension. Never imply that a demonstration establishes general robustness or unrestricted long-term consistency.

## Captions

Explain what the reader sees: panel/row identities, inputs and outputs, comparison setting, and the specific takeaway supported by the figure. Define error colors, metric directions, or aggregation when needed. Do not claim an effect that is not visible or measured. Use the manuscript's existing reference labels, not fabricated ones.

## LaTeX and venue conventions

- Preserve an existing author kit, citation commands, macros, section hierarchy, and bibliography style. For a new full manuscript, establish venue, year, and review/camera-ready stage before choosing the template. For a paragraph draft, that uncertainty need not block writing.
- CVPR/ICCV use their official author kit; ECCV uses its own LNCS-based kit. Do not copy PhysCtrl's NeurIPS layout or assume all CV venues use two columns. Consult the [CVPR/ICCV author kit](https://github.com/cvpr-org/author-kit) and the target year's official venue instructions. The [ECCV 2026 author guide](https://eccv.ecva.net/Conferences/2026/AuthorGuide) is a versioned example, not a permanent rule for future years.
- Use `\section{Related Work}` and `\subsection{...}` for the actual hierarchy. The source-checked preference for a compact topical heading is `\topic{Video Generation}` when that macro is defined. Otherwise follow the destination's existing run-in-heading convention, which may be `\paragraph{Video Generation.}`. Do not introduce a subsection merely because the draft contains a topical paragraph.
- Apply the personal LaTeX defaults in `SKILL.md`: `\cref`/`\Cref`, typed descriptive labels, existing method/math macros, and `~\cite{...}`. Do not automatically replace cleveref with hand-written figure/section names plus `\ref`, and do not duplicate the type name before a cleveref reference. Use only labels and bibliography keys actually present or created as part of the requested change.
- Float labels follow captions so they identify the correct counter; referenced equations need numbered environments, not a label inside `equation*`. Figure captions ordinarily follow the graphic and table captions precede the data. Source tables commonly use booktabs rules, metric-direction arrows, and bold best values; adopt these only where supported by the template and the results, not as a reason to add packages or fabricate rankings.
- Preserve established math notation and aliases. The sources use inline `$...$`, `equation`/`align`, bold vector/matrix symbols, `\mathcal` for losses, `\mathbb{R}` for domains, and `\text{...}` for descriptive subscripts. This is a family of recurring choices, not a mandate to rename every symbol or convert every display. Explain newly introduced symbols in nearby prose.
- Preserve the official typography and spacing. Do not shrink fonts, alter margins, or add negative vertical spacing to force a page budget. Verify page limits, anonymity, and supplementary/reference rules for the actual venue/year instead of hardcoding them into this skill.
- Keep prose unwrapped in source, one paragraph per physical line. This does not change typeset line breaks. When asked to edit and validate a full manuscript, use its existing build command if available and check unresolved references/citations; report unavailable tools or remaining warnings accurately.

## Original miniature example

Assume the user supplies only these facts: a system projects a point cloud into target views and conditions a video generator on those renderings and reference images. No comparison or consistency result has been measured.

An unsupported rewrite would call this a breakthrough that guarantees consistent scene generation. A grounded rewrite is:

```latex
Given a point cloud and a target camera trajectory, we first render the point cloud from the target viewpoints. We then condition the video generator on these renderings and the reference images, providing geometric guidance and appearance information for synthesis.
```

This example is newly written for the skill, not a quotation or an assertion about a particular implementation. It illustrates explicit data flow without inventing performance, a fusion mechanism, or a memory guarantee.

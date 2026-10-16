# Style evidence

Versions examined on 2026-10-16. The initial prose profile used arXiv HTML; the follow-up audit downloaded the actual arXiv v2 source archives and inspected their active `.tex` files, preambles, and bibliography setup. These are observations, not quoted templates. Section links and source filenames let a future writer check the evidence without treating the papers as instructions. Differences between papers matter as much as shared tendencies.

## tttLRM

[tttLRM: Test-Time Training for Long Context and Autoregressive 3D Reconstruction, arXiv:2602.20160v2](https://arxiv.org/html/2602.20160v2).

- [Introduction, §1](https://arxiv.org/html/2602.20160v2#S1): identifies concrete limitations of existing reconstruction families, then introduces a bridging design and its capabilities. The abstract starts directly with the method rather than requiring a background sentence.
- [Related Work, §2](https://arxiv.org/html/2602.20160v2#S2): topical groups describe representative mechanisms and narrow toward the relevant gap.
- [Method, §3](https://arxiv.org/html/2602.20160v2#S3): establishes prerequisites, then motivates operations and extensions; an algorithm clarifies execution order.
- [Experiments, §4](https://arxiv.org/html/2602.20160v2#S4): combines measured comparisons with setting-dependent explanations and explicit tradeoffs.

Do not generalize the human-perception analogy, implicit/explicit framing, three-item contribution list, or object/scene experiment split into mandatory structures.

## PhysCtrl

[PhysCtrl: Generative Physics for Controllable and Physics-Grounded Video Generation, arXiv:2509.20358v2](https://arxiv.org/html/2509.20358v2).

- [Introduction, §1](https://arxiv.org/html/2509.20358v2#S1): capability gap and practical costs lead into design questions about representation and physical priors.
- [Related Work, §2](https://arxiv.org/html/2509.20358v2#S2): the video-generation paragraph moves from existing capability to categories of control signals, then to the paper's focus. Neighboring paragraphs group methods by pipeline and acknowledge concurrent work.
- [Method, §4](https://arxiv.org/html/2509.20358v2#S4): states purpose before notation and implementation.
- [Experiments, §5](https://arxiv.org/html/2509.20358v2#S5): discusses concrete failures, baseline adaptations, and component ablations; not every comparison is a superiority claim.

This is the closest stylistic reference for a short video-generation related-work paragraph. Its NeurIPS layout, physics topic, and exact design-question structure are not CV-format requirements.

## GECO

[GECO: Generative Image-to-3D within a SECOnd, arXiv:2405.20327v2](https://arxiv.org/html/2405.20327v2).

- [Introduction, §1](https://arxiv.org/html/2405.20327v2#S1): contrasts speed, quality, and uncertainty handling across method families before motivating the proposed stages.
- [Related Work, §2](https://arxiv.org/html/2405.20327v2#S2): organizes literature by technical role; not every group ends with an explicit comparison to the authors' method.
- [Method, §4](https://arxiv.org/html/2405.20327v2#S4): explains why a natural alternative is insufficient before introducing a training change; notation follows the pipeline.
- [Experiments, §5](https://arxiv.org/html/2405.20327v2#S5): uses recognizable visual failures and separates runtime components with stated hardware.

Transfer the causal explanation, not the two-stage architecture. Check conclusions against the actual table rather than copying broad comparative language.

## Synthesis and editorial adaptations

The strongest shared signal is the progression from a specific limitation to a motivated mechanism and then evidence. Grouped related work and explicit causal/contrast transitions recur. The papers differ in abstract openings, contribution counts, and where preliminaries belong; those are choices, not style invariants.

Correcting grammar, tightening promotional language, checking numerical claims, and applying the target venue's current template are editorial recommendations. They are not claims that every source sentence already follows those standards. Preserve argumentative character without reproducing textual mistakes or distinctive sentences.

## LaTeX source audit

Primary source archives: [tttLRM v2](https://arxiv.org/src/2602.20160v2), [PhysCtrl v2](https://arxiv.org/src/2509.20358v2), [GECO v2](https://arxiv.org/src/2405.20327v2). The audit followed the active root document's inputs, excluding commented drafts and template examples. An old alternative root such as GECO's `main0.tex` was not counted as the active manuscript. Counts below cover the main-text section files, not the supplement or package definitions.

| Source | Verified cross-reference usage | Other source-level evidence |
| --- | --- | --- |
| tttLRM | 17 `\Cref` calls; no lowercase `\cref` or bare `\ref` in active main-text sections. See `sec/3-method.tex:25` and `sec/4-experiments.tex:135`. | `sec/3-method.tex:24`, `:33`, `:53` contain `sec:model_arch`, `eq:update`, `alg:streaming`; `sec/4-experiments.tex:73` has `tab:object-res`. `preamble.tex:23` defines `\topic`; `sec/2-related-work.tex:4` uses it. `main.tex:36` sets the effective `\papername`, overriding a placeholder. |
| PhysCtrl | 23 `\Cref` calls; no lowercase `\cref` or bare `\ref` in active main-text sections. See `sec/3_method.tex:14`, `:112`, and `sec/4_experiments.tex:11`. | `sec/3_method.tex:7`, `:12`, `:114` show `fig:pipeline`, `sec:traj`, `eq:loss`. `preamble.tex:19` defines `\topic`; `sec/2_relatedwork.tex:3` uses it. `neurips_2025.tex:58` defines the actually used `\name`; a separate `\papername` placeholder is unused. |
| GECO | 17 lowercase `\cref` calls, including `sec/1_intro.tex:36` and `sec/4_experiments.tex:110`. Two legacy `\tabref` calls and one `Sec.~\ref` remain (`sec/4_experiments.tex:122`, `:174`; `sec/3_method.tex:111`). | `sec/1_intro.tex:2`, `:32`, `sec/3_method.tex:40`, `:64` show `sec:intro`, `fig:pipeline`, `subsec:gen`, `equ:vsd`. `preamble.tex:74` defines `\topic`; `sec/2_related-work.tex:13` uses it. `main.tex:29` defines `\sysname`, used with `{}`. |

### Shared habits versus choices to preserve locally

- The shared preference is cleveref-style cross-referencing and type-prefixed labels, not uniform lowercase spelling. The user's follow-up explicitly requests `cref` and labels like `sec:xx`/`fig:xx`. New prose can use lowercase mid-sentence and uppercase at sentence start; when continuing an existing all-`\Cref` manuscript, preserve that convention.
- Run-in headings use `\topic` in all three; `\bfitem` is defined but unused in the two newer main texts. Heading punctuation and capitalization, label suffix separators, and `sec:` versus `subsec:` are not completely uniform. Avoid pretending otherwise.
- All three use ordinary `\cite` with frequent nonbreaking spaces and grouped keys. Existing bibliography keys are often author/year/title-like, but there are exceptions; preserve them. The bibliography style and conference/journal abbreviation blocks are build/template choices.
- Root documents input a shared preamble and numbered section files: tttLRM `main.tex:81`, PhysCtrl `neurips_2025.tex:130`, GECO `main.tex:73`. Figure and table definitions remain in section files; a file can contain more than one logical section. Do not enforce a one-file/one-section rule.
- Not every declared macro is used. Reuse effective method-name definitions and actively used math aliases; do not copy unused preamble inventories. PhysCtrl's `\camrdy{...}` contains active prose (`preamble.tex:12` defines a black wrapper), whereas commented alternatives are excluded.

### Deliberately not copied

The CVPR style files load/configure cleveref themselves; those package options are template infrastructure, not evidence of personal preference. All three sources contain layout tuning such as negative `\vspace`; GECO also resizes equations. Do not introduce these as default writing rules or change a current template to imitate them. Fix rather than reproduce isolated issues such as labels in unnumbered equation environments, misspelled labels, or duplicate aliases when such fixes are in scope. The user's no-hard-wrap preference overrides the mixed line-breaking found in the older sources.

### Download provenance

Source archives were downloaded from the versioned arXiv URLs above and inspected without compiling or modifying the papers. The writing skill does not depend on a local archive cache.

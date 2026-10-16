---
name: chenwang-cv-paper-writing
description: Draft, revise, or review computer-vision research manuscripts in the writing style reflected in Chen Wang's tttLRM, PhysCtrl, and GECO papers. Use for paper paragraphs, abstracts, introductions, related work, methods, experiments, captions, and LaTeX manuscript polishing, with venue-appropriate CVPR/ICCV/ECCV conventions. Not a general-purpose chat, documentation, or slide-writing style.
---

# Chen Wang CV Paper Writing

Write direct, technically specific English research prose. Preserve the recurring argumentative and LaTeX-source habits of the three reference papers, not their exact sentences, occasional errors, or paper-specific claims. This profile was checked against the actual arXiv v2 `.tex` sources, not just rendered papers. It is a sample-derived profile of coauthored papers, not a claim that every sentence reflects one author's individual preference.

## Establish the writing task

- Respect the requested section, length, language, and output format. For a Chinese request, default to English manuscript text and Chinese editorial notes outside it. A request for one paragraph should receive one paragraph, not a new paper outline.
- Read the supplied draft and relevant adjacent paragraphs; when editing a manuscript repository, inspect its notation, macros, bibliography, and template before changing files. A request to draft in chat does not authorize repository edits.
- Identify the available facts: task, inputs/outputs, actual mechanisms, evidence, and allowed comparisons. Preserve numerical values, uncertainty, mathematical meaning, and experimental conditions. Ask only when missing information prevents a meaningful draft; otherwise write the supported portion and briefly identify unresolved facts outside the manuscript.
- Read [section-patterns.md](references/section-patterns.md) when drafting a section or changing manuscript formatting. For a small wording edit, the core style below is sufficient. Read [style-evidence.md](references/style-evidence.md) when explaining the style, checking fidelity to a particular source, or adapting a pattern not covered here. The evidence notes avoid needing to reread all three papers for every paragraph.

## Core voice and reasoning

1. **Make the technical tension concrete.** Move quickly from the task to the relevant limitation: what information is missing, what operation is expensive, or what assumption fails. Broad significance statements should earn their space.
2. **Make design choices answer that tension.** Explain why the representation, conditioning, architecture, or objective is needed before detailing its implementation. Prefer a causal argument over a component inventory.
3. **Describe mechanisms with stable terminology.** Use precise subjects and verbs: what is encoded, predicted, conditioned on, reconstructed, or updated. Keep a technical term consistent instead of rotating through synonyms. Use “we” naturally for the authors' choices, without beginning every sentence identically.
4. **Compare families before enumerating papers.** Organize related work around representations, supervision, conditioning, computation, or another relevant distinction. Recognize existing capabilities before explaining a scoped limitation or the present work's difference.
5. **Attach interpretation to evidence.** Report the observed result and its evaluation setting before explaining what it suggests. Name a visible failure or measured tradeoff instead of merely saying the output is better. Do not turn a plausible mechanism into a demonstrated causal result.

Use transitions such as “However,” “Specifically,” and “In contrast” when the logic requires them; do not insert them mechanically. Prefer a readable mixture of short claims and longer explanatory sentences. Replace vague promotion with the concrete operation or outcome. There is no mandatory vocabulary blacklist, paragraph length, number of contributions, or fixed abstract opening.

## Evidence and citation discipline

- These papers are style references, not a permanent literature survey. Do not import their old novelty claims, baseline limitations, or citations into a new topic without checking relevance. Do not automatically cite the three papers in every new draft.
- Reuse existing, verified BibTeX keys. When adding literature or checking a comparative claim, inspect the primary paper or official project source and verify that it supports the sentence. Cite a named method immediately or group citations beside the supported category claim.
- Do not invent references, bibliography keys presented as real, experiments, metrics, architectural details, or citations to figures/tables that do not exist. For an incomplete draft, a visible `[citation needed]` or LaTeX comment is preferable to a fictitious `\cite{...}`; disclose unresolved items. Respect a user's request for a citation-free draft.
- Claims such as “first,” “state of the art,” universal superiority, or guaranteed consistency need appropriate evidence. If unsupported, state the actual capability instead. Do not strengthen a conclusion merely to imitate confident wording in the source papers.
- Do not transfer topic-specific content: physics simulation, test-time training, and two-stage distillation are not obligatory ingredients of a new manuscript. An interface or an agent workflow is not itself evidence of a research contribution.

## CV manuscript delivery

### Personal LaTeX defaults

- **Cross-references:** prefer the `cleveref` family, e.g. `\cref{fig:pipeline}` and `\Cref{sec:method}`, over hand-written `Fig.~\ref{...}` or numbered references. Follow the current manuscript's casing: tttLRM and PhysCtrl use `\Cref` even mid-sentence; GECO predominantly uses `\cref` with some legacy wrappers. For new prose without an established convention, use `\cref` mid-sentence and `\Cref` at sentence start. Do not write `Fig.~\cref{...}`, which duplicates the object name.
- **Labels:** use typed, descriptive identifiers such as `sec:method`, `fig:pipeline`, `tab:ablation`, `eq:loss`, and `alg:streaming`. Preserve existing identifiers, including `subsec:` or `equ:` and their hyphen/underscore choices; do not rename them during prose polishing. Put a new section label after its heading, a float label after its caption, and a referenced equation label inside a numbered environment. Refer only to real targets; create a label only when also creating its target or when that target already exists.
- **Compact headings:** all three papers actively use `\topic{...}` for run-in headings, especially related-work categories and experiment topics. Prefer that macro when defined, instead of automatically replacing it with `\paragraph` or a new subsection. Use short topical phrases, normally without a trailing period, while matching nearby headings. If unavailable, follow the destination's heading convention rather than emitting an undefined macro or copying a preamble wholesale.
- **Macro reuse:** retain the actual method-name macro (`\papername`, `\name`, or `\sysname{}` in the reference papers) and existing mathematical aliases such as `\bx` or `\bP`. Check the effective definitions and spacing behavior. A macro merely declared in a preamble is not evidence that it should be used everywhere; do not introduce these particular names into an unrelated manuscript automatically.
- **Citations:** the recurring source form is `MethodName~\cite{key}` and grouped `~\cite{key1,key2}`. Reuse the destination bibliography keys and citation style; do not switch to `\citep`/`\citet` without a reason or turn an old key's spelling into a universal naming rule.
- **Source organization:** the papers separate a root document, `preamble.tex`, numbered `sec/` inputs, `figures/`, and `main.bib`. Continue the current project's structure and filenames; do not reorganize it just to match one reference paper. Ignore commented drafts, unused macros, and template instructions when inferring author habits, while retaining active text inside revision wrappers.

These defaults reflect the [source audit](references/style-evidence.md#latex-source-audit); venue package settings, spacing hacks, and inconsistent legacy labels are not personal style requirements. If `cleveref` is unavailable and preamble edits are out of scope, use the supported explicit type plus `\ref` as a compatibility fallback and briefly explain why. Do not silently emit undefined macros or modify dependencies/template settings to satisfy a stylistic preference.

For a new paste-ready paper passage, use LaTeX when requested or when the destination is a LaTeX manuscript; otherwise return clean prose. Do not wrap a paragraph in a complete document. Keep each prose paragraph on one physical source line, with blank lines between paragraphs; this is the user's explicit auto-wrap preference, not a claim that all historical sources follow it. Display equations and environments may occupy multiple lines.

Use the official template for the specified venue, year, and submission stage. CVPR/ICCV and ECCV do not share the same layout. When no venue is specified, use CVPR/ICCV-style section organization and concise academic prose, but do not silently choose page limits or alter a template. See the formatting guidance in [section-patterns.md](references/section-patterns.md).

Before delivery, check that the paragraph has one clear role, each comparison has support, mechanisms and numerical facts are unchanged, and citations/labels resolve when a complete manuscript is available. Return the requested text first. Add only necessary editorial notes, especially missing evidence or meaningful changes in claim strength. Do not claim a LaTeX compilation or bibliography check unless it was actually performed.

# .agents/skills

Reviewed, reusable skills for agents working in this project.

Skills are mature operating knowledge, not raw notes. Agents may propose a skill
from a retrospective, but should not promote one without explicit review or a
clear project convention that allows it.

Skills may come from this kit's curated `.agents/skills/` catalog or from reviewed
external candidates copied under `external/`.

Use `registry.toml` to decide which skill fits a role, workflow, or trigger.

## Layout

```text
common/
workflows/
graphics/
research/
review/
```

Each skill still lives in a directory with `SKILL.md`; grouping directories help
agents find skills by role or workflow instead of scanning a flat list.

## Core Skill

| Skill | Purpose |
|---|---|
| `common/improve-this-kit/` | Collect feedback and propose review-gated improvements to this kit. |
| `research/baseline-selector/` | Select reproducible, reviewer-aware experimental baselines for research projects. |
| `graphics/xiaobei-skill-image-to-vba/` | Convert academic images and screenshots into editable Office VBA Shapes and PowerPoint reconstructions. |
| `graphics/paper-framework-figure-studio-pro/` | Co-design publication-ready paper framework figures and method overview diagrams. |
| `graphics/image-to-editable-ppt/` | Convert slide images, PDFs, and image-based PPTX files into editable PowerPoint decks. |
| `graphics/visiomaster/` | Rebuild flowcharts, architecture diagrams, and paper module figures as editable Visio `.vsdx`. |

Curated skills installed from this kit keep their catalog grouping, such
as `graphics/`, `research/`, `review/`, and `workflows/`.

## Graphics Skill Routing

Use the narrowest graphics skill that matches the requested output:

- Use `graphics/paper-framework-figure-studio-pro/` when the user wants to design or explore a new publication framework figure, method overview, architecture diagram, or pipeline figure for a paper. This is a human-in-the-loop figure co-design workflow, not a general PPT converter.
- Use `graphics/image-to-editable-ppt/` when the user provides slide images, PDFs, or image-based PPTX files and wants an editable PowerPoint `.pptx`. This is the default choice for full-deck or multi-page editable PPT reconstruction.
- Use `graphics/xiaobei-skill-image-to-vba/` for lighter image-to-Office reconstruction, especially single academic figures, screenshots, or diagrams that should become editable Office/VBA shapes.
- Use `graphics/visiomaster/` only when the desired output is editable Visio `.vsdx` or the source is a structured flowchart, architecture diagram, or paper module figure that should be rebuilt with Visio shapes. It expects Windows plus Microsoft Visio for final rendering.

If a request only says "make this editable PPT", prefer `image-to-editable-ppt`.
If it says "make this into Visio" or `.vsdx`, prefer `visiomaster`.
If it says "help me design the paper's framework figure", prefer
`paper-framework-figure-studio-pro`.

## Included External Skills

- `graphics/xiaobei-skill-image-to-vba/` includes material from [xiao24bei/xiaobei-skill-image-to-vba](https://github.com/xiao24bei/xiaobei-skill-image-to-vba) under the Apache-2.0 License; its `LICENSE` and `NOTICE` files are preserved in that directory.
- `graphics/paper-framework-figure-studio-pro/` includes material from [c-narcissus/paper-framework-figure-studio-pro](https://github.com/c-narcissus/paper-framework-figure-studio-pro) under the MIT No Attribution License; its license file is preserved in that directory.
- `graphics/image-to-editable-ppt/` includes material from [ningzimu/image-to-editable-ppt-skill](https://github.com/ningzimu/image-to-editable-ppt-skill) under the MIT License; its license file is preserved in that directory.
- `graphics/visiomaster/` includes material from [Rss3208/Visiomaster](https://github.com/Rss3208/Visiomaster) under the MIT License; its license file is preserved in that directory.
- `research/research-paper-writing/` includes material from [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) under the MIT License; its license file is preserved in that directory.
- `research/baseline-selector/` includes material from [RyanZhou168/baseline-selector](https://github.com/RyanZhou168/baseline-selector) under the MIT License; its license file is preserved in that directory.

## Promotion Criteria

- The lesson is likely to apply again.
- The trigger condition is clear.
- The steps are specific and verifiable.
- The skill is concise enough to be worth loading into context.

Use `.agents/templates/skill.md` when creating a new skill.

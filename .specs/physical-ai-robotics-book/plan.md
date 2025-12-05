<!--
Sync Impact Report:
- Version change: N/A
- Modified sections: All sections filled from template.
- Added sections:
    - Architecture Sketch (Integrated into Summary and Project Structure)
    - Section Structure (Integrated into Project Structure)
    - Research Approach (New Section)
    - Quality Validation (New Section)
    - Decisions Needing Documentation (New Section)
    - Testing Strategy (New Section)
    - Execution Phases (New Section)
- Removed sections: N/A
- Templates requiring updates:
    - .specify/templates/plan-template.md (✅ updated by previous constitution command for Constitution Check section)
    - .specify/templates/spec-template.md (✅ reviewed, no changes needed for template)
    - .specify/templates/tasks-template.md (✅ reviewed, no changes needed for template)
- Follow-up TODOs: N/A
-->
# Implementation Plan: Physical AI & Humanoid Robotics Book

**Branch**: `feat/physical-ai-robotics-book-plan` | **Date**: 2025-12-04 | **Spec**: .specs/physical-ai-robotics-book-spec.md
**Input**: Feature specification from `/specs/physical-ai-robotics-book-spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Establish the writing architecture, section structure, research flow, and validation strategy for the Physical AI & Humanoid Robotics book. This plan converts requirements from /sp.constitution and /sp.specify into a concrete implementation roadmap, including the core book architecture (4 modules), deployment architecture (Docusaurus, GitHub Pages, Vercel, PDF export), section structure, research methodology, and quality validation.

## Technical Context

**Language/Version**: Not applicable for book writing platform; book content will include Python 3.x for ROS 2 conceptual examples.
**Primary Dependencies**: Docusaurus v3, GitHub Pages, Vercel.
**Storage**: Markdown files (`.md`), `sidebars.js`.
**Testing**: Docusaurus build process, internal link validation, APA citation format validation, plagiarism check (manual/external tool), word count.
**Target Platform**: Web (static site via Docusaurus), PDF export.
**Project Type**: Technical Documentation/Book.
**Performance Goals**: Efficient Docusaurus build times, responsive deployed site.
**Constraints**: 5,000–7,000 words total, APA 7th edition citation style, minimum 15 sources (>=50% peer-reviewed robotics/AI journal articles), publish on GitHub Pages and Vercel within 2 weeks.
**Scale/Scope**: Four main book modules covering ROS 2, Digital Twin Simulation, NVIDIA Isaac, and Vision-Language-Action robotics.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Technical Accuracy & Clarity**: All technical details must be accurate and clearly explained for a computer science audience.
- [x] **Research & Citation Integrity**: Research must adhere to APA style, with >=50% peer-reviewed sources and 0% plagiarism.
- [x] **Content Scope & Length**: Plan must align with the book modules and target 5,000–7,000 words.
- [x] **Docusaurus & Output Format**: Plan must ensure output aligns with Docusaurus v3 Markdown and sidebars.js navigation.
- [x] **Deployment & Hosting**: Plan must consider GitHub Pages and Vercel deployment configurations.

## Project Structure

### Documentation (this feature)

```text
specs/physical-ai-robotics-book/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (research notes for /speckit.plan command)
├── data-model.md        # N/A for book content, conceptual only
├── quickstart.md        # N/A for book content
├── contracts/           # N/A for book content
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
docs/                   # Docusaurus Markdown chapters
├── introduction/       # What is Physical AI? Why humanoids?
├── ros2-fundamentals/  # Module 1
├── digital-twin-sim/   # Module 2
├── nvidia-isaac/       # Module 3
├── vla-humanoids/      # Module 4
├── appendices/         # Glossary, APA Reference List, Deployment Instructions
└── capstone-overview/  # Capstone system overview
sidebars.js             # Docusaurus navigation configuration
```

**Structure Decision**: The project structure will follow Docusaurus documentation site conventions, with Markdown files organized into modules within the `/docs` directory. `sidebars.js` will manage navigation. The `data-model.md`, `quickstart.md`, and `contracts/` from the template are marked N/A as they do not apply to the direct content of a technical book. Traditional `src/` and `tests/` directories are not directly applicable to the book's content, but a Docusaurus project will have its own build and configuration files at the root.

## Research Approach

**Method**: Use a research-concurrent writing approach — research while writing each module instead of gathering all sources beforehand.

**Sources**:
- IEEE, ICRA, IROS proceedings
- NVIDIA developer documentation
- ROS 2 technical documentation
- Peer-reviewed embodied AI research (last 10 years)

**Citation Style**: APA 7th edition, in-text citations + comprehensive reference list.

**Research Sequence**: Research → Write summary → Insert citations → Validate facts → Move to next section.

## Quality Validation

**Validation Rules**:
- Every factual claim must include a traceable APA citation.
- Minimum 15 sources total, with at least 50% peer-reviewed robotics research.
- Plagiarism score must be 0% prior to final export/publish.

**Automated Validation Checkpoints**:
- Citation presence check (per chapter/section).
- Broken internal link check (within Docusaurus site).
- Docusaurus build pass (`npm run build`).
- GitHub Pages site render test (manual verification initially, then automated).
- Vercel deployment preview (automated on commit).

## Decisions Needing Documentation

| Decision                     | Options                                       | Tradeoffs                                                              | Chosen Decision & Justification                                        |
|------------------------------|-----------------------------------------------|------------------------------------------------------------------------|------------------------------------------------------------------------|
| Simulation platform focus    | Gazebo vs. Unity vs. Isaac Sim                | Specialization vs. comprehensive coverage                               | Keep all 3, but emphasize Isaac for modern robotics training (aligns with current industry trends and project goals). |
| Language examples            | Full code vs. conceptual pseudocode           | Practicality/verbosity vs. clarity/focus on concepts                 | Conceptual only; no full programming tutorials (aligns with book's purpose as an overview, not a coding guide). |
| Deployment                   | Single hosting vs. dual hosting               | Simplicity vs. redundancy/preview capabilities                         | Dual (GitHub Pages + Vercel) for redundancy and enabling preview builds for review.
| Scope boundaries             | Include hardware construction?                | Comprehensive hardware/software vs. focused software/simulation       | Exclude hardware construction; maintain software/simulation focus (aligns with project goal of a technical book, not a DIY guide). |

## Testing Strategy

**Validation checks based on acceptance criteria**:
- ✔ **Build test**: `npm run build` must pass with zero errors.
- ✔ **Internal link test**: No broken Markdown links within the Docusaurus site.
- ✔ **Citation test**: Every chapter contains at least 3 APA references (as a guideline, actual check is global for 15+ sources).
- ✔ **Word count test**: 5,000–7,000 words total.
- ✔ **Publishing test**: GitHub Pages site publicly reachable and rendering correctly.
- ✔ **Deployment preview**: Vercel preview deployed successfully on commit.

## Execution Phases

1.  **Phase 1 — Research**: Collect key sources on Physical AI, ROS 2, Gazebo, Isaac. This will be an ongoing, concurrent process with writing.
2.  **Phase 2 — Foundation**: Outline chapters and create the initial Docusaurus site structure within the `/docs` directory and configure `sidebars.js`.
3.  **Phase 3 — Analysis & Writing**: Write technical explanations for each module, concurrently performing research, and insert APA-style citations.
4.  **Phase 4 — Synthesis & Deployment**: Combine all modules, ensure consistency, generate the final PDF (if Docusaurus supports it or via external tools), and deploy to GitHub Pages + Vercel.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A
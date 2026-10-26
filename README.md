# AI Documentary Production Studio

**Research-driven documentaries. Evidence-backed storytelling. Human-controlled production.**

> **Project status:** Requirements definition and architecture planning. This README describes the intended product and planned capabilities; it does not imply that the application has already been implemented.

## 1. Overview

AI Documentary Production Studio is a personal, AI-assisted web application for developing researched, cinematic documentary packages from a topic selected by the user.

The system brings research, source verification, narrative development, scriptwriting, visual planning, narration preparation, English captions, Bangla subtitles, editing instructions, quality assurance, and export into one approval-driven workflow.

Its core principle is:

**AI accelerates production; evidence supports important claims; the user retains control.**

The initial deployment target is a self-hosted application running locally with Docker Compose. The architecture should support secure remote access when needed and provide a documented path to future cloud deployment.

## 2. Goals

- Turn a selected topic into a complete documentary production package for a film of approximately **5–15 minutes**.
- Ground important factual claims in traceable evidence.
- Synthesize five approved books with relevant primary sources and supplementary scholarship.
- Preserve transparency around uncertainty, disagreement, source limitations, and AI-generated reconstructions.
- Produce English narration and naturally adapted, synchronized Bangla subtitles.
- Keep the user in control through explicit approval gates.
- Prefer low-cost and free tools where practical without compromising factual reliability.
- Make projects reproducible, searchable, versioned, testable, exportable, and recoverable.
- Operate securely as a single-user application initially.

## 3. Product Principles

1. **Evidence before narrative.** Storytelling must not override the available evidence.
2. **Claim-level traceability.** Major factual claims must link to their sources and script locations.
3. **Scholarly credibility.** Source quality matters; weak and strong evidence must not be presented as equivalent.
4. **Transparent uncertainty.** Disputed interpretations, missing evidence, and uncertain dates must be identified explicitly.
5. **Original expression.** Scripts synthesize research rather than reproduce copyrighted books.
6. **Honest source access.** The application must never imply it verified material it could not access.
7. **Human approval.** AI must not silently approve major stages, make consequential recovery actions, or publish a documentary.
8. **Cost awareness.** Estimate and track AI costs before and during work.
9. **Reproducibility.** Preserve source provenance, model configuration, decisions, approvals, and revisions.
10. **Privacy by design.** Project data remains local unless the user deliberately configures an external service.

## 4. Intended Users and Language

- **Initial user model:** One authorized user; no public registration or team roles in the initial release.
- **Interface language:** English.
- **Documentation language:** English, including README, technical docs, API contracts, task tracker, acceptance criteria, and development instructions.
- **Future localization:** The architecture should permit a Bengali interface later. Documentary Bangla subtitles are a separate production output and are supported from the beginning.

## 5. Main Features

### 5.1 Project Setup and Brief

- Create a project for any subject, including history, geopolitics, religion and intellectual history, economics, science, and technology.
- Generate a concise project brief containing the scope, central question, intended audience, constraints, and initial research direction.
- Identify overly broad topics and recommend a focused narrative or a multi-part series.
- Pause for user approval before research begins.

### 5.2 Book Selection and Research

- Generate and rank a shortlist of relevant books.
- Evaluate scholarly credibility, topic relevance, influence, reader engagement, narrative potential, and accessibility.
- Treat scholarly credibility as a minimum quality bar.
- Explain the rationale and evidence behind recommendations.
- Wait for the user to approve the final five books before detailed research begins.
- Incorporate relevant primary sources and supplementary scholarly sources.
- Use only legally accessible material. If a source cannot be accessed, clearly disclose the limitation and use suitable supplementary sources rather than claiming to have read it.

### 5.3 Source Import and Quality

Planned import formats:

- PDF
- EPUB
- DOCX
- TXT
- Web links

Planned processing:

- Extract text and capture available metadata.
- Apply OCR to scanned PDFs when supported.
- Preserve page or section references where possible.
- Assess extraction quality and flag missing pages, uncertain passages, or likely OCR errors.
- Allow manual correction.
- Verify original material before using quotations or critical claims.

### 5.4 Evidence Ledger and Source Evaluation

Maintain a claim-level evidence ledger linked to the documentary script. For every major claim, record:

- Claim text and claim type.
- Supporting source and exact page, section, or timestamp where available.
- Supporting passage and context.
- Source authority, primary-source status, independence, and corroboration.
- Evidence strength or confidence, with an explanation.
- Conflicting evidence and competing interpretations.
- Whether the material was directly verified or remains uncertain.
- The script section and scene that depend on the claim.

Source evaluations should consider authority, evidence quality, independence, relevance, recency where relevant, and corroboration. The application must explain its assessments and flag conflicts rather than treating an automated score as proof of truth.

### 5.5 Thesis and Story Development

- Develop an evidence-led central thesis.
- Compare competing interpretations and assess their supporting and conflicting evidence.
- Recommend a conclusion proportional to the strength of available evidence.
- Synthesize the approved books into a coherent narrative instead of summarizing each book separately.
- Use nonlinear storytelling when appropriate while maintaining a verified chronological backbone.
- Build dramatic cold opens, evidence-backed suspense, clear transitions, and a thought-provoking conclusion.
- Use a calm, authoritative cinematic narration style.
- Obtain user approval of the thesis and narrative plan before scripting proceeds.

### 5.6 Script and Narration

- Generate a narration-ready documentary script for approximately 5–15 minutes.
- Link important factual claims to the evidence ledger and citations.
- Distinguish facts, interpretations, allegations, and unresolved questions.
- Verify quotations against original texts or reliable critical editions where accessible.
- Record translation details and distinguish verbatim quotations from paraphrases.
- Maintain a project-wide style guide and terminology glossary.
- Generate a pronunciation guide for important names and specialist terms.
- Validate structure, required fields, citations, and cross-stage consistency.

### 5.7 English Captions and Bangla Subtitles

- Produce English captions and natural Bangla subtitle adaptations.
- Use standard Bengali script, consistent transliteration, and a project-wide terminology glossary.
- Synchronize subtitles with the approved narration.
- Export timed `.srt` files.
- Check timing, segmentation, readability, and synchronization.
- Avoid treating literal machine translation as sufficient without quality review.

### 5.8 Scene and Visual Planning

Each scene must have a defined narrative purpose: what the viewer should learn, feel, or understand.

The production plan may include:

- Scene descriptions and durations.
- Archival footage, stills, maps, diagrams, and other visual references.
- AI video-generation prompts and camera directions.
- On-screen text and citation cues.
- Transitions, music, sound effects, and cinematic pauses.
- Visual verification notes and asset references.

Prioritize authentic archival material when available and appropriate. Verify provenance, date, context, and rights. Use AI-generated or staged reenactments selectively, label them clearly, and never present them as authentic archival footage. Reuse suitable assets where possible to control costs.

### 5.9 Editing and Publication Package

Generate a timestamped editing blueprint that connects narration, visuals, scene duration, transitions, on-screen text, audio cues, captions, and subtitles.

Prepare several evidence-based options for:

- Documentary titles.
- Thumbnail concepts.
- Publication descriptions.
- Relevant credits and source lists.

Evaluate options for factual accuracy, clarity, curiosity, and audience appeal. The user chooses the final option. Titles and thumbnails must not make claims the documentary does not support.

### 5.10 Quality Assurance

The quality-control workflow should cover:

- Factual accuracy and claim-level evidence traceability.
- Source attribution and citation completeness.
- Scholarly balance and treatment of contested claims.
- Chronology, quotations, translations, and terminology.
- Narrative structure and clarity.
- Visual authenticity and historical accuracy.
- Narration, pronunciation, audio levels, and sound design.
- Subtitle quality, timing, and accessibility.
- Asset provenance, licensing, and usage restrictions.
- Platform-specific technical requirements.

Serious factual or copyright failures block publication readiness and cannot be offset by a high overall score. Automated checks supplement human review; they do not establish historical truth by themselves. Passing quality checks does not authorize publication.

## 6. Approval-Driven Workflow

The workflow should have explicit gates:

1. Create project and generate the project brief.
2. User approves the brief.
3. Generate a ranked book shortlist.
4. User approves the final five books.
5. Research approved sources and relevant primary materials.
6. Build and review the evidence ledger.
7. Propose thesis and narrative alternatives.
8. User approves the central thesis and narrative plan.
9. Generate the cited script.
10. User reviews and approves the script.
11. Generate the scene plan, visual prompts, narration guidance, captions, subtitles, and audio plan.
12. Assemble the editing blueprint and production package.
13. Run automated and manual quality checks.
14. Prepare publication concepts, citations, credits, and technical files.
15. User explicitly approves the final package before publication or distribution.

At each major stage, the user can approve, reject, request changes, or reopen a previously approved stage. The system must track dependencies, identify downstream materials affected by revisions, preserve previous versions, and wait for approval before applying substantive downstream changes.

## 7. Deliverables

Each completed project should provide a complete master document plus separate production-ready files, including:

- Project brief.
- Ranked book shortlist and approved five-book list.
- Research dossier.
- Bibliography and source notes.
- Claim-level evidence ledger.
- Source-linked historical chronology with date confidence and disputed-date flags.
- Project glossary and transliteration rules.
- Approved thesis and narrative plan.
- Cited documentary script.
- Pronunciation guide.
- Scene-by-scene visual plan.
- AI video prompts and camera directions.
- Audio, music, and sound-effects plan.
- English captions.
- Bangla `.srt` subtitles.
- Timestamped editing blueprint.
- Asset and licensing register.
- Title, thumbnail, and description concepts.
- Quality-control report.
- Version history and change log.

The user must be able to export the complete project folder and its separate deliverables in appropriate formats.

## 8. Proposed Technical Architecture

The following is the intended initial stack, subject to implementation validation.

| Layer | Proposed technology | Responsibility |
|---|---|---|
| Frontend | React, Vite, TypeScript | Dashboard, project setup, research views, approvals, job status, cost views, file browser |
| Backend | Python, FastAPI | API, workflow orchestration, validation, authentication, AI integrations, export |
| Database | SQLite initially | Projects, workflow stages, sources, claims, approvals, jobs, costs, versions |
| Database evolution | Abstraction for future PostgreSQL | Reduce coupling to SQLite and support a later migration |
| File storage | Organized local project folders | Imported sources, research, scripts, subtitles, assets, exports |
| Background work | Persistent job queue and checkpoints | Long-running tasks, progress, retries, cancellation, resumability |
| AI integration | Provider-independent adapters | Model selection, usage tracking, consistent interfaces |
| Testing | pytest, Vitest, React Testing Library, Playwright | Unit, frontend, integration, and end-to-end tests |
| Containers | Docker and Docker Compose | Reproducible local deployment |
| CI/CD | GitHub Actions | Tests, scans, image builds, release validation, deployment workflow |
| Observability | OpenTelemetry-compatible instrumentation, Prometheus, Grafana, Alertmanager | Traces, metrics, dashboards, and user-impact alerts |
| Version control | Git and private GitHub repository | Source history, branches, reviews, tagged releases |

### Conceptual architecture

```text
React + Vite + TypeScript
            |
            v
        FastAPI API
            |
            +-- Authentication and project workflow
            +-- Research and evidence ledger
            +-- Script and production generation
            +-- Validation and quality assurance
            +-- Background jobs and checkpoints
            +-- Provider-independent AI adapters
            +-- Cost and usage tracking
            +-- OpenTelemetry instrumentation
            |
            +-- SQLite database
            +-- Organized local project files
            +-- Export and backup services
```

The frontend must not connect directly to SQLite or receive AI-provider secrets. Sensitive operations belong on the server.

## 9. Background Jobs and AI Reliability

Long-running research and production tasks should run in a persistent background queue.

Required behavior:

- Show live progress, job status, and job history.
- Save checkpoints and resume after interruptions.
- Support cancellation where safe.
- Apply bounded retries with exponential backoff to recoverable failures.
- Respect provider `Retry-After` headers and rate limits.
- Use configurable per-provider and per-model limits, bounded concurrency, and request/token budgets.
- Validate AI output against explicit schemas and quality rules.
- Attempt bounded, targeted repairs when appropriate.
- Preserve failed outputs, versions, and diagnostic details.
- Request user intervention when validation still fails.
- Recommend alternative providers but require approval before switching if cost or output quality may change.

Maintain versioned model configuration and record the provider and model used for each task. Evaluate replacement models before adoption; require user approval for changes that may materially affect cost or output quality.

## 10. Cost Management

Track estimated and actual AI costs by:

- Project.
- Workflow stage.
- Provider.
- Model.

Provide configurable budgets, pre-run cost estimates, usage history, and warnings before expensive operations. Prefer lower-cost alternatives where suitable, but do not silently sacrifice factual reliability or approved output quality to reduce cost.

## 11. Database and File Management

- Use SQLite initially, with an abstraction for future PostgreSQL migration.
- Keep project assets in organized local folders.
- Maintain stable identifiers and links between projects, sources, claims, scenes, jobs, and deliverables.
- Provide full-text search across project documents and metadata, with filters for source, stage, date, file type, and project.
- Use version-controlled, forward-only database migrations.
- Automatically back up and verify the database before schema changes.
- Test migrations against representative data.
- Require explicit approval for production migrations.
- Document recovery procedures, including backup restoration.
- Perform integrity checks on database records and exported project files.

## 12. Security and Privacy

The application is initially a secure, single-user, self-hosted system with no public registration.

Planned safeguards:

- Secure authentication and protected sessions.
- Least-privilege access.
- Encrypted transport for remote access.
- Protected local storage where practical.
- Server-side secrets and API keys.
- Untracked local environment files during development.
- GitHub Actions encrypted secrets for CI/CD.
- Startup configuration validation and secret redaction in logs.
- Secure file-upload and file-processing controls.
- Documented retention and deletion policies.
- Explicit project and source deletion controls.
- Removal of deleted data from active storage and indexes.
- Clear documentation of backup retention and expiry.
- Minimal operational audit records retained under a defined policy.

A future migration to a dedicated secret manager should be documented. The application should not claim deleted information has disappeared from every backup until those copies expire or are otherwise removed.

### Release security gates

CI should include automated dependency and secret scanning, static analysis, authentication and authorization tests, secure file-upload tests, and security-focused integration tests. Releases must be blocked for unresolved critical or high-severity findings unless a documented exception receives explicit approval.

## 13. Backups and Disaster Recovery

- Create scheduled, versioned backups of the database and project files.
- Support optional encrypted off-device copies.
- Verify backup integrity automatically.
- Regularly test full restoration to a separate location.
- Maintain a documented recovery checklist.
- Preserve version history and approval records in recoverable backups.
- Document backup retention and expiry.
- Consider configurable recovery-point and recovery-time objectives as deployment matures.

## 14. Containerization, Deployment, and CI/CD

Initial deployment will use Docker Compose on the user's own computer, with secure remote access when needed. Cloud deployment is a future option and should have a documented migration path.

Release requirements:

- Build immutable, versioned Docker images.
- Run automated tests, security scans, and deployment health checks.
- Retain the previous known-good release.
- Require explicit approval for production deployment and rollback.
- Verify database compatibility and recovery before release.
- Preserve configuration separately from application images.
- Document deployment, rollback, backup, restoration, and troubleshooting procedures.

CI/CD should validate releases and produce evidence. It must not silently deploy a production change or perform a rollback without the required approval.

## 15. Observability and Incident Response

Use structured application logs and OpenTelemetry-compatible traces and metrics, with Prometheus, Grafana, and Alertmanager in a local-first setup.

Prioritize user-impact signals rather than CPU graphs alone. Signals should include:

- API error rate and latency.
- Project creation and workflow completion rates.
- Failed or stalled background jobs.
- Script or subtitle generation failures.
- Export success and failure rates.
- AI-provider errors, throttling, and latency.
- Budget warnings and unexpected cost increases.

Alert rules should be configurable and SLO-based, with sustained thresholds, severity levels, deduplication, recovery notifications, and documented runbooks.

### Incident responder agent

The responder agent should:

- Correlate alerts with logs, traces, metrics, recent deployments, and failed jobs.
- Produce evidence-linked incident reports with likely causes, user impact, confidence, and ranked runbook recommendations.
- Preserve an audit trail of investigations and recommendations.
- Operate in read-only diagnostic mode initially.
- Require explicit human approval for every change and recovery action.

The agent must not autonomously restart services, roll back releases, change configuration, or modify data.

## 16. Testing Strategy

Use multiple layers of automated testing:

- **Unit tests:** isolated business logic, ranking rules, cost calculations, validators, and utility functions.
- **Frontend tests:** React components, forms, navigation, approval controls, progress indicators, accessibility behavior.
- **Integration tests:** FastAPI endpoints, SQLite persistence, imports, AI adapters, job queue, exports, migrations, and recovery.
- **End-to-end tests:** important user journeys through the browser using Playwright.
- **AI output tests:** schema compliance, citation presence, subtitle timing, consistency, cost limits, and failure handling, with mocked providers for routine tests.
- **Security tests:** authentication, authorization, file handling, secrets, and access boundaries.
- **Operational tests:** container health checks, alert triggers, rollback verification, backup integrity, and restoration.

Real-provider smoke tests must be explicitly authorized and cost-aware.

Do not rely on coverage percentage alone. Tests should validate measurable behavior and important failure modes.

## 17. Task Tracker and Agent Accountability

The specification and task tracker must provide traceability from requirements through implementation and verification.

Every development task must include:

- A link to a specification requirement.
- Measurable acceptance criteria.
- Dependencies and relevant implementation scope.
- Linked commits or pull requests.
- Relevant passing test results.
- Implementation evidence.
- A verification record and independent completion decision.

Implementation agents must update the task tracker and link their work. Task completion requires independent verification, not merely an agent's claim.

The user has selected a private source-code repository and wants the specification and task tracker publicly accessible without exposing secrets or private project data. The precise tracker configuration and public links must be established during repository setup; no public tracker is claimed to exist yet.

## 18. Documentation Standards

All application documentation and interface text will be in English.

Maintain version-controlled documentation for:

- Product requirements and acceptance criteria.
- Architecture and design decisions.
- Local setup and deployment.
- API contracts and generated client types.
- Database schema and migrations.
- AI-provider integrations and model configuration.
- Workflows and approval gates.
- Testing and quality assurance.
- Security, privacy, and secrets.
- CI/CD, releases, rollback, and recovery.
- Observability, alert rules, runbooks, and incident response.
- Troubleshooting and operational procedures.

Update documentation alongside code changes.

For API compatibility, use versioned OpenAPI contracts, generated TypeScript client types, request/response validation, contract and integration tests in CI, and documented compatibility checks for breaking changes.

## 19. Accessibility and Interface Quality

Target practical WCAG 2.2 AA accessibility, including:

- Keyboard navigation.
- Screen-reader support.
- Visible focus indicators.
- Sufficient color contrast.
- Accessible forms and error messages.
- Readable, responsive layouts.

Include automated accessibility checks and manual keyboard and screen-reader testing in release validation.

## 20. Success Criteria

The initial product is successful when a user can complete one well-researched, accurately cited, bilingual documentary package through the full workflow with reliable approvals, revision tracking, and export.

Evaluate success across:

- Research quality and evidence traceability.
- Factual reliability, as a non-negotiable threshold.
- Narrative clarity and audience engagement.
- Educational value.
- Production quality and subtitle usability.
- Workflow reliability and recoverability.
- Cost transparency and affordability.
- Security, accessibility, and maintainability.

As projects are published, available audience-retention data, watch time, click-through rate, and viewer feedback may inform improvements. Performance metrics must never override factual accuracy.

## 21. Development Roadmap

### Phase 1 — Working Full-Stack Foundation

- Repository structure and English documentation.
- React frontend, FastAPI backend, and SQLite.
- Docker Compose local deployment.
- Authentication and project CRUD.
- Project folder creation and file browser.
- CI for linting, tests, and security checks.
- Initial unit, frontend, and integration tests.

### Phase 2 — Research and Evidence

- Source import and extraction-quality checks.
- Ranked book shortlist and approval of five books.
- Source evaluation and primary-source support.
- Claim-level evidence ledger and chronology.
- Search, glossary, and source-linked research dossier.

### Phase 3 — Thesis and Script

- Project brief approval.
- Central thesis and competing interpretations.
- Cited script generation and review.
- Versioning, revision dependencies, and consistency checks.

### Phase 4 — Production Package

- Scene plan and AI video prompts.
- Narration and pronunciation guide.
- English captions and Bangla subtitles.
- Audio plan and editing blueprint.
- Asset register and licensing checks.
- Master document and separate exports.

### Phase 5 — Operational Reliability

- Persistent background jobs and checkpoints.
- Cost dashboards and provider rate-limit controls.
- OpenTelemetry instrumentation and user-impact alerts.
- Read-only incident responder agent.
- Backup verification and tested restoration.
- Versioned container releases and human-approved rollback.
- Accessibility validation and expanded security testing.

### Phase 6 — Refinement and Future Deployment

- Model evaluation and controlled provider updates.
- Performance-informed workflow improvements.
- PostgreSQL migration readiness.
- Documented cloud deployment path.
- Optional advanced video generation and additional production integrations.

Each phase must have measurable acceptance criteria, relevant automated tests, implementation evidence, and independent verification before being marked complete.

## 22. Getting Started

This repository is at the requirements and planning stage. Installation commands, environment variables, database initialization, service ports, and run scripts must be documented after the initial implementation establishes those details.

The first technical milestone should be a tested vertical slice:

1. Start the frontend, backend, and database using Docker Compose.
2. Create a documentary project in the React interface.
3. Save it through FastAPI into SQLite.
4. Retrieve and display it in the interface.
5. Test the API and database integration.
6. Verify the workflow through a browser test.
7. Build and validate the container images in CI.

Only after this slice works should the research and production pipeline be added incrementally.

---

**AI Documentary Production Studio**

*Research carefully. Tell compelling stories. Keep every important claim accountable to evidence.*

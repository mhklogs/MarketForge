# MarketForge — Functional Requirements

> Derived from static analysis of the source tree on 2026-09-28. Each requirement cites
> the file that evidences it, so any claim can be checked. Requirements marked
> *inferred* are derived from naming and structure rather than an explicit
> specification.

## FR-1 Route and page behaviour

No file-system-routed pages were detected. This project appears to be a library, CLI, notebook collection, or a single-page entrypoint.

| ID | Requirement | Evidence |
| --- | --- | --- |
| FR-1.01 | The system shall provide the entrypoint `app.py` | `app.py` |

## FR-2 Programmatic interface

*No API route handlers detected.*

## FR-3 Presentation components

*No dedicated component directory detected.*

## FR-4 Notebook workflows

1 Jupyter notebook(s) are present. Each shall be runnable end-to-end from a clean environment, with inputs and expected outputs documented.

## FR-5 AI behaviour

An LLM or agent framework is a direct dependency. The system shall:

- accept a structured prompt or job input;
- return output conforming to a declared schema, or fail with an explicit error;
- never silently return partial or malformed model output;
- record model, prompt version, and token usage for every generative call. *(inferred — no audit logging was positively detected)*

## FR-8 Configuration

The following environment variables are referenced in source. Each shall be
validated at startup with a clear error when missing.

| Variable | Referenced in |
| --- | --- |
| `GEMINI_API_KEY` | see source |

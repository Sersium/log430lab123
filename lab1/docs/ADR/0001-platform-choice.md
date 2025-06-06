# ADR 0001: Platform Choice

Date: 2025-05-26
Status: accepted

## Context

We need a development and deployment setup that works the same everywhere and is easy to maintain. The application is a simple CLI point-of-sale tool.

## Decision

- Use Python 3.9+ for its readability and wide community support.
- Use containers with Podman Compose to isolate the environment and ensure consistent dependencies.
- Provide a console (CLI) interface instead of a web or GUI to keep the user experience simple and focused.

## Consequences

- Requires installing Podman (or Docker) in addition to Python.
- No graphical interface may limit non-technical users.

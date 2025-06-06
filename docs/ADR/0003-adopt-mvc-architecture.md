# ADR 0003: Adopt MVC Architecture

Date: 2025-05-27
Status: accepted

## Context

The current POS application runs as a command line interface. To eventually provide web or mobile user interfaces, we need a clean separation between presentation code and business logic. A modular structure will also make automated testing easier.

## Decision

- Organize the code following the Model-View-Controller (MVC) pattern.
- Keep SQLAlchemy models as the **Model** layer.
- Create controllers for business rules and database interaction.
- Keep the CLI as the initial **View** layer, allowing additional views for web or mobile later.

## Consequences

- Adds structural overhead with more folders and classes.
- Business logic becomes reusable across multiple interfaces.

# ADR 0002: Persistence Strategy

Date: 2025-05-26
Status: accepted

## Context

We need to store products, sales, and sale items in a reliable way. Data consistency and the ability to report on stock and sales history are important.

## Decision

- Use PostgreSQL as a server database.
- Use SQLAlchemy ORM in Python to interact with the database and avoid writing raw SQL.

## Consequences

- Ready support for transactions to keep stock levels accurate.
- Easily express relationships between products, sales, and items through ORM classes and methods.
- Query reports via ORM methods without hand-writing SQL statements.
- Running a database server adds deployment complexity.
- Extra configuration compared to an embedded or local file-based database.

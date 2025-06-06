# ADR 0004: Store Database Synchronization

Date: 2025-05-27
Status: accepted

## Context

Each store operates its own POS instance and must continue working even when the connection to headquarters (HQ) is unavailable. HQ needs consolidated data for reporting and to manage stock across stores. We must choose between a centralized database and some form of replication.

## Decision

- Run a local PostgreSQL database at each store.
- Periodically replicate data from each store to a central HQ database whenever connectivity allows.
- Resolve conflicts by timestamp and store identifier so HQ can merge updates reliably.

## Consequences

- Stores can operate offline without blocking sales.
- Additional synchronization tooling is required and may introduce replication delays.
- HQ receives a consolidated view of sales and inventory once replication completes.

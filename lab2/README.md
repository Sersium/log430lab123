# Lab 2

This lab extends the POS example to multiple store instances and a central logistics service with a simple head‑quarters interface.

- Each store runs the CLI from `src/cli.py` with its own PostgreSQL database.
- The logistics service manages central stock and restock requests (see `logistics/`).
- The HQ CLI (`hq/cli.py`) allows updating products in the logistics database and synchronising all stores as well as generating a consolidated sales report.
- `docker-compose.yml` starts two stores, the logistics service and the HQ container as a proof of concept.

Run tests with:

```bash
PYTHONPATH=. pytest -q
```

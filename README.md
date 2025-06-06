<!-- filepath: /home/log430/log430lab1/README.md -->

# log430lab123

laboratoire 1-2-3 du cours log430 ete 2025

## Project Overview

This repository contains a simple 2-tier (client/server) point-of-sale (POS) application implemented in Python using SQLAlchemy for persistence.

## Prerequisites

- Python 3.9+
- Podman & podman-compose

## Installation

Clone the repository and prepare the environment:

```bash
git clone https://github.com/<your-user>/log430lab1.git
cd log430lab1
```

## Running with Podman

1. Build or rebuild the client image:

   ```bash
   podman-compose build
   ```

2. Start the databases in detached mode (local store and HQ):

   ```bash
   podman-compose up -d db hqdb
   ```

3. Run the client (CLI) interactively (inherit tty and stdin settings from service):

   ```bash
   podman-compose run --rm app
   ```

This ensures both databases run in the background while you interact with the POS CLI.
The compose file already sets `HQ_DATABASE_URL` so the application can
synchronize with the HQ database and generate consolidated reports.

## Stopping Services

To stop and remove containers (preserving volumes):

```bash
podman-compose down
```

To also remove volumes:

```bash
podman-compose down -v
```

## Documentation

All design documents, ADRs, and UML diagrams are located under the `docs/` directory.

## Testing

You can run unit tests locally (requires Python and dependencies):

```bash
pytest -q
```

## Technology Stack

- Python 3.9+: clear syntax and rich ecosystem
- SQLAlchemy ORM + PostgreSQL: reliable transactions and easy data modeling
- Podman Compose: container-based isolation and consistent deployments
- tabulate: formatted console tables

## Usage

After starting the DB and running `podman-compose run --rm app`, you will see a menu:

```text
1. Add product
2. Update stock
3. Search products
4. Record sale
5. Return sale
6. Stock report
7. Sales report
8. Replenish from warehouse
9. Dashboard
10. HQ sales report
11. HQ stock report
0. Exit
```

Enter the number of the desired action and follow prompts to manage products and sales.

<!-- filepath: /home/log430/log430lab1/README.md -->

# log430lab1

laboratoire 1 du cours log430 ete 2025

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

2. Start the database in detached mode:

   ```bash
   podman-compose up -d db
   ```

3. Run the client (CLI) interactively (inherit tty and stdin settings from service):

   ```bash
   podman-compose run --rm app
   ```

This ensures the database runs in the background while you interact with the POS CLI.

## Stopping Services

To stop and remove containers (preserving volumes):

```bash
podman-compose down
```

To also remove volumes:

```bash
podman-compose down -v
```

## Seeding the Database

Once your services are running, inject demo data with the seed script:

```bash
podman-compose exec app python -m src.seed
```

Or run one-off (container will exit when done):

```bash
podman-compose run --rm app python -m src.seed
```

## Documentation

All design documents, ADRs, and UML diagrams are located under the `docs/` directory.

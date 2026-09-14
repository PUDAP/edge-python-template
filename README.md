# edge-python-template

Template for a machine edge service in Python (PUDA CLI **v0.1.0**, Python SDK **0.0.17**). Use this to scaffold a new machine integration.

## Repo Structure

```
edge-python-template/
├── pyproject.toml          # Python project dependencies
├── uv.lock                 # Locked dependency versions (uv)
├── main.py                 # Main edge service — NATS + driver instance
├── driver.py               # Machine driver and @command methods
├── Dockerfile              # Container build
├── compose.yml             # Docker Compose
├── start_edge.bat          # Windows launcher script
├── .env.example            # Environment variable template
├── .dockerignore           # Docker build context exclusions
└── .gitignore              # Git ignore rules
```

## AI Agent Instructions

Follow these steps in order to adapt this template for a new machine.

### 1. Choose a unique Machine ID in your env

Pick a short, lowercase, hyphen-separated identifier for the machine and edit the `.env` file. This becomes `MACHINE_ID` everywhere.

### 2. Complete all TODOs

Search the repo for every `TODO` marker and resolve each one — typically renaming placeholder strings, filling in package metadata, and updating import paths to match the chosen `MACHINE_ID`.

### 3. Implement the Driver

Add the machine driver source in `driver.py`. The driver must expose a class that `puda.EdgeRunner` can wrap. Parameters should be JSON primitives (`str`, `int`, `float`, `bool`, `dict`, `list`) rather than custom class instances.

- Require `puda>=0.0.17` in `pyproject.toml` (already set in this template). Add other hardware dependencies as needed.
- Put a one-sentence summary in the **class docstring**. `puda machine list` and `puda machine ping` show that first paragraph as `description`.
- Decorate every remotely callable method with `@command`. Undecorated methods are not advertised. A driver with no `@command` methods fails at startup.
- Keep helpers private (`_name`). Raise on hardware failure. Returning `False` is still a successful PUDA response (`{"result": false}`).
- Attach `@safety` to commands that can cause harm. It is published in the catalog; it does not block edge dispatch. This template includes two examples in `driver.py`:
  - `move_to` — `confirm=True` so the agent prompts the operator before the move.
  - `set_heater` — advisory only (`confirm` defaults to `false`).
  Omit `@safety` on read-only commands such as `get_position`.

### 4. Add Driver-Specific Environment Variables

In `.env`, add any new config fields below `MACHINE_ID` (e.g. `${MACHINE_ID}_PORT`, `${MACHINE_ID}_HOST`). Keep `NATS_SERVERS` and `MACHINE_ID` as-is.

### 5. Wire the Driver into main.py

In `main.py`:

1. Add any driver-specific environment variables to `Config` (e.g. device port, IP address).
2. Instantiate the driver using those config fields.

### 6. Update the Dockerfile

In `Dockerfile`, add any system-level dependencies your driver needs (e.g. `libusb-dev` for USB devices).

Replace this file with a machine-specific README describing what the machine does, how to connect to it, and any hardware prerequisites.

---

## Environment Setup

From repo root:

```bash
cp .env.example .env
```

Edit `.env` and fill in:

- `MACHINE_ID` — machine identifier
- `NATS_SERVERS` — comma-separated NATS server URLs
- Any additional driver-specific variables

## Run With Docker (Recommended)

All commands below run from repo root.

Build and start:

```bash
docker compose -f compose.yml up -d --build
```

View logs:

```bash
docker compose -f compose.yml logs -f
```

Stop:

```bash
docker compose -f compose.yml down
```

## Run Baremetal (uv)

```bash
uv sync
uv run python main.py
```

## Build and Push Image (GHCR)

Login:

```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

Build and push:

```bash
docker compose -f compose.yml build
docker compose -f compose.yml push
```

## Notes

- Docker build context is the repository root.
- Dockerfile path is `Dockerfile`.
- `MACHINE_ID` in `.env` is used for NATS subject routing and Docker image/container naming.

# edge-python-template

Template for a machine edge service in python. Use this to scaffold a new machine integration.

## Repo Structure

```
edge-python-template/
├── pyproject.toml          # Python project dependencies
├── uv.lock                 # Locked dependency versions (uv)
├── main.py                 # Main edge service — NATS + driver instance
├── driver.py               # Machine driver and public PUDA commands
├── Dockerfile              # Container build
├── compose.yml             # Docker Compose
├── compose.livestream.yml  # Livestream stack for camera streaming
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

Add the machine driver source in `driver.py`. The driver must expose a class that `puda.EdgeRunner` can wrap. Public methods should only accept primitives or standard data structures (like JSON, arrays, and tuples) rather than custom class instances.

- Add required dependencies in `pyproject.toml` if needed.

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

## Livestream Cameras

The livestream stack runs `mediamtx` and `ffmpeg` in a separate Compose file. It streams two local V4L2 camera devices to MediaMTX as `cam0` and `cam1`.

Required `.env` values:

- `TAILSCALE_IP` - Tailscale IP advertised for WebRTC clients
- `VIDEO_DEVICE_0` - first camera device path, for example `/dev/video0`
- `VIDEO_DEVICE_1` - second camera device path, for example `/dev/video1`

Check which cameras are available:

```bash
ls /dev/video*
```

If cameras are present, update `.env` with the matching devices:

```dotenv
TAILSCALE_IP=100.107.192.52
VIDEO_DEVICE_0=/dev/video0
VIDEO_DEVICE_1=/dev/video1
```

Start the livestream stack:

```bash
docker compose -f compose.livestream.yml up -d
```

Stop the livestream stack:

```bash
docker compose -f compose.livestream.yml down
```

Stream endpoints:

- RTMP publish paths: `rtmp://<host>:1935/cam0`, `rtmp://<host>:1935/cam1`
- HLS playback: `http://<host>:8888/cam0`, `http://<host>:8888/cam1`
- WebRTC/WHEP: `http://<host>:8889/cam0`, `http://<host>:8889/cam1`

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

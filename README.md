# Edge-Native Telemetry & Anomaly Engine

An asynchronous Python pipeline for ingestion, zero-phase SciPy digital filtering, and low-latency WebSocket streaming.

## Features
- **Zero-Phase Signal Processing**: SciPy Butterworth low-pass filter (`filtfilt`) preventing phase distortion.
- **Asynchronous Execution**: Thread-safe `asyncio.Queue` decoupling ingestion from CPU inference.
- **FastAPI Endpoint**: Real-time WebSocket metric broadcasting (`/ws/telemetry`).
- **Daemon Configuration**: Native Linux `systemd` service integration.

## Usage
```bash
python main.py
import asyncio
import uvicorn
import numpy as np
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from telemetry_engine.ingestor import StreamIngestor

app = FastAPI(title="Edge-Native Telemetry Engine", version="1.0.0")
ingestor = StreamIngestor()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "pipeline": "active"}

@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Simulate 16-point raw sensor chunk at 250 Hz
            synthetic_signal = np.random.normal(loc=0.0, scale=1.0, size=16).tolist()
            await ingestor.push_raw_stream(synthetic_signal)
            
            async for metric in ingestor.consume_and_process():
                await websocket.send_json(metric)
                await asyncio.sleep(0.064)
    except WebSocketDisconnect:
        print("Client disconnected.")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
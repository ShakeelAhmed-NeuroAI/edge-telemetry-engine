import asyncio
import numpy as np
from typing import AsyncGenerator
from .processor import TelemetryProcessor

class StreamIngestor:
    def __init__(self, buffer_size: int = 256):
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=buffer_size)
        self.processor = TelemetryProcessor()

    async def push_raw_stream(self, chunk: list[float]):
        data_array = np.array(chunk, dtype=np.float64)
        if self.queue.full():
            await self.queue.get()  # Drop oldest frame if buffer overflows
        await self.queue.put(data_array)

    async def consume_and_process(self) -> AsyncGenerator[dict, None]:
        while True:
            raw_frame = await self.queue.get()
            results = self.processor.process_frame(raw_frame)
            self.queue.task_done()
            yield results
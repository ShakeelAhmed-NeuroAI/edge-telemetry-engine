import numpy as np
from scipy.signal import butter, filtfilt

class TelemetryProcessor:
    def __init__(self, sample_rate: float = 250.0, cutoff: float = 40.0):
        self.sample_rate = sample_rate
        self.cutoff = cutoff
        nyquist = 0.5 * sample_rate
        normal_cutoff = cutoff / nyquist
        self.b, self.a = butter(N=2, Wn=normal_cutoff, btype='low', analog=False)

    def process_frame(self, raw_data: np.ndarray) -> dict:
        if len(raw_data) < 15:
            filtered = raw_data
        else:
            filtered = filtfilt(self.b, self.a, raw_data)

        std_dev = np.std(filtered)
        baseline = np.median(np.abs(filtered))
        anomaly_score = float(std_dev / (baseline + 1e-6))

        return {
            "filtered_mean": float(np.mean(filtered)),
            "anomaly_score": round(anomaly_score, 4),
            "is_anomaly": anomaly_score > 3.5
        }
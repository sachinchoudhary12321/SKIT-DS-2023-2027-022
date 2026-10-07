"""Crop disease inference seam (ML Integration task).

Current behaviour: `predict()` raises ModelNotAvailableError — the backend
NEVER produces fake predictions. When the trained model exists, only this
file (and a worker that calls PredictionService.process_prediction) changes.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

from app.core.exceptions import ModelNotAvailableError

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PredictionResult:
    """Output of a successful inference (produced only by the real model)."""

    crop: str
    disease: str
    confidence: float
    model_version: str


class CropDiseasePredictor:
    """Inference interface used by the prediction service."""

    def warm_up(self) -> None:
        """Called once at application startup.

        TODO(ML Integration task): load the trained artifact here
        (e.g. torch.load / YOLO weights) so the first request is not slowed
        down. Log a warning instead of crashing when no artifact exists.
        """
        logger.info("ML integration pending: predictor is running in stub mode.")

    def predict(self, image_bytes: bytes) -> PredictionResult:
        """Run disease detection on raw image bytes.

        TODO(ML Integration task), implement exactly here:
          1. decode + preprocess the image (OpenCV / Pillow: resize, normalise);
          2. run the model on the configured device (CPU / CUDA);
          3. map the output to (crop, disease, confidence);
          4. return PredictionResult(...).

        Synchronous and CPU-bound by design: callers execute it in a worker
        thread (see PredictionService.process_prediction).
        """
        raise ModelNotAvailableError(
            "Disease prediction is not connected to a trained model yet."
        )

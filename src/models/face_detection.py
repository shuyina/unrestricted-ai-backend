import logging
import cv2
import numpy as np
from typing import List, Tuple
from PIL import Image
import mediapipe as mp

logger = logging.getLogger(__name__)


class FaceDetector:
    def __init__(self):
        self.face_detection = mp.solutions.face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5,
        )

    def detect_faces(self, image: Image.Image) -> List[dict]:
        try:
            img_array = np.array(image)
            img_rgb = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

            results = self.face_detection.process(img_rgb)
            faces = []

            if results.detections:
                h, w = img_rgb.shape[:2]
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    x_min = max(0, int(bbox.xmin * w))
                    y_min = max(0, int(bbox.ymin * h))
                    x_max = min(w, int((bbox.xmin + bbox.width) * w))
                    y_max = min(h, int((bbox.ymin + bbox.height) * h))

                    faces.append({
                        "bbox": (x_min, y_min, x_max, y_max),
                        "confidence": detection.score[0],
                    })

            logger.info(f"Detected {len(faces)} faces")
            return faces
        except Exception as e:
            logger.error(f"Face detection failed: {e}")
            return []

    def extract_face_roi(self, image: Image.Image, bbox: Tuple[int, int, int, int]) -> Image.Image:
        x_min, y_min, x_max, y_max = bbox
        face_roi = image.crop((x_min, y_min, x_max, y_max))
        return face_roi

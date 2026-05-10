"""
Caving Detection Module
KI-basierte Erkennung von Kalbungen mittels YOLOv8
"""

import cv2
import numpy as np
from typing import Dict, Optional, Tuple
from datetime import datetime
import time

from ultralytics import YOLO

from logger import get_logger
from config import CONFIDENCE_THRESHOLD, IOU_THRESHOLD, DEBUG_MODE

logger = get_logger(__name__)


class CavingDetector:
    """Detektor für Kalberkennungs-Events."""

    # Signatur-Features für Kalbung
    CALVING_INDICATORS = {
        'cow_detected': True,
        'calf_nearby': True,
        'posture_lowered': True,  # Optional: Pose-Estimation
        'unusual_position': False,  # Optional: Spatial Analysis
    }

    def __init__(
        self,
        model: YOLO,
        confidence_threshold: float = CONFIDENCE_THRESHOLD,
        iou_threshold: float = IOU_THRESHOLD,
        debug_mode: bool = DEBUG_MODE
    ):
        """
        Initialisiere Caving Detector.

        Args:
            model: YOLOv8-Modell
            confidence_threshold: Minimum Konfidenz für Detektion
            iou_threshold: IOU-Threshold für NMS
            debug_mode: Debug-Visualisierung aktivieren
        """
        self.model = model
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.debug_mode = debug_mode

        self.last_detection_time = None
        self.detection_history = []
        self.max_history_size = 30  # ~1 Sekunde bei 30fps

        logger.info(
            f"CavingDetector initialisiert | "
            f"Confidence: {confidence_threshold:.2f} | "
            f"IOU: {iou_threshold:.2f}"
        )

    def detect(self, frame: np.ndarray) -> Optional[Dict]:
        """
        Führe Kalbungs-Detektion durch.

        Args:
            frame: Input Frame (BGR)

        Returns:
            Detection result dict oder None
        """
        try:
            # YOLOv8 Inferenz
            results = self.model(
                frame,
                conf=self.confidence_threshold,
                iou=self.iou_threshold,
                verbose=False
            )

            detections = self._parse_results(results[0], frame)

            # Kalbungs-Logik
            calving_detected = self._analyze_calving_indicators(detections, frame)

            detection_result = {
                'calving_detected': calving_detected,
                'confidence': detections.get('max_confidence', 0.0),
                'objects_detected': detections.get('num_objects', 0),
                'timestamp': datetime.now(),
                'detections': detections.get('classes', {})
            }

            # History aktualisieren
            self.detection_history.append(detection_result)
            if len(self.detection_history) > self.max_history_size:
                self.detection_history.pop(0)

            # Debug-Visualisierung
            if self.debug_mode and calving_detected:
                frame = self._draw_detections(frame, detections)
                cv2.imshow('Calving Detection', frame)
                cv2.waitKey(1)

            return detection_result

        except Exception as e:
            logger.error(f"Fehler in Detektion: {e}")
            return None

    def _parse_results(self, result, frame: np.ndarray) -> Dict:
        """Parse YOLOv8-Ergebnisse."""
        detections = {
            'num_objects': 0,
            'max_confidence': 0.0,
            'classes': {},
            'boxes': []
        }

        if result.boxes is None or len(result.boxes) == 0:
            return detections

        # Iteriere über alle erkannten Objekte
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            bbox = box.xyxy[0].cpu().numpy()

            class_name = result.names.get(class_id, f"unknown_{class_id}")

            # Speichere Detection
            if class_name not in detections['classes']:
                detections['classes'][class_name] = []

            detections['classes'][class_name].append({
                'confidence': confidence,
                'bbox': bbox,
                'x1': float(bbox[0]),
                'y1': float(bbox[1]),
                'x2': float(bbox[2]),
                'y2': float(bbox[3]),
                'width': float(bbox[2] - bbox[0]),
                'height': float(bbox[3] - bbox[1]),
            })

            detections['num_objects'] += 1
            detections['max_confidence'] = max(detections['max_confidence'], confidence)
            detections['boxes'].append(bbox)

        return detections

    def _analyze_calving_indicators(self, detections: Dict, frame: np.ndarray) -> bool:
        """
        Analysiere ob Kalbungs-Indikatoren vorhanden sind.

        Kalbungs-Signale:
        - Kuh erkannt
        - Kalb erkannt (oder Kuh gebeugte Haltung)
        - Zeitliche Sequenzen (mehrere Frames hintereinander)
        """
        # Basisch: Erkenne wenn "cow" oder "person" + high confidence
        detected_classes = list(detections.get('classes', {}).keys())

        calving_score = 0

        # Kuh erkannt
        if 'cow' in detected_classes:
            cow_conf = max([d['confidence'] for d in detections['classes']['cow']])
            if cow_conf > 0.7:
                calving_score += 0.5

        # Kalb erkannt
        if 'calf' in detected_classes:
            calf_conf = max([d['confidence'] for d in detections['classes']['calf']])
            if calf_conf > 0.6:
                calving_score += 0.3

        # Temporal Analysis: Konsistenz über mehrere Frames
        if len(self.detection_history) > 5:
            recent_calving = sum(
                1 for d in self.detection_history[-5:]
                if d.get('objects_detected', 0) > 1
            )
            if recent_calving >= 3:
                calving_score += 0.2

        # Schwellenwert
        is_calving = calving_score > 0.6

        if is_calving:
            logger.debug(
                f"Kalbungs-Indikatoren erkannt | "
                f"Score: {calving_score:.2f} | "
                f"Classes: {detected_classes}"
            )

        return is_calving

    def _draw_detections(self, frame: np.ndarray, detections: Dict) -> np.ndarray:
        """Zeichne Erkennungen in Frame."""
        frame_with_boxes = frame.copy()

        colors = {
            'cow': (0, 255, 0),    # Green
            'calf': (255, 0, 0),   # Blue
            'person': (0, 0, 255), # Red
        }

        for class_name, dets in detections['classes'].items():
            color = colors.get(class_name, (255, 255, 0))

            for det in dets:
                x1, y1, x2, y2 = int(det['x1']), int(det['y1']), int(det['x2']), int(det['y2'])
                conf = det['confidence']

                # Bounding Box
                cv2.rectangle(frame_with_boxes, (x1, y1), (x2, y2), color, 2)

                # Label
                label = f"{class_name} {conf:.2f}"
                cv2.putText(
                    frame_with_boxes,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2
                )

        return frame_with_boxes

    def get_detection_statistics(self) -> Dict:
        """Liefere Detektions-Statistiken."""
        if not self.detection_history:
            return {}

        total = len(self.detection_history)
        calving_count = sum(1 for d in self.detection_history if d['calving_detected'])
        avg_confidence = np.mean([d['confidence'] for d in self.detection_history])

        return {
            'total_frames_analyzed': total,
            'calving_events_detected': calving_count,
            'average_confidence': float(avg_confidence),
            'detection_rate': calving_count / total if total > 0 else 0,
        }

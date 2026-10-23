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
    """Detektor für Kalberkennungs-Events.

    Eine Kalbung meldet nur ein Modell-Befund: Fruchtblase (amniotic_sac)
    oder Kälberfüße (calf_legs) mit Konfidenz > 0.80 — dieselbe Regel wie
    der Austreibungs-Override der Edge-Wache (Die_Stallwache). „Kuh plus
    zweites Objekt" ist kein Geburtsbefund: Mit einem COCO-Modell meldete
    der Detektor jede Kuh neben einer zweiten Kuh oder einem Menschen als
    Kalbung. Ein Modell ohne diese Klassen meldet deshalb nie eine Kalbung.
    """

    # Geburts-Evidenz eines eigens trainierten Modells (Klassennamen).
    EVIDENZ_KLASSEN = ('amniotic_sac', 'calf_legs')
    EVIDENZ_KONFIDENZ = 0.80

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

        namen = getattr(model, 'names', None) or {}
        namen = set(namen.values()) if isinstance(namen, dict) else set(namen)
        self.kennt_evidenz = bool(namen & set(self.EVIDENZ_KLASSEN))
        if not self.kennt_evidenz:
            logger.warning(
                "Modell kennt keine Geburtsklassen (%s) – Kalbungs-Alarme sind "
                "abgeschaltet. Ein eigenes Modell mit diesen Klassen trainieren.",
                ", ".join(self.EVIDENZ_KLASSEN)
            )

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

            # Kalbungs-Logik: nur mit Modell-Befund
            beleg = self._geburts_beleg(detections)
            calving_detected = beleg is not None

            detection_result = {
                'calving_detected': calving_detected,
                'confidence': beleg if calving_detected else detections.get('max_confidence', 0.0),
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

    def _geburts_beleg(self, detections: Dict) -> Optional[float]:
        """Höchste Konfidenz einer Geburts-Evidenz über der Schwelle, sonst None.

        Kein Zeitfilter: Fruchtblase und Kälberfüße sind ein Notfall, jede
        einzelne Erkennung zählt (Recall vor Präzision).
        """
        beleg = None
        for klasse in self.EVIDENZ_KLASSEN:
            for det in detections.get('classes', {}).get(klasse, []):
                if det['confidence'] > self.EVIDENZ_KONFIDENZ:
                    beleg = max(beleg or 0.0, det['confidence'])
        if beleg is not None:
            logger.debug(f"Geburts-Evidenz erkannt | Konfidenz: {beleg:.2f}")
        return beleg

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

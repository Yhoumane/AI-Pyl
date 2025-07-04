import os
import cv2
import base64
import numpy as np
from ultralytics import YOLO
from typing import Dict

def segment_image(image_path: str, model_path: str = os.path.join(os.path.dirname(__file__), "rust_best.pt")) -> Dict:
    """
    Applique une segmentation avec un modèle YOLOv8 et renvoie l'image segmentée encodée en base64
    """
    try:
        # Vérification des fichiers
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"Image introuvable : {image_path}")

        if not os.path.isfile(model_path):
            raise FileNotFoundError(f"Modèle introuvable : {model_path}")

        # Chargement du modèle
        model = YOLO(model_path)

        # Prédiction
        results = model.predict(
            source=image_path,
            imgsz=640,
            conf=0.25,
            iou=0.5,
            save=False,
            device=0
        )

        result = results[0]

        if result.masks is None:
            return {
                "corroded": False,
                "message": "✅ Pas de corrosion détectée",
                "image_base64": ""
            }

        # Affichage du masque sur l'image
        image = cv2.imread(image_path)
        mask_img = result.plot()

        # Encodage en base64
        _, buffer = cv2.imencode('.jpg', mask_img)
        image_base64 = base64.b64encode(buffer).decode('utf-8')

        return {
            "corroded": True,
            "message": "⚠️ Image corrodée détectée",
            "image_base64": image_base64
        }

    except Exception as e:
        return {"error": f"Erreur de traitement : {str(e)}"}

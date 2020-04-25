from typing import List

from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
import numpy as np


class Predictor:
    """
    Class that contains model for predicting bounding boxes of people
    """

    def __init__(self, model_yaml: str, model_weights: str, threshold: float = 0.85):
        """
        Model initialiser
        :param model_yaml: Path to model .yaml config
        :param model_weights: Path to model .pkl weights
        :param threshold: Minimum probability to filter weak detections
        """
        cfg = get_cfg()
        cfg.merge_from_file(model_yaml)
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold  # set threshold for this model
        cfg.MODEL.WEIGHTS = model_weights
        self.predictor = DefaultPredictor(cfg)

    def predict(self, frame: np.ndarray, label: int) -> List[dict]:
        """
        Detect bounding boxes of people on picture
        :param frame: Picture as np.ndarray
        :param label: Label id of object to detect
        :return: List of boxes as dicts with keys 'leftup' and 'rightdown', each having 'x' and 'y' coordinates
        """
        outputs = self.predictor(frame)
        boxes = []
        for m in outputs['instances'].get_fields()['pred_boxes'][
            outputs['instances'].get_fields()['pred_classes'] == label]:
            boxes.append({
                'leftup': {
                    'x': int(m[0].item()),
                    'y': int(m[1].item())
                },
                'rightdown': {
                    'x': int(m[2].item()),
                    'y': int(m[3].item())
                }

            })
        return boxes

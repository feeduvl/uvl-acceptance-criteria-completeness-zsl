"""
This module provides a class for deserializing ground truth data from a JSON file.
"""
import json
from typing import List, Tuple
import jsons

from models.ground_truth import GroundTruth
from models.output_data import ACConcepts, ExtractionOutput


class GroundTruthDeserializer:
    """
    A class for deserializing ground truth data from a JSON file.
    """

    @staticmethod
    def from_json_file(file_path: str) -> List[GroundTruth]:
        """
        Deserialize ground truth data from a JSON file.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            List[GroundTruth]: A list of GroundTruth objects deserialized from the JSON file.
        """
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        return [jsons.load(item, GroundTruth) for item in data]

    @staticmethod
    def extraction_output_from_gt(gt: List[GroundTruth]) -> List[ExtractionOutput]:
        outputs: List[ExtractionOutput] = []
        for item in gt:
            us_concepts: List[Tuple[str, str]] = []
            for concept in item.gt_us_concepts:
                us_concepts.append(("", concept))
            acceptance_criteria: List[ACConcepts] = []
            for ac in item.gt_acceptance_criteria_concepts:
                ac_concepts: List[Tuple[str, str]] = []
                for concept in ac:
                    ac_concepts.append(("", concept))
                acceptance_criteria.append(ACConcepts("", ac_concepts))
            outputs.append(
                ExtractionOutput(
                    item.number,
                    item.id,
                    "",
                    us_concepts,
                    acceptance_criteria,
                )
            )

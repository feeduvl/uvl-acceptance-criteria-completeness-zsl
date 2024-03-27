from typing import List, Set, Tuple

from models.ground_truth import (
    BasicConceptComparison,
    ConceptComparison,
    GroundTruth,
)
from models.output_data import ExtractionOutput
from models.params import PerformanceParams


class ExtractionPerformance:
    """
    A class for measuring the performance of the extraction process.
    """

    @staticmethod
    def measure_extraction_performance(
        ground_truth: List[GroundTruth],
        extracted: List[ExtractionOutput],
        params: PerformanceParams,
    ) -> Tuple[List[ConceptComparison], List[ConceptComparison]]:
        """
        Measure the performance of the extraction process.

        Args:
            ground_truth (List[GroundTruth]): The ground truth data.
            extracted (List[ExtractionOutput]): The extracted data.

        Returns:
            float: The performance of the extraction process.
        """
        result_list_gt_to_algo: List[ConceptComparison] = []
        result_list_algo_to_gt: List[ConceptComparison] = []
        for extraction_output in extracted:
            gt = ExtractionPerformance.get_gt_from_list(
                ground_truth, extraction_output.id
            )

            us_concepts_gt = gt.gt_us_concepts
            us_concepts_extracted = [
                concept[1] for concept in extraction_output.us_concepts
            ]
            us_gt_to_algo, us_algo_to_gt = ExtractionPerformance.__compare_concepts(
                us_concepts_gt,
                us_concepts_extracted,
            )
            us_gt_to_algo = [
                ConceptComparison(
                    extraction_output.id,
                    extraction_output.us_text,
                    "",
                    concept.concept,
                    concept.mapped_concepts,
                    concept.unmapped_concepts,
                    concept.case_str,
                    concept.case_int,
                    concept.case_1_num,
                    concept.case_2_num,
                    concept.case_3_num,
                    concept.case_4_num,
                    concept.case_5_num,
                )
                for concept in us_gt_to_algo
            ]
            us_algo_to_gt = [
                ConceptComparison(
                    extraction_output.id,
                    extraction_output.us_text,
                    "",
                    concept.concept,
                    concept.mapped_concepts,
                    concept.unmapped_concepts,
                    concept.case_str,
                    concept.case_int,
                    concept.case_1_num,
                    concept.case_2_num,
                    concept.case_3_num,
                    concept.case_4_num,
                    concept.case_5_num,
                )
                for concept in us_algo_to_gt
            ]
            result_list_gt_to_algo.extend(us_gt_to_algo)
            result_list_algo_to_gt.extend(us_algo_to_gt)

            for ac in extraction_output.acceptance_criteria:
                ac_concepts_gt = gt.gt_acceptance_criteria_concepts[
                    extraction_output.acceptance_criteria.index(ac)
                ]
                ac_concepts_extracted = [concept[1] for concept in ac.ac_concepts]
                ac_gt_to_algo, ac_algo_to_gt = ExtractionPerformance.__compare_concepts(
                    ac_concepts_gt, ac_concepts_extracted
                )
                ac_gt_to_algo = [
                    ConceptComparison(
                        extraction_output.id,
                        "",
                        ac.ac_text,
                        concept.concept,
                        concept.mapped_concepts,
                        concept.unmapped_concepts,
                        concept.case_str,
                        concept.case_int,
                        concept.case_1_num,
                        concept.case_2_num,
                        concept.case_3_num,
                        concept.case_4_num,
                        concept.case_5_num,
                    )
                    for concept in ac_gt_to_algo
                ]
                ac_algo_to_gt = [
                    ConceptComparison(
                        extraction_output.id,
                        "",
                        ac.ac_text,
                        concept.concept,
                        concept.mapped_concepts,
                        concept.unmapped_concepts,
                        concept.case_str,
                        concept.case_int,
                        concept.case_1_num,
                        concept.case_2_num,
                        concept.case_3_num,
                        concept.case_4_num,
                        concept.case_5_num,
                    )
                    for concept in ac_algo_to_gt
                ]
                result_list_gt_to_algo.extend(ac_gt_to_algo)
                result_list_algo_to_gt.extend(ac_algo_to_gt)

        return result_list_gt_to_algo, result_list_algo_to_gt

    @staticmethod
    def __compare_concepts(
        first_concepts: List[str],
        second_concepts: List[str],
    ) -> Tuple[List[BasicConceptComparison], List[BasicConceptComparison]]:
        """
        Compare two lists of concepts.

        Args:
            first_concepts (List[str]): The first list of concepts.
            second_concepts (List[str]): The second list of concepts.

        Returns:
            Tuple[List[BasicConceptComparison], List[BasicConceptComparison]]: The comparison results.
        """
        first_concept_comparisons = ExtractionPerformance.__compare_two_concept_lists(
            first_concepts, second_concepts
        )
        second_concept_comparisons = ExtractionPerformance.__compare_two_concept_lists(
            second_concepts, first_concepts
        )
        return first_concept_comparisons, second_concept_comparisons

    @staticmethod
    def __compare_two_concept_lists(
        first_concepts: List[str], second_concepts: List[str]
    ) -> List[BasicConceptComparison]:
        first_concept_comparisons: List[BasicConceptComparison] = []

        for concept in first_concepts:
            mapped_concepts: List[Tuple[str, int]] = []
            unmapped_concepts: List[str] = []
            min_case_int = 6
            min_case_str = ""
            if concept == "":
                case_str = "Different"
                case_int = 5
                first_concept_comparisons.append(
                    BasicConceptComparison(
                        concept,
                        mapped_concepts,
                        unmapped_concepts,
                        case_str,
                        case_int,
                        0,
                        0,
                        0,
                        0,
                        0,
                    )
                )

            case_1_num = 0
            case_2_num = 0
            case_3_num = 0
            case_4_num = 0
            case_5_num = 0
            for concept2 in second_concepts:
                if concept2 == "":
                    case_str = "Different"
                    case_int = 5
                else:
                    case_str, case_int = ExtractionPerformance.__compare_two_concepts(
                        concept, concept2
                    )
                if case_int < 5:
                    mapped_concepts.append((concept2, case_int))
                else:
                    unmapped_concepts.append(concept2)
                if case_int < min_case_int:
                    min_case_int = case_int
                    min_case_str = case_str
                if case_int == 1:
                    case_1_num += 1
                elif case_int == 2:
                    case_2_num += 1
                elif case_int == 3:
                    case_3_num += 1
                elif case_int == 4:
                    case_4_num += 1
                elif case_int == 5:
                    case_5_num += 1
            first_concept_comparisons.append(
                BasicConceptComparison(
                    concept,
                    mapped_concepts,
                    unmapped_concepts,
                    min_case_str,
                    min_case_int,
                    case_1_num,
                    case_2_num,
                    case_3_num,
                    case_4_num,
                    case_5_num,
                )
            )
        return first_concept_comparisons

    @staticmethod
    def __compare_two_concepts(concept1: str, concept2: str) -> Tuple[str, int]:
        """
        Compare two concepts word by word.

        Args:
            concept1 (str): The first concept.
            concept2 (str): The second concept.

        Returns:
            Tuple[str, int]: The comparison result.
        """
        words1 = concept1.lower().split()
        words2 = concept2.lower().split()

        words_1_set = set(words1)
        words_2_set = set(words2)

        words_1_set_used = dict.fromkeys(words_1_set, 0)
        words_2_set_used = dict.fromkeys(words_2_set, 0)

        equal_count = 0
        for word1 in words1:
            for word2 in words2:
                if (
                    word1 == word2
                    and words_1_set_used[word1] == 0
                    and words_2_set_used[word2] == 0
                ):
                    equal_count += 1
                    words_1_set_used[word1] = 1
                    words_2_set_used[word2] = 1
                    break

        if equal_count == len(words1) == len(words2):
            return "Equal", 1
        elif equal_count == len(words1):
            return "Subset", 2
        elif equal_count == len(words2):
            return "Superset", 3
        elif equal_count > 0:
            return "Intersection", 4
        else:
            return "Different", 5

    @staticmethod
    def get_gt_from_list(ground_truth: List[GroundTruth], us_id: str) -> GroundTruth:
        """
        Get the ground truth for a specific user story.

        Args:
            ground_truth (List[GroundTruth]): The ground truth data.
            us_id (str): The id of the user story.

        Returns:
            GroundTruth: The ground truth for the user story.
        """
        for gt in ground_truth:
            if gt.id == us_id:
                return gt
        raise ValueError(f"Ground truth for user story with id '{us_id}' not found.")

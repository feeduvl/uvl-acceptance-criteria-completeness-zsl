from typing import List
from models.ground_truth import GroundTruth, GroundTruthCompleteResult
from models.output_data import CompletionOutput
from models.params import PerformanceParams


class CompletePerformance:
    """
    This class is responsible for measuring the complete performance.
    """

    @staticmethod
    def measure_complete_performance(
        params: PerformanceParams,
        ground_truth: List[GroundTruth],
        completion_output: List[CompletionOutput],
    ) -> List[GroundTruthCompleteResult]:
        """
        Measures the complete performance based on the provided ground truth and completion output.

        Args:
            params (PerformanceParams): The performance parameters.
            ground_truth (List[GroundTruth]): The list of ground truth data.
            completion_output (List[CompletionOutput]): The list of completion output data.

        Returns:
            List[GroundTruthCompleteResult]: The list of complete performance results for each ground truth.

        """
        complete_performance_results = []
        for gt in ground_truth:
            matching_completion_output = (
                CompletePerformance.get_completion_output_from_list(
                    completion_output, gt.id
                )
            )
            if matching_completion_output:
                gt_case_str = CompletePerformance.get_case_str(
                    gt.gt_complete, matching_completion_output.complete
                )
                gt_case_int = CompletePerformance.get_case_int(
                    gt.gt_complete, matching_completion_output.complete
                )
                gt_complete_result = GroundTruthCompleteResult(
                    gt.id, gt_case_str, gt_case_int
                )
            complete_performance_results.append(gt_complete_result)
        return complete_performance_results

    @staticmethod
    def get_completion_output_from_list(
        completion_output: List[CompletionOutput], id: str
    ) -> CompletionOutput:
        """
        Retrieves the MappingOutput object from the given list based on the provided id.

        Args:
            mapping_output (List[MappingOutput]): The list of CompletionOutput objects.
            id (str): The id of the CompletionOutput object to retrieve.

        Returns:
            CompletionOutput: The CompletionOutput object with the matching id, or None if not found.
        """
        for mapping in completion_output:
            if mapping.id == id:
                return mapping
        return None

    @staticmethod
    def get_case_str(gt_complete: bool, algo_complete: bool) -> str:
        """
        Returns a string representing the case based on the ground truth completeness and ground truth concept completeness.

        Parameters:
        gt_complete (bool): Indicates if the ground truth is complete.
        gt_concept_complete (bool): Indicates if the ground truth concept is complete.

        Returns:
        str: The case string, which can be one of the following: "TP" (True Positive), "FN" (False Negative), "FP" (False Positive), or "TN" (True Negative).
        """
        if gt_complete and algo_complete:
            return "TP"
        elif gt_complete and not algo_complete:
            return "FN"
        elif not gt_complete and algo_complete:
            return "FP"
        else:
            return "TN"

    @staticmethod
    def get_case_int(gt_complete: bool, algo_complete: bool) -> int:
        """
        Determines the case integer based on the completeness of ground truth and ground truth concept.

        Args:
            gt_complete (bool): Indicates if the ground truth is complete.
            algo_complete (bool): Indicates if the algo result is complete.

        Returns:
            int: The case integer, which can be one of the following: 1 (True Positive), 2 (False Negative), 3 (False Positive), or 4 (True Negative).
        """
        if gt_complete and algo_complete:
            return 1
        elif gt_complete and not algo_complete:
            return 2
        elif not gt_complete and algo_complete:
            return 3
        else:
            return 4

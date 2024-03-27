"""
This module provides a class for writing performance output to a file.
"""

from typing import List, Tuple, TypedDict
import pandas as pd
from models.ground_truth import ConceptComparison


class WriteExtractionPerformanceOutput:
    """
    A class for writing performance output to a file.
    """

    def __init__(
        self, output_file_name, output_file_extension=".xlsx", output_path="./results/"
    ):
        """
        Initializes a WritePerformanceOutput object.

        Args:
            output_path (str): The path where the output file will be saved.
            output_file_name (str): The name of the output file.
            output_file_extension (str): The file extension of the output file.
        """
        self.output_path = output_path
        self.output_file_name = output_file_name
        self.output_file_extension = output_file_extension

    class ExcelRow(TypedDict):
        """
        Represents a row in the Excel file.
        """

        user_story_id: str
        user_story: str
        acceptance_citerion: str
        gt_concepts: str
        extracted_concepts: str
        comparison_case: str
        case_int: int
        mapping_from_gt_to_extracted: str
        mapping_from_extracted_to_gt: str
        gt_concepts_not_in_extracted: str
        extracted_concepts_not_in_gt: str

    def write_output(
        self, output: Tuple[List[ConceptComparison], List[ConceptComparison]]
    ):
        """
        Writes the output to an Excel file.

        Args:
            output (List[GroundTruthExtractionResult]): The output to be written to the file.
        """
        df1 = WriteExtractionPerformanceOutput.__get_df_from_results(output[0])
        df2 = WriteExtractionPerformanceOutput.__get_df_from_results(output[1])

        output_file_path = (
            self.output_path
            + self.output_file_name.replace("/", "")
            + "_extraction"
            + self.output_file_extension
        )

        with pd.ExcelWriter(output_file_path) as writer:
            df1.to_excel(writer, sheet_name="gt_to_extracted")
            df2.to_excel(writer, sheet_name="extracted_to_gt")

    @staticmethod
    def __get_df_from_results(
        concept_comparisons: List[ConceptComparison],
    ) -> pd.DataFrame:
        """
        Converts a list of ConceptComparison objects to a DataFrame.

        Args:
            concept_comparisons (List[ConceptComparison]): The ConceptComparison objects to be converted.

        Returns:
            pd.DataFrame: The ConceptComparison objects in a DataFrame.
        """
        df = pd.DataFrame()
        for concept_comparison in concept_comparisons:
            excel_row = WriteExtractionPerformanceOutput.convert_to_excel_format(
                concept_comparison
            )
            df_dictionary = pd.DataFrame([excel_row])
            df = pd.concat([df, df_dictionary], ignore_index=True)
        return df

    @staticmethod
    def convert_to_excel_format(concept_comparison: ConceptComparison) -> ExcelRow:
        """
        Converts a ConceptComparison object to an Excel format.

        Args:
            concept_comparison (ConceptComparison): The ConceptComparison object to be converted.

        Returns:
            WritePerformanceOutput.ExcelRow: The ConceptComparison object in an Excel format.
        """
        excel_row = {
            "user_story_id": concept_comparison.id,
            "user_story": concept_comparison.user_story,
            "acceptance_citerion": concept_comparison.acceptance_criterion,
            "concept": concept_comparison.concept,
            "mapping": "\n".join(
                [
                    f"{mapped_concept[0]} ({mapped_concept[1]})"
                    for mapped_concept in concept_comparison.mapped_concepts
                ]
            ),
            "comparison_case": concept_comparison.case_str,
            "case_int": concept_comparison.case_int,
            "unmapped_concepts": "\n".join(concept_comparison.unmapped_concepts),
            "case_1_num": concept_comparison.case_1_num,
            "case_2_num": concept_comparison.case_2_num,
            "case_3_num": concept_comparison.case_3_num,
            "case_4_num": concept_comparison.case_4_num,
            "case_5_num": concept_comparison.case_5_num,
        }
        return excel_row

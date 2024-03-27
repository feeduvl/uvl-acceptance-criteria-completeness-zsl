from typing import List

import pandas as pd

from models.ground_truth import GroundTruthCompleteResult


class CompletePerformanceOutputWriter:
    """
    A class for writing performance output to a file.
    """

    def __init__(
        self, output_file_name, output_file_extension=".xlsx", output_path="./results/"
    ):
        """
        Initializes a CompletePerformanceOutputWriter object.

        Args:
            output_path (str): The path where the output file will be saved.
            output_file_name (str): The name of the output file.
            output_file_extension (str): The file extension of the output file.
        """
        self.output_path = output_path
        self.output_file_name = output_file_name + "_complete"
        self.output_file_extension = output_file_extension

    def write_output(self, output: List[GroundTruthCompleteResult]):
        """
        Writes the output to an Excel file.

        Args:
            output (List[GroundTruthCompleteResult]): The output to be written to the file.
        """
        df = pd.DataFrame()
        for result in output:
            user_story_id = result.id
            case_str = result.case_str
            case_int = result.case_int
            excel_row = {
                "User Story ID": user_story_id,
                "Case Str": case_str,
                "Case Int": case_int,
            }

            df_dictionary = pd.DataFrame([excel_row])
            df = pd.concat([df, df_dictionary], ignore_index=True)
        output_file_path = (
            self.output_path
            + self.output_file_name.replace("/", "")
            + self.output_file_extension
        )
        df.to_excel(output_file_path, index=False)

import json
from typing import List, Tuple

from models.input_data import InputData
from models.params import ExtractionParams, MappingParams, PerformanceParams


class InputReader:

    @staticmethod
    def read_json(documents) -> List[InputData]:
        input_data_list = []
        for document in documents:
            input_data = InputData(
                number=document["number"],
                user_story_text=InputReader.get_user_story_text(document),
                acceptance_criteria=InputReader.get_acceptance_criteria_text(document),
                id=document["id"]
            )
            input_data_list.append(input_data)
        return input_data_list
    
    @staticmethod
    def read_params_json(params) -> Tuple[ExtractionParams, MappingParams, PerformanceParams]:
        extraction_params = ExtractionParams(
            data_file_name=None,
            model_name=params["extraction_model"],
            num=1000,
            method=""
        )
        mapping_params = MappingParams(
            output_scores=True,
            threshold=params["mapping_threshold"],
            use_cosine_similarity=True
        )
        performance_params = None
        return extraction_params, mapping_params, performance_params

    @staticmethod
    def read(input_file, number_of_user_stories) -> List[InputData]:
        with open(f"./data/{input_file}.json") as json_file:
            dataset = json.load(json_file)
        questions_split = dataset["documents"][:number_of_user_stories]
        input_data_list = []
        for document in questions_split:
            input_data = InputData(
                number=document["number"],
                user_story_text=InputReader.get_user_story_text(document),
                acceptance_criteria=InputReader.get_acceptance_criteria_text(document),
                id=document["id"]
            )
            input_data_list.append(input_data)
        return input_data_list

    @staticmethod
    def get_user_story_text(document):
        """
        Get user story text from document
        """
        user_story_text = document["text"].split("###")[1].replace("\n", " ").replace("*", "").strip().lower()

        # Find first parentheses, and if there is text between parentheses, remove it
        first_parentheses_position = user_story_text.find("(")
        if first_parentheses_position > 0:
            second_parentheses_position = user_story_text.find(")")
            if second_parentheses_position > 0:
                user_story_text = user_story_text[:first_parentheses_position] + user_story_text[
                                                                                second_parentheses_position + 1:]

        i_want_position = user_story_text.find("i want")
        so_that_position = user_story_text.find("so that")

        user_story_text = user_story_text[i_want_position:so_that_position]

        return user_story_text

    @staticmethod
    def get_acceptance_criteria_text(document):
        """
        Get acceptance criteria text from document
        """
        acceptance_criteria_text = document["text"].split("###")[2]
        acceptance_criteria_texts_split = []

        for single_acceptance_criteria_text in acceptance_criteria_text.split("+++"):
            single_acceptance_criteria_text_clean = single_acceptance_criteria_text.replace("\n",
                                                                                            "").replace("*", "").strip()
            if len(single_acceptance_criteria_text_clean) > 5:
                acceptance_criteria_texts_split.append(single_acceptance_criteria_text_clean)
        return acceptance_criteria_texts_split

from typing import List, Tuple

from models.output_data import ACMapping, CompletionOutput, MappingOutput
from sklearn.feature_extraction.text import TfidfVectorizer


class CompletionCalculation:
    """
    A class that provides methods for calculating completeness.
    """

    COMPLETENESS_THRESHOLD = 0.5

    @staticmethod
    def calculate_completeness(
        ac_mappings: List[ACMapping], us_concepts: List[Tuple[str, str]]
    ) -> float:
        """
        Calculates the completeness of the AC mappings based on the given US concepts.

        Args:
            ac_mappings (List[ACMapping]): List of AC mappings.
            us_concepts (List[Tuple[str, str]]): List of US concepts.

        Returns:
            float: The completeness value, which is the ratio of mapped US concepts to total US concepts.
        """
        num_us_concepts = len(us_concepts)
        set_of_mapped_us_concepts = set()
        for us_concept in us_concepts:
            for ac_mapping in ac_mappings:
                for found_concept in ac_mapping.mapping.keys():
                    if CompletionCalculation.compare_strings(
                        us_concept[1], found_concept
                    ):
                        set_of_mapped_us_concepts.add(us_concept)
        num_mapped_us_concepts = len(set_of_mapped_us_concepts)
        return num_mapped_us_concepts / num_us_concepts

    @staticmethod
    def compare_strings(str1: str, str2: str) -> bool:
        """
        Compares two strings and returns True if they are equal, False otherwise.

        Args:
            str1 (str): The first string.
            str2 (str): The second string.

        Returns:
            bool: True if the strings are equal, False otherwise.
        """
        threshold = 0.5
        vectorizer = TfidfVectorizer()
        try:
            vectorizer.fit([str1, str2])
        except ValueError:
            return False
        gt_vector = vectorizer.transform([str1])
        extracted_vector = vectorizer.transform([str2])
        cosine_similarity = gt_vector.dot(extracted_vector.T).toarray()[0][0]
        return cosine_similarity >= threshold

    @staticmethod
    def calculate_completeness_bool(
        ac_mappings: List[ACMapping], us_concepts: List[Tuple[str, str]], threshold: float = 0.5
    ) -> bool:
        """
        Calculates the boolean completeness between ground truth concepts and algorithm concepts.

        Args:
            gt_concepts (List[Concept]): The list of ground truth concepts.
            algo_concepts (List[Concept]): The list of algorithm concepts.

        Returns:
            bool: True if completeness is 1.0, False otherwise.
        """
        return (
            CompletionCalculation.calculate_completeness(ac_mappings, us_concepts)
            > threshold
        )

    @staticmethod
    def calculate_completeness_for_mapping_result(
        mapping_results: List[MappingOutput], threshold: float = 0.5
    ) -> List[CompletionOutput]:
        """
        Calculates the completeness for each mapping result in the given list.

        Args:
            mapping_results (List[MappingOutput]): A list of MappingOutput objects.

        Returns:
            List[CompletionOutput]: A list of CompletionOutput objects representing the completeness of each mapping result.
        """
        completion_outputs = []
        for output in mapping_results:
            completeness_numerical = CompletionCalculation.calculate_completeness(
                output.ac_mappings, output.us_concepts
            )
            completeness = CompletionCalculation.calculate_completeness_bool(
                output.ac_mappings, output.us_concepts, threshold
            )
            completion_output = CompletionOutput(
                output.number,
                output.id,
                output.user_story_text,
                output.ac_mappings,
                output.us_concepts,
                output.scores,
                completeness_numerical,
                completeness,
            )
            completion_outputs.append(completion_output)
        return completion_outputs

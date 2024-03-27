import dataclasses
import json
from typing import List

from models.output_data import CompletionOutput, ExtractionOutput, MappingOutput


class OutputWriter(object):
    """
    A class that provides methods for writing output data to JSON files.
    """

    @staticmethod
    def write(
        output_name_extraction, result_extraction, output_name_mapping, result_mapping
    ):
        """
        Writes the extraction and mapping results to JSON files.

        Parameters:
        - output_name_extraction (str): The name of the extraction output file.
        - result_extraction (dict): The extraction results to be written.
        - output_name_mapping (str): The name of the mapping output file.
        - result_mapping (dict): The mapping results to be written.
        """

        class EnhancedJSONEncoder(json.JSONEncoder):
            """
            A custom JSON encoder that enhances the default behavior of the JSONEncoder class.

            This encoder is capable of serializing dataclasses by converting them to dictionaries using the `dataclasses.asdict()` function.

            Usage:
            encoder = EnhancedJSONEncoder()
            json_data = encoder.encode(my_object)
            """

            def default(self, o):
                if dataclasses.is_dataclass(o):
                    return dataclasses.asdict(o)
                return super().default(o)

        with open(
            f"./results/{output_name_extraction}.json", "w", encoding="utf-8"
        ) as output_file:
            json.dump(result_extraction, output_file, indent=4, cls=EnhancedJSONEncoder)

        if result_mapping is not None:
            with open(
                f"./results/{output_name_mapping}.json", "w", encoding="utf-8"
            ) as output_file:
                json.dump(
                    result_mapping, output_file, indent=4, cls=EnhancedJSONEncoder
                )

    @staticmethod
    def write_all_to_json(extraction_output: List[ExtractionOutput], mapping_output: List[MappingOutput], completion_output: List[CompletionOutput]):
        """
        Returns the extraction, mapping, and completion results as JSON.
        """

        rows = []

        for extraction in extraction_output:
            id = extraction.id
            # Find the corresponding mapping output
            mapping = next((m for m in mapping_output if m.id == id), None)
            # Find the corresponding completion output
            completion = next((c for c in completion_output if c.id == id), None)
            mappings = []
            positions_found = []
            for word in mapping.user_story_text.split():
                # Check if word has alrady been found:
                for position_start, position_end in positions_found:
                    if mapping.user_story_text.split().index(word) >= position_start and mapping.user_story_text.split().index(word) <= position_end:
                        continue
                concept_found_for_word = False
                for _, concept in mapping.us_concepts:
                    for concept_word in concept.split():
                        if word == concept_word:
                            concept_words = concept.split()
                            if len(mapping.user_story_text.split()) - mapping.user_story_text.split().index(word) >= len(concept_words):
                                user_story_potential_match_words = mapping.user_story_text.split()[mapping.user_story_text.split().index(word):mapping.user_story_text.split().index(word) + len(concept_words)]
                                if user_story_potential_match_words == concept_words:
                                    for word in user_story_potential_match_words:
                                        mappings.append({"annotation": "non-complete", "text": word})
                                    positions_found.append((mapping.user_story_text.split().index(word), mapping.user_story_text.split().index(word) + len(concept_words)))
                                    concept_found_for_word = True
                if not concept_found_for_word:
                    mappings.append({"annotation": "no-concept", "text": word})

            ac_mappings = []
            for ac_mapping in mapping.ac_mappings:
                for ac in ac_mapping.ac_text.split():
                    ac_mappings.append({"annotation": "no-concept", "text":ac})
            rows.append({
                "id": id,
                "mapping": mappings,
                "acMapping": ac_mappings,
            })
            

        output = {
            "topics": {
                "completeness_results": rows
            },
            "doc_topic": None,
            "metrics": {},
            "codes": None
        }

        return output

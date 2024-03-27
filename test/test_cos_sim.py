import unittest
from mapping.cos_sim import map_concepts
from models.output_data import ExtractionOutput, ACConcepts, MappingOutput
from models.params import MappingParams

class TestMapConcepts(unittest.TestCase):

    def test_map_concepts(self):
        extraction_results = [
            ExtractionOutput(
                number=1,
                id="doc1",
                us_text="",
                us_concepts=[("", "concept1"), ("", "concept2")],
                acceptance_criteria=[ACConcepts("", [("", "concept3"), ("", "concept4")])]
            )
        ]
        params = MappingParams(
            output_scores=True,
            threshold=0.5,
            use_cosine_similarity=True
        )
        output = map_concepts(extraction_results, params)
        # Check that the output is a list
        self.assertIsInstance(output, list)
        # Check that the output list is not empty
        self.assertTrue(output)
        # Check that the first item in the output list is a MappingOutput instance
        self.assertIsInstance(output[0], MappingOutput)

if __name__ == '__main__':
    unittest.main()
import unittest
from input_data.read_input import InputReader
from models.input_data import InputData
from models.params import ExtractionParams, MappingParams, PerformanceParams

class TestInputReader(unittest.TestCase):

    def test_read_json(self):
        documents = [
            {
                "number": 1,
                "text": "### as a something I want to test this function so that it is### this is the acceptance criteria",
                "id": "doc1"
            }
        ]
        expected_output = [
            InputData(
                number=1,
                user_story_text="i want to test this function ",
                acceptance_criteria=["this is the acceptance criteria"],
                id="doc1"
            )
        ]
        self.assertEqual(InputReader.read_json(documents), expected_output)

    def test_read_params_json(self):
        params = {
            "extraction_model": "model1",
            "mapping_threshold": 0.5
        }
        expected_output = (
            ExtractionParams(
                data_file_name=None,
                model_name="model1",
                num=1000,
                method=""
            ),
            MappingParams(
                output_scores=True,
                threshold=0.5,
                use_cosine_similarity=True
            ),
            None
        )
        self.assertEqual(InputReader.read_params_json(params), expected_output)

if __name__ == '__main__':
    unittest.main()
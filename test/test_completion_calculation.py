import unittest
from completion_calculation.completion_calculation import CompletionCalculation
from models.output_data import ACMapping

class TestCompletionCalculation(unittest.TestCase):

    def test_calculate_completeness(self):
        ac_mappings = [
            ACMapping(ac_text="AC1", ac_concepts=[["","Description 1"]], mapping={}),
            ACMapping(ac_text="AC1", ac_concepts=[["","Description 2"]], mapping={}),
            ACMapping(ac_text="AC1", ac_concepts=[["","Description 3"]], mapping={}),
        ]
        us_concepts = [
            ("Concept1", "Description 1"),
            ("Concept2", "Description 2"),
            ("Concept3", "Description 3"),
        ]
        completeness = CompletionCalculation.calculate_completeness(ac_mappings, us_concepts)
        self.assertEqual(completeness, 0.0)  # Add your expected value here

    def test_compare_strings(self):
        str1 = "Hello"
        str2 = "hello"
        result = CompletionCalculation.compare_strings(str1, str2)
        self.assertTrue(result)  # Add your expected value here

    def test_calculate_completeness_bool(self):
        ac_mappings = [
            ACMapping(ac_text="AC1", ac_concepts=[["","Description 1"]], mapping={}),
            ACMapping(ac_text="AC1", ac_concepts=[["","Description 2"]], mapping={}),
            ACMapping(ac_text="AC1", ac_concepts=[["","Description 3"]], mapping={}),
        ]
        us_concepts = [
            ("Concept1", "Description 1"),
            ("Concept2", "Description 2"),
            ("Concept3", "Description 3"),
        ]
        threshold = 0.5
        completeness_bool = CompletionCalculation.calculate_completeness_bool(ac_mappings, us_concepts, threshold)
        self.assertFalse(completeness_bool)  # Add your expected value here

if __name__ == '__main__':
    unittest.main()

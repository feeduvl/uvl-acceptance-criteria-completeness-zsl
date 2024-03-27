import unittest
import os
from output_data.write_output import OutputWriter
from models.output_data import ExtractionOutput, MappingOutput, CompletionOutput

class TestOutputWriter(unittest.TestCase):

    def test_write(self):
        output_name_extraction = 'test_extraction'
        result_extraction = {'key': 'value'}
        output_name_mapping = 'test_mapping'
        result_mapping = {'key': 'value'}
        OutputWriter.write(output_name_extraction, result_extraction, output_name_mapping, result_mapping)
        # Check if the files are created
        self.assertTrue(os.path.isfile(f'./results/{output_name_extraction}.json'))
        self.assertTrue(os.path.isfile(f'./results/{output_name_mapping}.json'))
        # Clean up
        os.remove(f'./results/{output_name_extraction}.json')
        os.remove(f'./results/{output_name_mapping}.json')

    def test_write_all_to_json(self):
        extraction_output = [ExtractionOutput(number=1, id='doc1', us_text='', us_concepts=[], acceptance_criteria=[])]
        mapping_output = [MappingOutput(number=1, id='doc1', user_story_text='', ac_mappings=[], us_concepts=[], scores=[])]
        completion_output = [CompletionOutput(id='doc1', user_story_text='', us_concepts=[], ac_mappings=[], number=None, scores=[], completeness_numerical=.5, complete=False)]
        output = OutputWriter.write_all_to_json(extraction_output, mapping_output, completion_output)
        # Check that the output is a dictionary
        self.assertIsInstance(output, dict)
        # Check that the output dictionary has the correct keys
        self.assertListEqual(list(output.keys()), ['topics', 'doc_topic', 'metrics', 'codes'])

if __name__ == '__main__':
    unittest.main()
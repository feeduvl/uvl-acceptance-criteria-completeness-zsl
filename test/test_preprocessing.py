import unittest
from preprocessing.preprocessing import full_preprocessing, get_tokenized_list, word_stemmer, remove_stopwords, remove_punctuation

class TestPreprocessing(unittest.TestCase):

    def test_full_preprocessing(self):
        doc_text = "This is a test sentence. It contains punctuation and stop words!"
        expected_output = "test sentenc contain punctuat stop word"
        self.assertEqual(full_preprocessing(doc_text), expected_output)

    def test_get_tokenized_list(self):
        doc_text = "This is a test sentence."
        expected_output = ['This', 'is', 'a', 'test', 'sentence', '.']
        self.assertEqual(get_tokenized_list(doc_text), expected_output)

    def test_word_stemmer(self):
        token_list = ['running', 'jumps', 'leaves']
        expected_output = ['run', 'jump', 'leav']
        self.assertEqual(word_stemmer(token_list), expected_output)

    def test_remove_stopwords(self):
        token_list = ['This', 'is', 'a', 'test', 'sentence', '.']
        expected_output = ['test', 'sentence', '.']
        self.assertEqual(remove_stopwords(token_list), expected_output)

    def test_remove_punctuation(self):
        doc_text = "This is a test sentence. It contains punctuation!"
        expected_output = "This is a test sentence It contains punctuation"
        self.assertEqual(remove_punctuation(doc_text), expected_output)

if __name__ == '__main__':
    unittest.main()
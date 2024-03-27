from typing import List, Tuple

from transformers import pipeline

from models.input_data import InputData
from models.output_data import QAOutput, ExtractionOutput, ACConcepts


class QuestionAnswering:
    def __init__(self, model_name):
        self.nlp = pipeline(
            "question-answering", model=model_name, tokenizer=model_name
        )

    def fetch_answers(self, question, document):
        QA_input = {"question": question, "context": document}
        res = self.nlp(QA_input)
        res = res["answer"].strip()

        # Remove trailing or starting punctuation
        while len(res) > 0 and (
            res[0] in [".", ",", "!", "?", " "] or res[-1] in [".", ",", "!", "?", " "]
        ):
            if res[0] in [".", ",", "!", "?", " "]:
                res = res[1:]
            if len(res) > 0 and res[-1] in [".", ",", "!", "?", " "]:
                res = res[:-1]

        return res

    def do_qa_for_document(
        self, document: InputData, questions_to_ask: list[str]
    ) -> list[QAOutput]:
        outputs = []
        for question in questions_to_ask:
            question_keyword = question.split(" ")[3]

            us_answer = (
                question_keyword,
                self.fetch_answers(question, document.user_story_text),
            )
            answers_ac: list[ACConcepts] = []

            for single_ac_text in document.acceptance_criteria:
                initial_ac_text = single_ac_text
                single_ac_answers: List[Tuple[str, str]] = []

                ac_iterations = 3

                while len(initial_ac_text) > 5:
                    ac_answer = self.fetch_answers(question, initial_ac_text)
                    if ac_answer != "":
                        single_ac_answers.append((question_keyword, ac_answer))
                    lower_ac_text = initial_ac_text.lower()
                    position_to_remove = lower_ac_text.find(ac_answer.lower())
                    initial_ac_text = (
                        initial_ac_text[:position_to_remove]
                        + initial_ac_text[position_to_remove + len(ac_answer) :]
                    )

                    ac_iterations -= 1
                    if ac_iterations == 0:
                        break

                answers_ac.append(ACConcepts(single_ac_text, single_ac_answers))

            outputs.append(
                QAOutput(
                    question,
                    us_answer,
                    answers_ac,
                    document.number,
                    document.user_story_text,
                    document.id,
                )
            )
        return outputs

    def extract_concepts(self, documents: List[InputData]) -> List[ExtractionOutput]:
        questions = [
            "What are the interactions mentioned in the sentence?",
            "What is the data mentioned in the sentence?",
            "What is the condition mentioned in the sentence?",
        ]
        results = []
        for document in documents:
            qa_result = self.do_qa_for_document(document, questions)

            us_concepts: Tuple[List[str, str]] = []
            ac_results = []
            distinct_ac = {}

            for qa in qa_result:
                for ac in qa.ac_answers:
                    if ac.ac_text not in distinct_ac:
                        distinct_ac[ac.ac_text] = ac.ac_concepts
                    else:
                        distinct_ac[ac.ac_text].extend(ac.ac_concepts)
                us_concepts.append(qa.us_answer)
            for ac_text in distinct_ac:
                ac_results.append(ACConcepts(ac_text, distinct_ac[ac_text]))
            results.append(
                ExtractionOutput(
                    document.number,
                    document.id,
                    document.user_story_text,
                    us_concepts,
                    ac_results,
                )
            )
        results = self.remove_duplicates_from_extraction_output(results)
        return results

    def remove_duplicates_from_extraction_output(
        self, extraction_output: List[ExtractionOutput]
    ) -> List[ExtractionOutput]:
        """
        Removes duplicates from the extraction output.

        Args:
            extraction_output (List[ExtractionOutput]): The extraction output to process.

        Returns:
            List[ExtractionOutput]: The extraction output with duplicates removed.
        """
        for extraction in extraction_output:
            for ac in extraction.acceptance_criteria:
                unique_concepts: List[Tuple[str, str]] = []
                seen_concept_str: List[str] = []
                for concept in ac.ac_concepts:
                    if concept[1] not in seen_concept_str:
                        unique_concepts.append(concept)
                        seen_concept_str.append(concept[1])
                ac.ac_concepts = unique_concepts
            unique_concepts: List[Tuple[str, str]] = []
            seen_concept_str: List[str] = []
            for concept in extraction.us_concepts:
                if concept[1] not in seen_concept_str:
                    unique_concepts.append(concept)
                    seen_concept_str.append(concept[1])
            extraction.us_concepts = unique_concepts
        return extraction_output

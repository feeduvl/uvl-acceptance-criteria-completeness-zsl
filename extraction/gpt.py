"""
This module contains the GPTExtraction class for performing extraction using the GPT model.

Classes:
    GPTExtraction: Class for performing extraction using GPT model.
"""

from typing import List, Tuple
from openai import OpenAI

from models.input_data import InputData
from models.output_data import QAOutput, ExtractionOutput, ACConcepts

GPT_PROMPT_US = """
The following is a user story. Your task is to find the three most important concepts in this user story that should be covered in acceptance criteria for this user story. Do not formulate entire acceptance criteria, just write concepts separated by commas. The important part is between the role and the "so that" in the user story.
User story: {us_text}
"""

GPT_PROMPT_AC = """
The following is an acceptance criterion for a user story. Extract the three most important concepts in this acceptance criterion. Do not formulate entire acceptance criteria, just write concepts separated by commas.
Acceptance criterion: {ac_text}
"""


class GPTExtraction:
    """
    Class for performing extraction using GPT model.

    Args:
        model_name (str): The name of the GPT model.

    Attributes:
        client: The OpenAI client.
        model_name (str): The name of the GPT model.

    Methods:
        do_qa_for_document: Performs question answering for a document.
        extract_concepts: Extracts concepts from a list of documents.
    """

    def __init__(self, model_name: str):
        self.client = OpenAI()
        self.model_name = model_name

    def do_qa_for_document(self, document: InputData) -> list[QAOutput]:
        """
        Performs question answering for a document.

        Args:
            document (InputData): The input document.

        Returns:
            list[QAOutput]: The list of QA outputs.
        """
        outputs = []
        us_text = document.user_story_text
        answer = self.client.chat.completions.create(
            model=self.model_name,
            max_tokens=100,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": GPT_PROMPT_US.format(us_text=us_text),
                },
            ],
        )
        us_answer_text = answer.choices[0].message.content
        us_answers = []
        for us_concept in us_answer_text.split(","):
            us_concept = us_concept.strip()
            if us_concept != "":
                us_answers.append(("", us_concept))

        ac_answers = []
        for ac in document.acceptance_criteria:
            answer = self.client.chat.completions.create(
                model=self.model_name,
                max_tokens=100,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": GPT_PROMPT_AC.format(ac_text=ac),
                    },
                ],
            )
            ac_answer_text = answer.choices[0].message.content
            answers_for_single_ac = []
            for ac_concept in ac_answer_text.split(","):
                ac_concept = ac_concept.strip()
                if ac_concept != "":
                    answers_for_single_ac.append(("", ac_concept))
            ac_answers.append(
                ACConcepts(
                    ac,
                    ac_answer_text,
                )
            )

        outputs.append(
            QAOutput(
                question="",
                us_answer=us_answers,
                ac_answers=ac_answers,
                number=document.number,
                us_text=us_text,
                id=document.id,
            )
        )
        return outputs

    def extract_concepts(self, documents: List[InputData]) -> List[ExtractionOutput]:
        """
        Extracts concepts from a list of documents.

        Args:
            documents (List[InputData]): The list of input documents.

        Returns:
            List[ExtractionOutput]: The list of extraction outputs.
        """
        results = []
        for document in documents:
            qa_result = self.do_qa_for_document(document)

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
            for ac_text, ac_concepts in distinct_ac.items():
                ac_results.append(ACConcepts(ac_text, ac_concepts))
            results.append(
                ExtractionOutput(
                    document.number,
                    document.id,
                    document.user_story_text,
                    us_concepts,
                    ac_results,
                )
            )
        return results

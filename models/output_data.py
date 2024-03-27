from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class ACConcepts:
    ac_text: str
    ac_concepts: List[Tuple[str, str]]


@dataclass
class ACMapping:
    ac_text: str
    ac_concepts: List[Tuple[str, str]]
    mapping: dict[str, str]


@dataclass
class MappingScore:
    us_concept: str
    ac_concept: str
    score: float


@dataclass
class QAOutput:
    """
    Output of extraction with QA per question that was asked
    """

    question: str
    us_answer: List[Tuple[str, str]]
    ac_answers: list[ACConcepts]
    number: int
    us_text: str
    id: str


@dataclass
class ExtractionOutput:
    number: int
    id: str
    us_text: str
    us_concepts: List[Tuple[str, str]]
    acceptance_criteria: list[ACConcepts]


@dataclass
class MappingOutput:
    number: int
    id: str
    user_story_text: str
    ac_mappings: list[ACMapping]
    us_concepts: List[Tuple[str, str]]
    scores: list[MappingScore]


@dataclass
class CompletionOutput:
    number: int
    id: str
    user_story_text: str
    ac_mappings: list[ACMapping]
    us_concepts: List[Tuple[str, str]]
    scores: list[MappingScore]
    completeness_numerical: float
    complete: bool

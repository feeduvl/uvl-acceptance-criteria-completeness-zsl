"""
This module contains the Document dataclass which represents
the structure of documents in the 'warn_gt.json' file.

Each Document has the following attributes:
- id: a unique identifier for the document (str)
- number: a number associated with the document (int)
- gt_us_concepts: a list of concepts associated with the document (List[str])
- gt_complete: a boolean indicating whether the document is complete (bool)
- gt_concept_complete: a boolean indicating whether the concept of the document is complete (bool)
- gt_acceptance_criteria_concepts: a list of lists, where each
  inner list contains concepts associated with a specific acceptance criteria (List[List[str]])
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class GroundTruth:
    """
    Represents the ground truth for a single user story.
    """

    id: str
    number: Optional[int]
    gt_us_concepts: List[str]
    gt_complete: bool
    gt_concept_complete: bool
    gt_acceptance_criteria_concepts: List[List[str]]


@dataclass
class ConceptComparison:
    """
    Represents the comparison of a ground truth concept with extracted concepts.
    """

    id: str
    user_story: str
    acceptance_criterion: str
    concept: str
    mapped_concepts: List[Tuple[str, int]]
    unmapped_concepts: List[str]
    case_str: str
    case_int: int
    case_1_num: int
    case_2_num: int
    case_3_num: int
    case_4_num: int
    case_5_num: int


@dataclass
class BasicConceptComparison:
    """ """

    concept: str
    mapped_concepts: List[str]
    unmapped_concepts: List[str]
    case_str: str
    case_int: int
    case_1_num: int
    case_2_num: int
    case_3_num: int
    case_4_num: int
    case_5_num: int


@dataclass
class GroundTruthCompleteResult:
    """
    Represents the performance results for the entire process.
    """

    id: str
    case_str: str
    case_int: int

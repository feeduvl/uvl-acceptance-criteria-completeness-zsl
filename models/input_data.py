from dataclasses import dataclass
from typing import List


@dataclass
class InputData:
    """
    One user story input containing user story text and acceptance criteria texts
    """
    number: int
    user_story_text: str
    acceptance_criteria: List[str]
    id: str

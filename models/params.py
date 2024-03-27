from dataclasses import dataclass


@dataclass
class ExtractionParams:
    model_name: str
    data_file_name: str
    num: int
    method: str


@dataclass
class MappingParams:
    threshold: float
    use_cosine_similarity: bool
    output_scores: bool


@dataclass
class PerformanceParams:
    gt_file_name: str
    output_file_name: str
    use_cosine_similarity: bool
    output_scores: bool
    threshold: float
    num: int

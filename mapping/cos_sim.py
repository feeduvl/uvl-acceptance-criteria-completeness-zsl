from typing import Dict, List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from models.output_data import ExtractionOutput, MappingOutput, ACMapping, MappingScore
from models.params import MappingParams
from preprocessing.preprocessing import full_preprocessing


def map_concepts(extraction_results: list[ExtractionOutput], params: MappingParams) -> list[MappingOutput]:
    output = []
    vectorizer = TfidfVectorizer()
    all_concepts = []

    for extraction_result in extraction_results:
        all_concepts.extend(list(map(lambda x: x[1], extraction_result.us_concepts)))
        for acceptance_criterion in extraction_result.acceptance_criteria:
            all_concepts.extend(list(map(lambda x: x[1], acceptance_criterion.ac_concepts)))
    vectorizer.fit(list(map(lambda x: full_preprocessing(x), all_concepts)))

    for extraction_result in extraction_results:
        us_concepts: List[Tuple[str, str]] = extraction_result.us_concepts
        # Convert us_concepts to list of its values
        us_concepts: List[str] = list(map(lambda x: x[1], us_concepts))
        us_vectors = vectorizer.transform(list(map(lambda x: full_preprocessing(x), us_concepts)))
        ac_mappings = []
        scores = []
        for acceptance_criterion in extraction_result.acceptance_criteria:
            ac_concepts = acceptance_criterion.ac_concepts
            ac_concepts: List[str] = list(map(lambda x: x[1], ac_concepts))
            ac_vectors = vectorizer.transform(list(map(lambda x: full_preprocessing(x), ac_concepts)))
            cosine_similarities = cosine_similarity(us_vectors, ac_vectors)
            score_per_ac = []

            for score_row, us_concept in zip(cosine_similarities, us_concepts):
                for score, ac_concept in zip(score_row, ac_concepts):
                    score_per_ac.append(MappingScore(us_concept, ac_concept, score))

            if params.output_scores:
                scores.extend(score_per_ac)
            ac_mapping = {}
            for score in score_per_ac:
                if score.score >= 0.5:
                    ac_mapping[score.us_concept] = score.ac_concept

            ac_mappings.append(ACMapping(acceptance_criterion.ac_text, acceptance_criterion.ac_concepts, ac_mapping))
        output.append(MappingOutput(extraction_result.number, extraction_result.id, extraction_result.us_text,
                                    ac_mappings, extraction_result.us_concepts, scores))

    return output


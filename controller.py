from datetime import date
from typing import Dict, List, Tuple
from completion_calculation.completion_calculation import CompletionCalculation

from extraction.gpt import GPTExtraction
from extraction.question_answering import QuestionAnswering
from extraction.question_answering_gpt import QuestionAnsweringGPT
from input_data.read_ground_truth import GroundTruthDeserializer
from input_data.read_input import InputReader
from mapping.cos_sim import map_concepts
from models.ground_truth import GroundTruthCompleteResult
from models.input_data import InputData
from models.output_data import CompletionOutput, ExtractionOutput, MappingOutput
from models.params import ExtractionParams, MappingParams, PerformanceParams
from output_data.write_complete_performance_output import (
    CompletePerformanceOutputWriter,
)
from output_data.write_output import OutputWriter
from output_data.write_extraction_performance_output import (
    WriteExtractionPerformanceOutput,
)
from performance.measure_complete_performance import CompletePerformance
from performance.measure_extraction_performance import ExtractionPerformance


def main(
    extraction_params: ExtractionParams,
    mapping_params: MappingParams,
    performance_params: PerformanceParams,
    input_data: List[InputData],
    write_output: bool = True,
) -> Tuple[List[ExtractionOutput], List[MappingOutput], List[CompletionOutput]]:
    output_name_data_concept_extraction = f"{str(date.today())}_{extraction_params.data_file_name}_{extraction_params.model_name}_concepts".replace(
        "/", ""
    ).replace(
        ".", ""
    )
    output_name_data_concept_mapping = f"{str(date.today())}_{extraction_params.data_file_name}_{extraction_params.model_name}_mapping".replace(
        "/", ""
    ).replace(
        ".", ""
    )
    if extraction_params.method == "gpt":
        qa = GPTExtraction(extraction_params.model_name)
    elif extraction_params.method == "gpt_qa":
        qa = QuestionAnsweringGPT(extraction_params.model_name)
    else:
        qa = QuestionAnswering(extraction_params.model_name)

    outputs_qa = qa.extract_concepts(input_data)

    mapping_result = (
        map_concepts(outputs_qa, mapping_params) if mapping_params else None
    )

    complete_result: List[CompletionOutput] = (
        CompletionCalculation.calculate_completeness_for_mapping_result(mapping_result)
    )

    OutputWriter.write(
        output_name_data_concept_extraction,
        outputs_qa,
        output_name_data_concept_mapping,
        mapping_result,
    )

    if performance_params:
        performance_results_extraction = (
            ExtractionPerformance.measure_extraction_performance(
                GroundTruthDeserializer.from_json_file(performance_params.gt_file_name),
                outputs_qa,
                performance_params,
            )
        )
        write_performance_output = WriteExtractionPerformanceOutput(
            output_file_name=performance_params.output_file_name
        )
        write_performance_output.write_output(performance_results_extraction)


        for threshold in [x/10 for x in range(0, 10)]:
            complete_result: List[CompletionOutput] = (
                CompletionCalculation.calculate_completeness_for_mapping_result(
                    mapping_result, threshold
                )
            )
            complete_results_performance = CompletePerformance.measure_complete_performance(
                    performance_params,
                    GroundTruthDeserializer.from_json_file(performance_params.gt_file_name),
                    complete_result,
                )

            write_complete_performance_output = CompletePerformanceOutputWriter(
                output_file_name=performance_params.output_file_name + f"_{threshold}"
            )
            write_complete_performance_output.write_output(complete_results_performance)
    return outputs_qa, mapping_result, complete_result

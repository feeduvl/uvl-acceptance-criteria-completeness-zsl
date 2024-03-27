"""
This module contains the main script for performing extraction 
and mapping tasks on different datasets using various models.

The script iterates over a list of datasets and models, 
and for each combination, it calls the `main` function from the `controller` module.
The `main` function takes two parameters: `ExtractionParams` and `MappingParams`,
which specify the data file name, model name, and other parameters for extraction and mapping.

Example usage:
    datasets = ["COMET_dataset", "STAR_dataset", "warn"]
    models = ["MaRiOrOsSi/t5-base-finetuned-question-answering",
    "deepset/deberta-v3-base-squad2",
    "deepset/roberta-base-squad2",
    "deepset/tinyroberta-squad2",
    "sjrhuschlee/flan-t5-base-squad2"]
    method = "local_qa" | "gpt_qa" | "gpt"

"""

from datetime import date
from controller import main
from input_data.read_input import InputReader
from models.params import ExtractionParams, MappingParams, PerformanceParams

datasets = ["cost"]
# models = ["gpt-3.5-turbo-1106"]
models = ["MaRiOrOsSi/t5-base-finetuned-question-answering",
    "deepset/deberta-v3-base-squad2",
    "deepset/roberta-base-squad2",
    "deepset/tinyroberta-squad2",
    "sjrhuschlee/flan-t5-base-squad2"]
# models = ["gpt-3.5-turbo-instruct"]

method = ""

for dataset in datasets:
    input_data = InputReader.read(
        dataset, 100
    )
    for model in models:
        print(f"Starting {dataset} with {model}")
        main(
            ExtractionParams(
                data_file_name=dataset, model_name=model, num=100, method=method
            ),
            MappingParams(
                output_scores=True, threshold=0.5, use_cosine_similarity=True
            ),
            PerformanceParams(
                gt_file_name=f"data/{dataset}_gt.json",
                output_file_name=f"{str(date.today())}_{dataset}_{model}_performance",
                use_cosine_similarity=True,
                output_scores=True,
                threshold=0.5,
                num=25,
            ),
            input_data
        )
        print(f"Finished {dataset} with {model}")

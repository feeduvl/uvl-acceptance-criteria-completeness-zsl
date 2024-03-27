from time import time
from flask import Flask, json, request

from controller import main
from input_data.read_input import InputReader
from models.params import ExtractionParams, MappingParams, PerformanceParams
from output_data.write_output import OutputWriter


app = Flask(__name__)

@app.route("/hitec/classify/concepts/acceptance-criteria-completeness-zsl/run", methods=["POST"])
def start_analysis():
    data = json.loads(request.data)
    documents = data["dataset"]["documents"]

    extraction_params, mapping_params, performance_params = InputReader.read_params_json(data["params"])

    input_data = InputReader.read_json(documents)
    extraction_output, mapping_output, completion_output = main(
        extraction_params,
        mapping_params,
        performance_params,
        input_data
    )

    res = OutputWriter.write_all_to_json(extraction_output, mapping_output, completion_output)
            
    return res

@app.route("/hitec/classify/concepts/acceptance-criteria-completeness-zsl/status", methods=["GET"])
def get_status():
    status = {"status": "operational"}
    return status

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=9699)
    
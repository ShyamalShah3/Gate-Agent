import yaml
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
)
from constructs import Construct
from infra.constructs.lambda_layers import LambdaLayers
from infra.constructs.api_construct import ApiConstruct

class GateAgentBeStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Load configuration files
        with open("config.yml", "r") as config_file:
            config = yaml.safe_load(config_file)

        # Set architecture
        architecture = _lambda.Architecture.X86_64
        if config["lambda"]["architecture"].upper() == "ARM_64":
            architecture = _lambda.Architecture.ARM_64

        # Set Python runtime
        python_runtime_str = config["lambda"]["python_runtime"]
        if python_runtime_str == "PYTHON_3_9":
            python_runtime = _lambda.Runtime.PYTHON_3_9
        elif python_runtime_str == "PYTHON_3_10":
            python_runtime = _lambda.Runtime.PYTHON_3_10
        elif python_runtime_str == "PYTHON_3_11":
            python_runtime = _lambda.Runtime.PYTHON_3_11
        elif python_runtime_str == "PYTHON_3_12":
            python_runtime = _lambda.Runtime.PYTHON_3_12
        elif python_runtime_str == "PYTHON_3_13":
            python_runtime = _lambda.Runtime.PYTHON_3_13
        else:
            raise ValueError(f"Unsupported Python runtime: {python_runtime_str}")

        # Get values from config
        max_tokens = str(config["model"]["max_tokens"])
        temperature = str(config["model"]["temperature"])
        num_search_results = str(config["rag"]["num_search_results"])
        rag_model_name = str(config["rag"]["rag_model_name"])
        knowledge_base_id = str(config["rag"]["knowledge_base_id"])

        ## **************** Lambda Layers ****************
        self.layers = LambdaLayers(
            self,
            f"{construct_id}-layers",
            stack_name=construct_id,
            architecture=architecture,
            python_runtime=python_runtime,
        )

        ## **************** API Construct ****************
        self.api_construct = ApiConstruct(
            self,
            "ApiConstruct",
            stack_name=construct_id,
            layers=self.layers.get_all_layers(),
            architecture=architecture,
            runtime=python_runtime,
            max_tokens=max_tokens,
            temperature=temperature,
            num_search_results=num_search_results,
            rag_model_name=rag_model_name,
            knowledge_base_id=knowledge_base_id
        )
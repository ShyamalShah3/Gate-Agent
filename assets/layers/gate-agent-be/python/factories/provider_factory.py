from providers.base_provider import BaseProvider
from providers.bedrock_provider import BedrockProvider
from utils.enums import Provider, BedrockModel
from model.streaming import StreamingCallback
import os
import json
import logging
import boto3
from botocore.exceptions import ClientError

class ProviderFactory:
    """
    Factory class to instantiate AI model providers based on the provider type.
    """

    def __init__(self, model_name: str, streaming_callback: StreamingCallback = None, max_tokens: int = 1000, temperature: float = 0.7) -> None:
        """
        Initialize the ProviderFactory with necessary parameters.
        
        Parameters:
        model_name (str): The name of the model to instantiate.
        streaming_callback (StreamingCallback, optional): Callback handler for streaming responses.
        max_tokens (int, optional): Maximum number of tokens in the model's response. Defaults to 1000.
        temperature (float, optional): Temperature to set for the model. Defaults to 0.7.
        """
        self.model_name = model_name
        self.provider = self._get_provider_type()
        self.streaming_callback = streaming_callback
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(f"ProviderFactory initialized with model_name: {self.model_name}, max_tokens: {self.max_tokens}, temperature: {self.temperature}")
    
    def _get_provider_type(self):
        if self.model_name in BedrockModel.__members__:
            return Provider.BEDROCK
        else:
            raise ValueError(f"{self.model_name} is not a currently supported model")
    
    def get_provider(self) -> BaseProvider:
        """
        Determine the provider based on the model name and instantiate the corresponding provider.
        
        Returns:
            BaseProvider: An instance of a provider implementing BaseProvider.
        
        Raises:
            ValueError: If the provider for the given model is unsupported or not found.
        """
        if self.provider == Provider.BEDROCK:
            model_id = BedrockModel[self.model_name].value
            self.logger.debug(f"Model '{self.model_name}' identified as Bedrock model with ID '{model_id}'")
            if not self.streaming_callback:
                raise ValueError("Streaming callback is required for Bedrock Models")
            return BedrockProvider(model_id=model_id, streaming_callback=self.streaming_callback, max_tokens=self.max_tokens, temperature=self.temperature)
        else:
            self.logger.error(f"Unsupported or unknown model name: {self.model_name}")
            raise ValueError(f"Unsupported or unknown model name: {self.model_name}")

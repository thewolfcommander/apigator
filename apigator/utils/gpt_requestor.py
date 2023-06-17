import os
import openai

from .logger import log_custom_error, log_info


class GPTRequestor:
    """
    Module for making requests to GPT
    """
    def __init__(self, gpt_key, organization_id) -> None:
        self.gpt_key = gpt_key
        self.organization_id = organization_id
    
    def check_authorization(self):
        """
        Method to make request on GPT
        """
        try:
            log_info('openai_started')

            openai.organization = self.organization_id
            openai.api_key = self.gpt_key
            models = openai.Model.list()

            log_info('openai_completed', {'models': models})
            return {
                'status': True
            }
        except Exception as e:
            response = log_custom_error('error_connecting_openai', e, data={})
            return response
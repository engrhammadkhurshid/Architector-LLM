"""
LLM API Client for DeepSeek API and Ollama
Handles secure communication with LLM providers
"""

import os
import logging
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class OllamaClient:
    """
    Client for interacting with Ollama (local LLM)
    """
    
    def __init__(self):
        self.base_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        self.model = os.getenv('OLLAMA_MODEL', 'deepseek-coder:6.7b')
        self.temperature = float(os.getenv('LLM_TEMPERATURE', 0.2))
        self.max_tokens = int(os.getenv('LLM_MAX_TOKENS', 4096))
        
        logger.info(f'Initialized Ollama client with model: {self.model}')
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate text using Ollama
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt for context
            
        Returns:
            Response containing generated text
        """
        logger.info(f'Sending request to Ollama at {self.base_url}')
        
        # Build the full prompt with system context
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        payload = {
            'model': self.model,
            'prompt': full_prompt,
            'stream': False,
            'options': {
                'temperature': self.temperature,
                'num_predict': self.max_tokens
            }
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/api/generate',
                json=payload,
                timeout=300  # Ollama can be slower on first run
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info('Successfully received response from Ollama')
            
            return {
                'status': 'success',
                'content': result['response'],
                'model': result.get('model', self.model),
                'eval_count': result.get('eval_count', 0),
                'eval_duration': result.get('eval_duration', 0)
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f'Ollama request failed: {str(e)}')
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def test_connection(self) -> bool:
        """Test if Ollama is running and model is available"""
        try:
            # Check if Ollama is running
            response = requests.get(f'{self.base_url}/api/tags', timeout=5)
            response.raise_for_status()
            
            models = response.json().get('models', [])
            model_names = [m['name'] for m in models]
            
            logger.info(f'Available Ollama models: {model_names}')
            
            # Check if our model is available
            if self.model not in model_names:
                logger.warning(f'Model {self.model} not found. Available: {model_names}')
                return False
            
            # Test generation
            test_response = self.generate('Reply with OK', system_prompt='You are a test assistant')
            return test_response['status'] == 'success'
            
        except Exception as e:
            logger.error(f'Ollama connection test failed: {e}')
            return False


class LLMClient:
    """
    Client for interacting with DeepSeek API
    """
    
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        self.api_url = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1')
        self.model = os.getenv('LLM_MODEL', 'deepseek-coder')
        self.temperature = float(os.getenv('LLM_TEMPERATURE', 0.2))
        self.max_tokens = int(os.getenv('LLM_MAX_TOKENS', 4096))
        
        if not self.api_key:
            raise ValueError('DEEPSEEK_API_KEY not found in environment variables')
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate text using the DeepSeek API
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt for context
            
        Returns:
            Response from the API containing generated text
        """
        logger.info('Sending request to DeepSeek API')
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        messages = []
        if system_prompt:
            messages.append({
                'role': 'system',
                'content': system_prompt
            })
        
        messages.append({
            'role': 'user',
            'content': prompt
        })
        
        payload = {
            'model': self.model,
            'messages': messages,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens
        }
        
        try:
            response = requests.post(
                f'{self.api_url}/chat/completions',
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info('Successfully received response from DeepSeek API')
            
            return {
                'status': 'success',
                'content': result['choices'][0]['message']['content'],
                'usage': result.get('usage', {}),
                'model': result.get('model', self.model)
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f'API request failed: {str(e)}')
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def test_connection(self) -> bool:
        """Test if the API connection is working"""
        try:
            response = self.generate('Hello', system_prompt='Reply with "OK"')
            return response['status'] == 'success'
        except Exception as e:
            logger.error(f'Connection test failed: {e}')
            return False


def get_llm_client() -> Any:
    """
    Factory function to get the appropriate LLM client based on configuration
    
    Returns:
        LLMClient, OllamaClient, OpenAIClient, or ClaudeClient instance
    """
    provider = os.getenv('LLM_PROVIDER', 'ollama').lower()
    
    if provider == 'ollama':
        logger.info('Using Ollama client')
        return OllamaClient()
    elif provider == 'deepseek':
        logger.info('Using DeepSeek API client')
        return LLMClient()
    elif provider == 'openai':
        logger.info('Using OpenAI client')
        return OpenAIClient()
    elif provider == 'claude':
        logger.info('Using Anthropic Claude client')
        return ClaudeClient()
    else:
        raise ValueError(f'Unknown LLM provider: {provider}. Use "ollama", "deepseek", "openai", or "claude"')


class OpenAIClient:
    """Client for OpenAI GPT-4 API"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.api_url = 'https://api.openai.com/v1'
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
        self.temperature = float(os.getenv('LLM_TEMPERATURE', 0.2))
        self.max_tokens = int(os.getenv('LLM_MAX_TOKENS', 4096))
        
        if not self.api_key:
            raise ValueError('OPENAI_API_KEY not found in environment variables')
        
        logger.info(f'Initialized OpenAI client with model: {self.model}')
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate text using OpenAI API"""
        logger.info('Sending request to OpenAI API')
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})
        
        payload = {
            'model': self.model,
            'messages': messages,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens
        }
        
        try:
            response = requests.post(
                f'{self.api_url}/chat/completions',
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info('Successfully received response from OpenAI')
            
            return {
                'status': 'success',
                'content': result['choices'][0]['message']['content'],
                'usage': result.get('usage', {}),
                'model': result.get('model', self.model)
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f'OpenAI API request failed: {str(e)}')
            return {'status': 'error', 'message': str(e)}
    
    def test_connection(self) -> bool:
        """Test OpenAI API connection"""
        try:
            response = self.generate('Reply with OK', system_prompt='You are a test assistant')
            return response['status'] == 'success'
        except Exception as e:
            logger.error(f'OpenAI connection test failed: {e}')
            return False


class ClaudeClient:
    """Client for Anthropic Claude API"""
    
    def __init__(self):
        self.api_key = os.getenv('CLAUDE_API_KEY')
        self.api_url = 'https://api.anthropic.com/v1'
        self.model = os.getenv('CLAUDE_MODEL', 'claude-3-sonnet-20240229')
        self.temperature = float(os.getenv('LLM_TEMPERATURE', 0.2))
        self.max_tokens = int(os.getenv('LLM_MAX_TOKENS', 4096))
        
        if not self.api_key:
            raise ValueError('CLAUDE_API_KEY not found in environment variables')
        
        logger.info(f'Initialized Claude client with model: {self.model}')
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate text using Claude API"""
        logger.info('Sending request to Claude API')
        
        headers = {
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': self.model,
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': self.max_tokens,
            'temperature': self.temperature
        }
        
        if system_prompt:
            payload['system'] = system_prompt
        
        try:
            response = requests.post(
                f'{self.api_url}/messages',
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info('Successfully received response from Claude')
            
            return {
                'status': 'success',
                'content': result['content'][0]['text'],
                'usage': result.get('usage', {}),
                'model': result.get('model', self.model)
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f'Claude API request failed: {str(e)}')
            return {'status': 'error', 'message': str(e)}
    
    def test_connection(self) -> bool:
        """Test Claude API connection"""
        try:
            response = self.generate('Reply with OK', system_prompt='You are a test assistant')
            return response['status'] == 'success'
        except Exception as e:
            logger.error(f'Claude connection test failed: {e}')
            return False

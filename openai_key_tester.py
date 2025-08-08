#!/usr/bin/env python3
"""
OpenAI API Key Tester

A simple and graceful tool to test OpenAI API keys with comprehensive error handling.
"""

import os
import sys
import time
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import requests
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class OpenAIKeyTester:
    """A class to test OpenAI API keys with graceful error handling."""
    
    def __init__(self):
        """Initialize the tester and load environment variables."""
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.api_base = os.getenv('OPENAI_API_BASE')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        
    def print_header(self):
        """Print a beautiful header for the tester."""
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🤖 OpenAI API Key Tester")
        print(f"{Fore.CYAN}{'='*60}")
        print()
        
    def print_success(self, message: str):
        """Print a success message in green."""
        print(f"{Fore.GREEN}✅ {message}")
        
    def print_error(self, message: str):
        """Print an error message in red."""
        print(f"{Fore.RED}❌ {message}")
        
    def print_warning(self, message: str):
        """Print a warning message in yellow."""
        print(f"{Fore.YELLOW}⚠️  {message}")
        
    def print_info(self, message: str):
        """Print an info message in blue."""
        print(f"{Fore.BLUE}ℹ️  {message}")
        
    def check_api_key_format(self) -> bool:
        """Check if the API key has the correct format."""
        if not self.api_key:
            self.print_error("No API key found. Please set OPENAI_API_KEY in your .env file.")
            return False
            
        if not self.api_key.startswith('sk-'):
            self.print_error("Invalid API key format. OpenAI API keys should start with 'sk-'.")
            return False
            
        if len(self.api_key) < 20:
            self.print_error("API key seems too short. Please check your API key.")
            return False
            
        self.print_success("API key format looks valid.")
        return True
        
    def test_connectivity(self) -> bool:
        """Test basic connectivity to OpenAI API."""
        try:
            # Test with a simple request to the models endpoint
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            url = f"{self.api_base or 'https://api.openai.com'}/v1/models"
            
            self.print_info("Testing connectivity to OpenAI API...")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                self.print_success("Successfully connected to OpenAI API.")
                return True
            elif response.status_code == 401:
                self.print_error("Authentication failed. Please check your API key.")
                return False
            elif response.status_code == 403:
                self.print_error("Access forbidden. Your API key may not have the required permissions.")
                return False
            else:
                self.print_error(f"Unexpected response: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            self.print_error("Connection timeout. Please check your internet connection.")
            return False
        except requests.exceptions.ConnectionError:
            self.print_error("Connection failed. Please check your internet connection.")
            return False
        except Exception as e:
            self.print_error(f"Unexpected error during connectivity test: {str(e)}")
            return False
            
    def test_simple_completion(self) -> bool:
        """Test a simple completion request."""
        try:
            import openai
            
            # Configure the client
            client_kwargs = {
                'api_key': self.api_key
            }
            
            if self.api_base:
                client_kwargs['base_url'] = self.api_base
                
            client = openai.OpenAI(**client_kwargs)
            
            self.print_info(f"Testing completion with model: {self.model}")
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": "Hello! Please respond with 'API test successful' if you can see this message."}
                ],
                max_tokens=50,
                temperature=0.1
            )
            
            if response.choices and response.choices[0].message.content:
                self.print_success("Simple completion test successful!")
                self.print_info(f"Response: {response.choices[0].message.content.strip()}")
                return True
            else:
                self.print_error("Completion test failed - no response received.")
                return False
                
        except openai.AuthenticationError:
            self.print_error("Authentication failed during completion test.")
            return False
        except openai.RateLimitError:
            self.print_error("Rate limit exceeded. Please wait a moment and try again.")
            return False
        except openai.APIError as e:
            self.print_error(f"API error during completion test: {str(e)}")
            return False
        except Exception as e:
            self.print_error(f"Unexpected error during completion test: {str(e)}")
            return False
            
    def test_model_availability(self) -> bool:
        """Test if the specified model is available."""
        try:
            import openai
            
            client_kwargs = {'api_key': self.api_key}
            if self.api_base:
                client_kwargs['base_url'] = self.api_base
                
            client = openai.OpenAI(**client_kwargs)
            
            self.print_info(f"Checking availability of model: {self.model}")
            
            # Try to get model info
            try:
                model_info = client.models.retrieve(self.model)
                self.print_success(f"Model {self.model} is available.")
                return True
            except openai.NotFoundError:
                self.print_warning(f"Model {self.model} not found. Trying with gpt-3.5-turbo...")
                # Try with a fallback model
                try:
                    model_info = client.models.retrieve('gpt-3.5-turbo')
                    self.print_success("Fallback model gpt-3.5-turbo is available.")
                    return True
                except:
                    self.print_error("Neither the specified model nor fallback model is available.")
                    return False
                    
        except Exception as e:
            self.print_error(f"Error checking model availability: {str(e)}")
            return False
            
    def run_comprehensive_test(self) -> Dict[str, bool]:
        """Run all tests and return results."""
        results = {}
        
        self.print_header()
        
        # Test 1: API Key Format
        self.print_info("Step 1: Checking API key format...")
        results['format'] = self.check_api_key_format()
        print()
        
        if not results['format']:
            return results
            
        # Test 2: Connectivity
        self.print_info("Step 2: Testing connectivity...")
        results['connectivity'] = self.test_connectivity()
        print()
        
        if not results['connectivity']:
            return results
            
        # Test 3: Model Availability
        self.print_info("Step 3: Checking model availability...")
        results['model_available'] = self.test_model_availability()
        print()
        
        # Test 4: Simple Completion
        self.print_info("Step 4: Testing simple completion...")
        results['completion'] = self.test_simple_completion()
        print()
        
        return results
        
    def print_summary(self, results: Dict[str, bool]):
        """Print a summary of all test results."""
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}📊 Test Summary")
        print(f"{Fore.CYAN}{'='*60}")
        
        total_tests = len(results)
        passed_tests = sum(results.values())
        
        for test_name, result in results.items():
            status = f"{Fore.GREEN}✅ PASS" if result else f"{Fore.RED}❌ FAIL"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
            
        print()
        print(f"Overall: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            self.print_success("🎉 All tests passed! Your OpenAI API key is working correctly.")
        elif passed_tests > 0:
            self.print_warning("⚠️  Some tests passed, but there are issues to address.")
        else:
            self.print_error("💥 All tests failed. Please check your configuration.")

def main():
    """Main function to run the OpenAI key tester."""
    try:
        tester = OpenAIKeyTester()
        results = tester.run_comprehensive_test()
        tester.print_summary(results)
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Testing interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()

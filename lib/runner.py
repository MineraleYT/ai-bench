#!/usr/bin/env python3.12
import json
import logging
import os
import sys
import time
import ollama
import concurrent.futures
import GPUtil
from datetime import datetime
import numpy as np

from .result import BenchmarkResult
from .system_info import SystemInfo
from .analysis import print_results

def save_results(results, timestamp):
    results_dir = 'results'
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        
    filename = f"{results_dir}/benchmark_{timestamp}.json"
    
    def convert_numpy(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj

    with open(filename, 'w') as f:
        json.dump({"results": results}, f, indent=4, default=convert_numpy)
    logging.info(f"Results saved to {filename}")

def run_benchmark_for_prompts(model, prompts, verbose=False):
    result = BenchmarkResult(model)
    result.system_specs = SystemInfo.get_system_specs()
    
    # Check if Ollama is running
    try:
        ollama.list()
    except Exception as e:
        logging.error("Ollama is not running. Please start it with 'ollama serve'")
        sys.exit(1)

    # Model loading time
    start_time = time.time()
    try:
        ollama.pull(model)
    except Exception as e:
        logging.error(f"Error pulling model {model}: {str(e)}")
        sys.exit(1)
        
    result.model_load_time = time.time() - start_time
    
    # Start resource monitoring in a separate thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(SystemInfo.monitor_resources, 60)  # Monitor for 60 seconds max
        
        try:
            # Process each prompt
            for prompt in prompts:
                prompt_start_time = time.time()
                
                # Get response from model
                response = ollama.generate(
                    model=model,
                    prompt=prompt,
                    options={
                        "num_gpu": len(GPUtil.getGPUs()) if GPUtil.getGPUs() else 0,
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                )
                
                if verbose:
                    print(f"\nPrompt: {prompt}\n")
                    print(f"Response: {response['response']}\n")
                
                prompt_end_time = time.time()
                result.prompt_tokens += response['prompt_eval_count']
                result.response_tokens += response['eval_count']
                result.prompt_eval_time += prompt_end_time - prompt_start_time
                
                # Get token-by-token metrics
                stream = ollama.generate(
                    model=model,
                    prompt=prompt,
                    stream=True,
                    options={
                        "num_gpu": len(GPUtil.getGPUs()) if GPUtil.getGPUs() else 0,
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                )
                
                last_token_time = time.time()
                tokens_since_last = 0
                    
                for chunk in stream:
                    current_time = time.time()
                    if isinstance(chunk, dict) and 'response' in chunk:
                        tokens_since_last += 1
                        
                        # Calculate tokens per second every 10 tokens
                        if tokens_since_last >= 10:
                            time_diff = current_time - last_token_time
                            if time_diff > 0:
                                result.completion_tokens_per_second.append(tokens_since_last / time_diff)
                            tokens_since_last = 0
                            last_token_time = current_time
                        
                        if verbose:
                            print(chunk['response'], end='', flush=True)
                
                if verbose:
                    print("\n")

                result.response_time += time.time() - prompt_end_time
                
            result.total_time = time.time() - start_time
            result.resources_usage = future.result()
            result.calculate_metrics()
            return result
            
        except Exception as e:
            logging.error(f"Error during benchmark for {model}: {str(e)}")
            return None

def main(verbose=False, prompts=None, models=None):
    # Setup logging
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[
            logging.FileHandler(f'logs/benchmark_{datetime.now().strftime("%H%M%S_%d%m%Y")}.log'),
            logging.StreamHandler()
        ]
    )
    logging.getLogger('httpx').setLevel(logging.WARNING)  # Disable ollama HTTP logs

    # Default prompts
    if not prompts:
        prompts = [
            "What are the key differences between classical and quantum computing?",
            "Describe an efficient implementation of quicksort in Python.",
            "How do transformer models handle long-range dependencies?",
            "Explain the concept of algorithmic complexity using Big O notation."
        ]

    timestamp = datetime.now().strftime("%H%M%S_%d%m%Y")
    all_results = []
    
    try:
        # Get available models if none specified
        if not models:
            response = ollama.list()
            if not response or not response.get('models', []):
                logging.error("No models available. Please download some models first.")
                return []
            models = [model.get('name', model.get('model', 'Unknown')) 
                     for model in response.get('models', [])]

        # Run benchmark for each model
        for model in models:
            logging.info(f"\nBenchmarking {model}...")
            result = run_benchmark_for_prompts(model, prompts, verbose)
            if result:
                all_results.append(result.to_dict())
                print_results({"model_name": model, "speeds": result.to_dict()["speeds"], "performance": result.to_dict()["performance"]})
                    
        save_results(all_results, timestamp)
        return all_results
        
    except Exception as e:
        logging.error(f"Error during benchmarking: {str(e)}")
        return []

# For backward compatibility
run_benchmark = run_benchmark_for_prompts

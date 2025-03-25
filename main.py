#!/usr/bin/env python3.12
import sys
import os
from lib import run_benchmark_main as run_benchmark

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    print(f"""
{Colors.CYAN}╭─────────────────── AI BENCHMARK ──────╮
│                                       │
│  {Colors.BOLD}Welcome to the AI Benchmark Tool{Colors.CYAN}     │
│  {Colors.CYAN}Measure and Compare LLM Performance  │
│  {Colors.CYAN}Made by Mineraleyt with ❤️            │
│                                       │
╰───────────────────────────────────────╯{Colors.END}""")

def colorize_menu(text, num):
    return f"{Colors.CYAN}{num}. {Colors.END}{Colors.BOLD}{text}{Colors.END}"

def manage_models():
    while True:
        print(f"\n{Colors.BOLD}Model Management:{Colors.END}")
        print(colorize_menu("Download model", 1))
        print(colorize_menu("List installed models", 2))
        print(colorize_menu("Delete model", 3))
        print(colorize_menu("Back to main menu", 4))
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            print("\nFind available models at: https://ollama.com/search")
            model = input("\nEnter model name (e.g., llama3.2:3b): ")
            print(f"\nDownloading {model}...")
            try:
                import ollama
                ollama.pull(model)
                print(f"\n{Colors.GREEN}{model} downloaded successfully!{Colors.END}")
            except Exception as e:
                print(f"\n{Colors.FAIL}Error downloading model: {str(e)}{Colors.END}")
                print(f"{Colors.WARNING}Make sure Ollama is running (ollama serve){Colors.END}")
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            print("\nInstalled models:")
            try:
                import ollama
                response = ollama.list()
                if not response:
                    print("No models installed")
                else:
                    models = response.get('models', [])
                    if not models:
                        print("No models installed")
                    else:
                        for model in models:
                            name = str(model.get('name', model.get('model', 'Unknown')))
                            digest = model.get('digest', '')[:12]  # Show first 12 chars of digest if available
                            size = model.get('size', 0) / (1024 * 1024 * 1024)  # Convert to GB
                            if digest:
                                print(f"- {name:<20} ({size:.1f} GB) [{digest}]")
                            else:
                                print(f"- {name:<20} ({size:.1f} GB)")
            except Exception as e:
                print(f"{Colors.FAIL}Error listing models: {str(e)}{Colors.END}")
                print(f"{Colors.WARNING}Make sure Ollama is running (ollama serve){Colors.END}")
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            try:
                import ollama
                response = ollama.list()
                if not response:
                    print("\nNo models installed")
                else:
                    models = response.get('models', [])
                    if not models:
                        print("\nNo models installed")
                    else:
                        print("\nInstalled models:")
                        for i, model in enumerate(models, 1):
                            name = str(model.get('name', model.get('model', 'Unknown')))
                            digest = model.get('digest', '')[:12]
                            size = model.get('size', 0) / (1024 * 1024 * 1024)
                            print(f"{i}. {name:<20} ({size:.1f} GB) [{digest}]")
                        
                        choice = input("\nEnter model number to delete (or 0 to cancel): ")
                        try:
                            idx = int(choice) - 1
                            if idx >= 0 and idx < len(models):
                                model_name = str(models[idx].get('name', models[idx].get('model', 'Unknown')))
                                if input(f"\n{Colors.WARNING}Confirm deletion of {model_name}? (y/N): {Colors.END}").lower().startswith('y'):
                                    ollama.delete(model_name)
                                    print(f"\n{Colors.GREEN}{model_name} deleted successfully!{Colors.END}")
                            elif idx != -1:  # If not 0 (cancel)
                                print(f"\n{Colors.FAIL}Invalid model number{Colors.END}")
                        except ValueError:
                            print(f"\n{Colors.FAIL}Invalid choice{Colors.END}")
            except Exception as e:
                print(f"\n{Colors.FAIL}Error managing models: {str(e)}{Colors.END}")
                print(f"{Colors.WARNING}Make sure Ollama is running (ollama serve){Colors.END}")
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            return
            
        else:
            print(f"\n{Colors.FAIL}Invalid choice. Please try again.{Colors.END}")

def print_menu():
    print(f"\n{Colors.BOLD}Choose an action:{Colors.END}")
    print(colorize_menu("Run benchmark", 1))
    print(colorize_menu("Model management", 2))
    print(colorize_menu("Exit", 3))
    return input("\nEnter your choice (1-3): ")

def get_benchmark_options():
    options = {}
    
    print(f"\n{Colors.BOLD}Benchmark Options:{Colors.END}")
    if input("Enable verbose output? (y/N): ").lower().startswith('y'):
        options['verbose'] = True
    
    if input("Use custom prompts? (y/N): ").lower().startswith('y'):
        prompts = []
        print("\nEnter prompts (empty line to finish):")
        while True:
            prompt = input("> ")
            if not prompt:
                break
            prompts.append(prompt)
        if prompts:
            options['prompts'] = prompts
    
    try:
        import ollama
        print("\nAvailable models:")
        response = ollama.list()
        if not response or not response.get('models', []):
            print("No models installed. Use the model management menu to download models first.")
            return None
        
        models = response.get('models', [])
        selected_models = []
        
        print("\nSelect models for benchmark:")
        for i, model in enumerate(models, 1):
            name = str(model.get('name', model.get('model', 'Unknown')))
            size = model.get('size', 0) / (1024 * 1024 * 1024)  # Convert to GB
            print(f"{i}. {name:<20} ({size:.1f} GB)")
        
        print("\nEnter model numbers to benchmark (space-separated), or press Enter to benchmark all:")
        choice = input("> ").strip()
        
        if choice.strip():
            try:
                indices = [int(idx) - 1 for idx in choice.split()]
                for idx in indices:
                    if 0 <= idx < len(models):
                        model_name = str(models[idx].get('name', models[idx].get('model', 'Unknown')))
                        selected_models.append(model_name)
                    else:
                        print(f"\n{Colors.WARNING}Invalid model number {idx + 1}, skipping...{Colors.END}")
                
                if not selected_models:
                    print(f"\n{Colors.FAIL}No valid models selected{Colors.END}")
                    return None
            except ValueError:
                print(f"\n{Colors.FAIL}Invalid input. Please enter numbers only.{Colors.END}")
                return None
        else:
            # If no choice made (pressed Enter), use all models
            selected_models = [str(model.get('name', model.get('model', 'Unknown'))) for model in models]
        
        options['models'] = selected_models
    except Exception as e:
        print(f"\n{Colors.FAIL}Error listing models: {str(e)}{Colors.END}")
        print(f"{Colors.WARNING}Make sure Ollama is running (ollama serve){Colors.END}")
        return None
    
    return options

def main():
    print_banner()
    
    while True:
        choice = print_menu()
        
        if choice == '1':
            if not os.path.exists('.venv'):
                setup_script = 'setup.bat' if sys.platform == 'win32' else './setup.sh'
                print(f"\n{Colors.FAIL}Error: Virtual environment not found. Please run {setup_script} first.{Colors.END}")
                input("\nPress Enter to continue...")
                continue
                
            print("\nConfiguring benchmark...")
            options = get_benchmark_options()
            
            if options is None:
                input("\nPress Enter to continue...")
                continue
            
            print(f"\n{Colors.BOLD}Selected models for benchmark:{Colors.END}")
            for model in options.get('models', []):
                print(f"- {model}")
            
            print(f"\n{Colors.BOLD}Starting benchmark...{Colors.END}")
            try:
                # Extract models and create kwargs for run_benchmark
                selected_models = options.pop('models', None) if options else None
                if selected_models:
                    run_benchmark(models=selected_models, **options or {})
                else:
                    print(f"{Colors.FAIL}Error: No models selected for benchmark{Colors.END}")
            except Exception as e:
                print(f"\n{Colors.FAIL}Error during benchmark: {str(e)}{Colors.END}")
                input("\nPress Enter to continue...")
                continue
        
        elif choice == '2':
            manage_models()
            continue
            
        elif choice == '3':
            print(f"\n{Colors.GREEN}Goodbye!{Colors.END}")
            sys.exit(0)
        
        else:
            print(f"\n{Colors.FAIL}Invalid choice. Please try again.{Colors.END}")
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Operation cancelled by user{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}Unexpected error: {str(e)}{Colors.END}")
        sys.exit(1)

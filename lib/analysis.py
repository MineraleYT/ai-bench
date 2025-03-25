def analyze_performance(results):
    """Generate performance insights from benchmark results"""
    insights = []
    
    for result in results:
        model = result["model_name"]
        speeds = result["speeds"]
        res_usage = result["system"]["resources"]
        
        # Analyze resource utilization
        if res_usage and res_usage.get("gpu"):
            gpu_efficiency = res_usage["gpu"]["load"]["mean"] / 100
            if gpu_efficiency < 0.7:
                insights.append(f"{model}: Low GPU utilization ({gpu_efficiency:.1%})")
            
    return insights

def print_results(avg_result):
    """Print benchmark results in a formatted way"""
    from .utils import Colors

    print(f"\n{Colors.BOLD}Model: {Colors.CYAN}{avg_result['model_name']}{Colors.END}\n")
    
    # Speed Metrics
    print(f"{Colors.BOLD}Speed Metrics:{Colors.END}")
    print(f"  Prompt Evaluation:    {Colors.GREEN}{avg_result['speeds']['prompt_eval']:.2f} t/s{Colors.END}")
    print(f"  Response Generation:  {Colors.GREEN}{avg_result['speeds']['response']:.2f} t/s{Colors.END}")
    print(f"  Total Speed:          {Colors.GREEN}{avg_result['speeds']['total']:.2f} t/s{Colors.END}\n")
    
    # Token Statistics
    print(f"{Colors.BOLD}Token Statistics:{Colors.END}")
    print(f"  Prompt Tokens:        {Colors.GREEN}{avg_result['performance']['prompt_tokens']:.0f}{Colors.END}")
    print(f"  Response Tokens:      {Colors.GREEN}{avg_result['performance']['response_tokens']:.0f}{Colors.END}\n")
    
    # Timing Metrics
    print(f"{Colors.BOLD}Timing Metrics:{Colors.END}")
    print(f"  Model Load:           {Colors.GREEN}{avg_result['performance']['model_load_time']:.2f}s{Colors.END}")
    print(f"  Prompt Evaluation:    {Colors.GREEN}{avg_result['performance']['prompt_eval_time']:.2f}s{Colors.END}")
    print(f"  Response Generation:  {Colors.GREEN}{avg_result['performance']['response_time']:.2f}s{Colors.END}")
    print(f"  Total Time:           {Colors.GREEN}{avg_result['performance']['total_time']:.2f}s{Colors.END}\n")

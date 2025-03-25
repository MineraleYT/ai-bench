def analyze_performance(results):
    """Generate performance insights from benchmark results"""
    insights = []
    
    for result in results:
        model = result["model_name"]
        speeds = result["speeds"]
        res_usage = result["system"]["resources"]
        
        # Analyze token generation efficiency
        peak_speed = speeds["completion"]["peak"]
        avg_speed = speeds["completion"]["average"]
        if peak_speed > 0:
            token_efficiency = avg_speed / peak_speed
            if token_efficiency < 0.5:
                insights.append(f"{model}: High token generation variance - achieving {token_efficiency:.1%} of peak performance")
            
        # Analyze resource utilization
        if res_usage and res_usage.get("gpu"):
            gpu_efficiency = res_usage["gpu"]["load"]["mean"] / 100
            if gpu_efficiency < 0.7:
                insights.append(f"{model}: Low GPU utilization ({gpu_efficiency:.1%})")
            
    return insights

def print_results(avg_result):
    """Print benchmark results in a formatted way"""
    print("\nResults:\n")
    print("-" * 60)
    print(f"\t{avg_result['model_name']}")
    print(f"\t\tPrompt eval: {avg_result['speeds']['prompt_eval']:.2f} t/s")
    print(f"\t\tResponse: {avg_result['speeds']['response']:.2f} t/s")
    print(f"\t\tTotal: {avg_result['speeds']['total']:.2f} t/s")
    print(f"\t\tPeak completion: {avg_result['speeds']['completion']['peak']:.2f} t/s\n")
    
    print("\tPerformance:")
    print(f"\t\tPrompt tokens: {avg_result['performance']['prompt_tokens']:.2f}")
    print(f"\t\tResponse tokens: {avg_result['performance']['response_tokens']:.2f}")
    print(f"\t\tModel load time: {avg_result['performance']['model_load_time']:.2f}s")
    print(f"\t\tPrompt eval time: {avg_result['performance']['prompt_eval_time']:.2f}s")
    print(f"\t\tResponse time: {avg_result['performance']['response_time']:.2f}s")
    print(f"\t\tTotal time: {avg_result['performance']['total_time']:.2f}s")
    print("-" * 60)

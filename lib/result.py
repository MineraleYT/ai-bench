import numpy as np

class BenchmarkResult:
    def __init__(self, model_name):
        self.model_name = model_name
        self.prompt_tokens = 0
        self.response_tokens = 0
        self.model_load_time = 0
        self.prompt_eval_time = 0
        self.response_time = 0
        self.total_time = 0
        self.completion_tokens_per_second = []
        self.resources_usage = None
        self.system_specs = None
        
    def calculate_metrics(self):
        self.prompt_eval_speed = self.prompt_tokens / self.prompt_eval_time if self.prompt_eval_time > 0 else 0
        self.response_speed = self.response_tokens / self.response_time if self.response_time > 0 else 0
        self.total_speed = (self.prompt_tokens + self.response_tokens) / self.total_time if self.total_time > 0 else 0
        self.avg_completion_speed = np.mean(self.completion_tokens_per_second) if self.completion_tokens_per_second else 0
        self.peak_completion_speed = np.max(self.completion_tokens_per_second) if self.completion_tokens_per_second else 0
        
    def to_dict(self):
        return {
            "model_name": self.model_name,
            "performance": {
                "prompt_tokens": self.prompt_tokens,
                "response_tokens": self.response_tokens,
                "model_load_time": round(self.model_load_time, 2),
                "prompt_eval_time": round(self.prompt_eval_time, 2),
                "response_time": round(self.response_time, 2),
                "total_time": round(self.total_time, 2)
            },
            "speeds": {
                "prompt_eval": round(self.prompt_eval_speed, 2),
                "response": round(self.response_speed, 2),
                "total": round(self.total_speed, 2),
                "completion": {
                    "average": round(self.avg_completion_speed, 2),
                    "peak": round(self.peak_completion_speed, 2)
                }
            },
            "system": {
                "specs": self.system_specs,
                "resources": self.resources_usage
            }
        }

import psutil
import GPUtil
import cpuinfo
import numpy as np
import time

class SystemInfo:
    @staticmethod
    def get_system_specs():
        try:
            cpu_info = cpuinfo.get_cpu_info()
            freq = cpu_info.get('hz_actual_friendly', 'Unknown')
            brand = cpu_info.get('brand_raw', 'Unknown CPU')
        except Exception:
            freq = "Unknown"
            brand = "Unknown CPU"
            
        specs = {
            "cpu": {
                "model": brand,
                "cores": psutil.cpu_count(logical=False),
                "threads": psutil.cpu_count(logical=True),
                "frequency": freq
            }
        }
        
        if GPUtil.getGPUs():
            specs["gpu"] = [{"name": gpu.name} for gpu in GPUtil.getGPUs()]
            
        return specs

    @staticmethod
    def monitor_resources(duration):
        samples = []
        end_time = time.time() + duration
        
        while time.time() < end_time:
            cpu = psutil.cpu_percent(interval=0.1)
            gpu_data = None
            
            if GPUtil.getGPUs():
                gpu = GPUtil.getGPUs()[0]
                gpu_data = {"load": gpu.load * 100, "temperature": gpu.temperature}
                
            samples.append((cpu, gpu_data))
            time.sleep(0.1)
            
        cpu_samples = [s[0] for s in samples]
        
        result = {
            "cpu": {
                "mean": np.mean(cpu_samples),
                "max": np.max(cpu_samples),
                "std": np.std(cpu_samples)
            }
        }
        
        if any(s[1] for s in samples):
            gpu_loads = [s[1]["load"] for s in samples if s[1]]
            gpu_temps = [s[1]["temperature"] for s in samples if s[1]]
            
            result["gpu"] = {
                "load": {
                    "mean": np.mean(gpu_loads),
                    "max": np.max(gpu_loads),
                    "std": np.std(gpu_loads)
                },
                "temperature": {
                    "mean": np.mean(gpu_temps),
                    "max": np.max(gpu_temps),
                    "std": np.std(gpu_temps)
                }
            }
            
        return result

# 🚀 AI Benchmark

A comprehensive benchmarking tool for evaluating Local LLM performance using Ollama. Measure speed, resource usage, and compare different models with detailed metrics.

## ✨ Features

- **🔄 Multi-Model Testing**: Benchmark multiple models in a single run
- **📊 Performance Metrics**:
  - Token generation speed (tokens/s)
  - Model load time
  - Prompt evaluation time
  - Response generation time
- **📈 Resource Monitoring**:
  - CPU usage (average & peak)
  - GPU utilization (if available)
- **🎯 Interactive Interface**:
  - Model selection
  - Custom prompt input
  - Verbose output option
- **🔧 Model Management**:
  - Download models
  - List installed models
  - Remove unused models

## 🛠️ Prerequisites

- Python 3.12+
- [Ollama](https://ollama.com/) installed and running

## ⚡ Quick Start

1. Clone the repository:
```bash
git clone https://github.com/mineraleyt/ai-bench.git
cd ai-bench
```

2. Set up the environment:

macOS/Linux:
```bash
source setup.sh  # or . setup.sh
```

Windows:
```cmd
setup.bat
```

3. Start benchmarking:
```bash
python main.py
```

## 📖 Usage Guide

### 🏃 Running Benchmarks

1. Start the tool: `python main.py`
2. Select "Run benchmark" from the menu
3. Configure your benchmark:
   - Choose models to test (or benchmark all)
   - Enable verbose mode for detailed output
   - Add custom prompts (optional)
4. View results in the terminal and find detailed logs in `results/`

### 🤖 Managing Models

The tool provides a model management interface to:
- Download new models from [ollama.com/library](https://ollama.com/library)
- List all installed models with their sizes
- Remove models you no longer need

### 💡 Example Prompts

Default prompts test various aspects of model performance:
- Complex reasoning (quantum computing concepts)
- Code generation (algorithm implementations)
- Technical explanation (transformer architecture)
- Abstract concepts (algorithmic complexity)

### 📊 Results

Benchmark results are saved in:
- `results/`: JSON files with detailed metrics
- `logs/`: Detailed execution logs

Each result includes:
- Token generation speeds
- Timing metrics
- Resource utilization
- System information

## 🏗️ Architecture

The benchmark runs in these phases:
1. Model loading
2. Prompt evaluation
3. Response generation
4. Resource monitoring
5. Metrics calculation
6. Results storage

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT - See [LICENSE](LICENSE) for details.

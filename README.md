# AutoBiota 🧬🦠

- AutoBiota is an intelligent microbiome analysis tool that combines machine learning with conversational AI to analyze gut microbiome data and predict disease status. 
- The system uses a LangChain agent with multiple specialized tools to handle the complete analysis pipeline from data preprocessing to report generation.

## Features

- **Automated Data Preprocessing**: Clean and prepare microbiome CSV data for analysis
- **Disease Classification**: Train ML models to classify healthy vs diseased samples
- **Model Evaluation**: Comprehensive model performance assessment
- **Diversity Analysis**: Compute alpha diversity metrics from microbiome data
- **Visualization**: Generate PCA plots and other visualizations
- **Report Generation**: Automatically create DOCX reports with results and explanations
- **Conversational Interface**: Natural language interaction with the analysis pipeline

## Project Structure

```
autobiota/
├── main.py                    # Main agent entry point
├── pipeline/                  # Analysis pipeline modules
│   ├── preprocess.py         # Data preprocessing
│   ├── train.py              # Model training
│   ├── evaluate.py           # Model evaluation
│   ├── predict.py            # Disease prediction
│   ├── diversity.py          # Diversity calculations
│   ├── plots.py              # Visualization generation
│   └── report.py             # Report generation
├── data/                     # Data directory
│   ├── sample.csv            # Raw microbiome data
│   └── sample_preprocessed.csv # Processed data
├── outputs/                  # Output directory
│   ├── model/                # Trained models
│   ├── eval/                 # Evaluation results
│   ├── plots/                # Generated plots
│   └── reports/              # Generated reports
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## Data Format

The system expects microbiome data in CSV format with the following structure:

- `sample_id`: Unique identifier for each sample
- Bacterial abundance columns (e.g., `Bacteroides`, `Faecalibacterium`, `Prevotella`, etc.)
- `label`: Classification label (`healthy` or `diseased`)

Example:
```csv
sample_id,Bacteroides,Faecalibacterium,Prevotella,Ruminococcus,Clostridium,Akkermansia,Escherichia,label
S1,0.341,0.226,0.133,0.165,0.048,0.057,0.029,healthy
S2,0.317,0.277,0.053,0.201,0.072,0.062,0.018,healthy
...
```

## Installation

1. **Prerequisites**: Ensure you have Python 3.12+ installed

2. **Clone the repository**:
   ```bash
   git clone https://github.com/ryzary/autobiota.git
   cd autobiota
   ```

3. **Install dependencies using uv**:
   ```bash
   # Install uv if you haven't already
   pip install uv
   
   # Install project dependencies
   uv sync
   ```

4. **Set up Ollama** (required for the AI agent):
   ```bash
   # Install Ollama (macOS)
   brew install ollama
   
   # Pull the required model
   ollama pull gemma3n
   ```

## Usage

### Interactive Mode
Run a model using ollama:
```
ollama run gemma3n
```

Open a new terminal and the agent interactively and provide custom instructions:

```bash
uv run main.py
```

You'll be prompted to enter your analysis request, or press Enter to run the default pipeline.

### Command Line Mode

Provide instructions directly via command line:

```bash
uv run main.py "Analyze the microbiome data and generate a comprehensive report"
```

### Default Pipeline

The default pipeline performs the following steps:
1. Preprocesses raw data from `data/sample.csv`
2. Trains a Random Forest disease classifier
3. Evaluates model performance
4. Generates PCA visualizations
5. Creates a comprehensive DOCX report

## Available Tools

The AI agent has access to the following specialized tools:

- **PreprocessData**: Clean and prepare microbiome CSV data
- **TrainModel**: Train Random Forest classifier for disease prediction
- **EvaluateModel**: Assess model performance with metrics and validation
- **PredictDisease**: Make predictions on new microbiome samples
- **ComputeDiversity**: Calculate alpha diversity metrics
- **PlotPCA**: Generate PCA visualizations colored by health status
- **GenerateReport**: Create comprehensive DOCX reports

## Dependencies

- **langchain**: AI agent framework
- **langchain-ollama**: Ollama integration for local LLM
- **scikit-learn**: Machine learning algorithms
- **xgboost**: Gradient boosting (alternative classifier)
- **pandas**: Data manipulation
- **matplotlib**: Plotting and visualization
- **python-docx**: DOCX report generation
- **joblib**: Model serialization

## Example Queries

You can interact with the system using natural language:

- "Preprocess the data and train a model to classify disease status"
- "Generate a PCA plot showing the separation between healthy and diseased samples"
- "Compute diversity metrics for all samples and include them in a report"
- "Evaluate the model performance and show me the confusion matrix"

## Output Files

The system generates various outputs in the `outputs/` directory:

- **Models**: Trained classifiers saved as `.joblib` files
- **Evaluations**: Model performance metrics and validation results
- **Plots**: PCA plots and other visualizations as image files
- **Reports**: Comprehensive DOCX reports with analysis results

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Built with [LangChain](https://langchain.com/) for AI agent capabilities
- Uses [Ollama](https://ollama.ai/) for local LLM inference
- Microbiome analysis powered by scikit-learn and pandas

---

*AutoBiota: Automating microbiome analysis with AI* 🧬✨

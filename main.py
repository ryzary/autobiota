from langchain.agents import initialize_agent, Tool
from pipeline import preprocess, train, evaluate, predict, diversity, plots, report
from langchain_ollama import OllamaLLM


# --- Define Tools ---
tools = [
    Tool(
        name="PreprocessData",
        func=preprocess.preprocess_data,
        description="Intelligently preprocess microbiome data CSV file. Automatically detects column names, data orientation (samples in rows/columns), sample IDs, labels, and bacterial abundance columns. Automatically finds and merges metadata files containing labels for ML training. Handles various data formats flexibly with smart sample ID matching. Input should be the relative file path as a string without quotes, e.g. data/sample.csv."
    ),
    Tool(
        name="TrainModel",
        func=train.train_model,
        description="Trains a disease classifier model from preprocessed data."
    ),
    Tool(
        name="EvaluateModel",
        func=evaluate.evaluate_model,
        description="Evaluates the trained model using preprocessed data with labels."
    ),
    Tool(
        name="PredictDisease",
        func=predict.predict_from_model,
        description="Predicts disease status using the trained model and new microbiome data."
    ),
    Tool(
        name="ComputeDiversity",
        func=diversity.compute_diversity,
        description="Computes alpha diversity from microbiome data."
    ),
    Tool(
        name="PlotPCA",
        func=plots.plot_results,
        description="Plots PCA of microbiome features colored by label (if available)."
    ),
    Tool(
        name="GenerateReport",
        func=report.generate_report,
        description="Generate a comprehensive DOCX report with analysis summary, methodology, results, and conclusions. Automatically includes evaluation metrics and plots."
    )
]

# --- Create Agent ---
llm = OllamaLLM(model="gemma3n")
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True
)

# --- Run Gut Microbiome Analysis Agent ---

if __name__ == "__main__":
    import sys

    print("\n🧬 Welcome to the Gut Microbiome Agent 🦠")
    print("Type a custom instruction or press [Enter] to run the full pipeline.\n")

    default_query = (
        "1. Use PreprocessData tool to process data/ZellerG_2014.csv (metadata labels will be automatically detected and merged). "
        "2. Train a disease classifier model using the preprocessed data with merged labels. "
        "3. Evaluate the trained model performance with classification metrics. "
        "4. Compute diversity metrics from the preprocessed microbiome data. "
        "5. Generate PCA plots showing separation between disease groups and save to outputs/plots directory. "
        "6. Generate a comprehensive DOCX report with analysis results and save to outputs/reports directory."
    )

    # Accept query from command-line or user input
    query = sys.argv[1] if len(sys.argv) > 1 else input("📝 Your prompt: ").strip()
    if not query:
        query = default_query
        print("\n⚙️  Using default query...\n")

    print("🚀 Starting agent...\n")

    # For streaming (if supported by your agent)
    try:
        for step in agent.stream(query):
            print(step)
    except AttributeError:
        # Fallback if stream() is not implemented
        result = agent.run(query)
        print("\n✅ Final Result:\n", result)

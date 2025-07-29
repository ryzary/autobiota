from langchain.agents import initialize_agent, Tool
from pipeline import preprocess, train, evaluate, predict, diversity, plots, report
from langchain_ollama import OllamaLLM


# --- Define Tools ---
tools = [
    Tool(
        name="PreprocessData",
        func=preprocess.preprocess_data,
        description="Preprocess microbiome data CSV file. Input should be the relative file path as a string without quotes, e.g. data/sample.csv."
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
        description="Generate DOCX report from text summary and plot image file paths."
    )
]

# --- Create Agent ---
llm = OllamaLLM(model="gemma3n")
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# --- Run Gut Microbiome Analysis Agent ---

if __name__ == "__main__":
    import sys

    print("\n🧬 Welcome to the Gut Microbiome Agent 🦠")
    print("Type a custom instruction or press [Enter] to run the full pipeline.\n")

    default_query = (
        "Preprocess the raw data data/sample.csv. Saved the preprocessed data to data/sample_preprocessed.csv. "
        "Train and evaluate a disease classifier using data/preprocessed_data.csv"
        "Generate plots and save them into the plots directory."
        "Produce a DOCX report containing the model evaluation result, plots, and explanations. Save it into the report directory"
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
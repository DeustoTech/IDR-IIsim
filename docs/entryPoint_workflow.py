from graphviz import Digraph

# Create a directed graph for the flowchart
flowchart = Digraph("Setup_Flowchart", format="png")
flowchart.attr(rankdir="TB")  # Top-to-bottom layout

# Add nodes
flowchart.node("Start", "Start: setup.py", shape="ellipse", fontsize="12")
flowchart.node("Main", "Call main()", shape="box", fontsize="12")
flowchart.node("Init", "Initialize (init())", shape="box", fontsize="12")
flowchart.node("LoadConfigYAML", "Load config.yaml", shape="box", fontsize="12")
flowchart.node("Config", "Load Config (config.py)", shape="box", fontsize="12")
flowchart.node("ValidateSchema", "Validate Schema (schema.py)", shape="box", fontsize="12")
flowchart.node("ScanIndustry", "Scan industry/", shape="box", fontsize="12")
flowchart.node("DiscoverModels", "Discover Models (models_dict.py)", shape="box", fontsize="12")
flowchart.node("RegisterModels", "Register Models (models_dict.py)", shape="box", fontsize="12")
flowchart.node("GenerateQueue", "Generate Execution Queue (execution.py)", shape="box", fontsize="12")
flowchart.node("ExecuteModels", "Execute Models (model.py)", shape="box", fontsize="12")
flowchart.node("LogStatus", "Log Status (logger.py)", shape="box", fontsize="12")
flowchart.node("End", "End Execution", shape="ellipse", fontsize="12")

# Add edges
flowchart.edge("Start", "Main")
flowchart.edge("Main", "Init")
flowchart.edge("Init", "LoadConfigYAML")
flowchart.edge("LoadConfigYAML", "Config")
flowchart.edge("Config", "ValidateSchema")
flowchart.edge("ValidateSchema", "ScanIndustry")
flowchart.edge("ScanIndustry", "DiscoverModels")
flowchart.edge("DiscoverModels", "RegisterModels", "Register models", fontsize="10")
flowchart.edge("RegisterModels", "GenerateQueue", "Create execution order", fontsize="10")
flowchart.edge("GenerateQueue", "ExecuteModels", "Run model calculations", fontsize="10")
flowchart.edge("ExecuteModels", "LogStatus", "Log results/errors", fontsize="10")
flowchart.edge("LogStatus", "End", "Complete execution", fontsize="10")

# Save and render the diagram
output_path = "./docs/Setup_Flowchart"
flowchart.render(output_path, cleanup=True)

output_path + ".png"
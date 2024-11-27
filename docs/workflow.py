from graphviz import Digraph

# Create a directed graph
dependency_diagram = Digraph("Detailed_Dependency_Graph", format="png")
dependency_diagram.attr(rankdir="TB")  # Top-to-bottom layout

# Add nodes
dependency_diagram.node("Setup", "setup.py", shape="box")
dependency_diagram.node("Config", "utils/config.py", shape="box")
dependency_diagram.node("Schema", "utils/schema.py", shape="box")
dependency_diagram.node("Execution", "utils/execution.py", shape="box")
dependency_diagram.node("Logger", "utils/logger.py", shape="box")
dependency_diagram.node("ModelsDict", "utils/models_dict.py", shape="box")
dependency_diagram.node("IndustryModel", "industry/.../model.py", shape="box")
dependency_diagram.node("BaseModel", "models/model.py", shape="box")
dependency_diagram.node("PyYAML", "PyYAML", shape="ellipse", style="filled", fillcolor="lightgray")
dependency_diagram.node("JSON", "JSON", shape="ellipse", style="filled", fillcolor="lightgray")
dependency_diagram.node("template_script", "template_script", shape="box", style="filled", fillcolor="lightgray")
dependency_diagram.node("generated_png", "model.png", shape="ellipse", style="filled", fillcolor="lightblue")
dependency_diagram.node("generated_script", "model_script.png", shape="ellipse", style="filled", fillcolor="lightblue")

# Add edges
dependency_diagram.edge("Setup", "Config", "Load configuration", fontsize="10")
dependency_diagram.edge("Setup", "Schema", "Validate schemas", fontsize="10")
dependency_diagram.edge("Setup", "Execution", "Execute workflows", fontsize="10")
dependency_diagram.edge("Schema", "PyYAML", "Validates YAML", fontsize="10")
dependency_diagram.edge("Schema", "JSON", "Validates JSON schema", fontsize="10")
dependency_diagram.edge("Config", "PyYAML", "Uses PyYAML", fontsize="10")
dependency_diagram.edge("Setup", "ModelsDict", "Registers models", fontsize="10")
dependency_diagram.edge("ModelsDict", "Execution", "Resolve dependencies   ", fontsize="10")
dependency_diagram.edge("ModelsDict", "IndustryModel", "Discovers models", fontsize="10")
dependency_diagram.edge("IndustryModel", "BaseModel", "Inherits from BaseModel", fontsize="10")
dependency_diagram.edge("Logger", "Config", "Logs errors", fontsize="10")
dependency_diagram.edge("BaseModel", "template_script", "uploads template script     ", fontsize="10")
dependency_diagram.edge("BaseModel", "generated_png", "Gegenerated PNG", fontsize="10")
dependency_diagram.edge("BaseModel", "generated_script", "Generated model script", fontsize="10") 

# Save the diagram
output_path = "./docs/workflow_setup"
dependency_diagram.render(output_path, cleanup=True)

output_path + ".png"
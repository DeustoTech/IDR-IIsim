from graphviz import Digraph

# Create an updated UML Sequence Diagram including the call to model.py for creating the model class
yaml_model_sequence = Digraph("YAML_Model_Sequence_Diagram", format="png")
yaml_model_sequence.attr(rankdir="TB")  # Top-to-bottom layout

# Define participants
yaml_model_sequence.node("User", "User", shape="box")
yaml_model_sequence.node("Setup", "setup.py", shape="box")
yaml_model_sequence.node("ConfigLoader", "utils/config.py", shape="box")
yaml_model_sequence.node("SchemaLoader", "utils/schema.py", shape="box")
yaml_model_sequence.node("Validator", "Validator", shape="box")
yaml_model_sequence.node("Model", "models/model.py", shape="box")

# Define interactions
yaml_model_sequence.edge("User", "Setup", "Provides .yaml file for validation", fontsize="10")
yaml_model_sequence.edge("Setup", "ConfigLoader", "Loads .yaml file", fontsize="10")
yaml_model_sequence.edge("ConfigLoader", "SchemaLoader", "Loads schema for validation", fontsize="10")
yaml_model_sequence.edge("SchemaLoader", "Validator", "Validates .yaml against schema", fontsize="10")
yaml_model_sequence.edge("Validator", "SchemaLoader", "Returns validation result", fontsize="10")
yaml_model_sequence.edge("SchemaLoader", "ConfigLoader", "Validation result forwarded", fontsize="10")
yaml_model_sequence.edge("ConfigLoader", "Setup", "Validation result returned", fontsize="10")
yaml_model_sequence.edge("Setup", "Model", "Creates model class from validated data", fontsize="10")
yaml_model_sequence.edge("Model", "Setup", "Returns instantiated model class", fontsize="10")
yaml_model_sequence.edge("Setup", "User", "Displays model creation result", fontsize="10")

# Save the updated sequence diagram
yaml_model_sequence_path = "./docs/YAML_Model_Sequence_Diagram"
yaml_model_sequence.render(yaml_model_sequence_path, cleanup=True)

yaml_model_sequence_file = f"{yaml_model_sequence_path}.png"
yaml_model_sequence_file

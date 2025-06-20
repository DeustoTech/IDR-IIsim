__package__ = "models"

from functools import partial
import os
import graphviz
import yaml
from sympy import parse_expr, Array, Matrix
from idr_iisim.utils.logger import i_logger
from idr_iisim.utils.types import ModelStruct, ArgumentStruct
from string import Template  # Use Template for substitution


def generate_centered_list(num_elements: int) -> list[int]:
    """
    Generate a list of integers centered around 0.

    Args:
        num_elements (int): The number of elements in the list.

    Returns:
        list[int]: A list of integers centered around 0.

    Example:
        >>> generate_centered_list(3)
        [-1, 0, 1]
    """
    if num_elements % 2 == 0:
        # Even number of elements
        half = num_elements // 2
        return list(range(-half, half))
    else:
        # Odd number of elements
        half = num_elements // 2
        return list(range(-half, half + 1))


class Model:
    """Model class that represents a model in the system.
    It contains the model configuration, functions map, results, and external inputs.
    """

    directory: str
    model_config: str
    config: ModelStruct
    functions_map: dict
    results: dict[str, Matrix] = {}
    external_inputs: dict[
        str, dict[str, Matrix]
    ] = {}  # dict[model_id, dict[arg_name, value]]

    txt_constants: str = ""

    def setup(self) -> None:
        """Reads the model configuration file and sets up the model for calculation.
        Args: None
        Returns: None
        """
        # read config file
        try:
            with open(self.model_config) as file:
                data: dict = yaml.safe_load(file)
            self.config = ModelStruct(**data)
        except Exception as e:
            raise e

        # read functions
        self.functions_map = {}
        for output in self.config.outputs:
            operation = parse_expr(output["operation"])
            f = partial(lambda op, **kwargs: op.subs(kwargs), op=operation)
            key = output["name"]
            self.functions_map[key] = dict(
                function=f,
                args=output["args"],
                expression=operation,
                description=output["description"],
            )

        i_logger.logger.debug(f"setup completed for {self.config.name}")
        i_logger.logger.debug(f"functions_map: \n{self.functions_map}")
        pass

    def prepare_calculation(
        self, model_id: str, outputs: dict[str, float]
    ) -> None:
        """Prepares the external inputs for the calculation of a model.
        Args:
            model_id (str): The identifier of the model.
            outputs (dict[str, float]): The outputs of the model.
        Returns: None
        """
        self.external_inputs[model_id] = outputs
        i_logger.logger.debug(f"external inputs: {self.external_inputs}")
        pass

    def calculate(self) -> None:
        """Iterates through a functions_map, which likely maps variable names to functions and their required arguments.
        1. Fetches and prepares arguments from: inputs, constants, or external inputs.
        2. Executes the function associated with each variable in the functions_map.
        3. Stores the computed result in a results attribute.
        4. Prints the result.

        Argds: None
        Returns: None
        """

        i_logger.logger.debug(f"calculating {self.config.name}")
        for variable_name in self.functions_map:
            # Iterates over each variable name in self.functions_map.
            # Fetching and Preparing Arguments
            outputs = self.functions_map[variable_name]
            i_logger.logger.debug(f"calculating {variable_name}")
            args = {}
            for arg in outputs["args"]:
                # Iterating over args, eaah arg contains a type & a name.
                type_arg = arg["type"]
                arg_name = arg["name"]
                value: Matrix | float
                if type_arg == "outputs":
                    # Fetch its value from self.results & Convert the value to a Matrix.
                    if isinstance(self.results[arg_name], Matrix):
                        value = Matrix(self.results[arg_name])
                    else:
                        value = Matrix([[self.results[arg_name]]])
                else:
                    list_type = getattr(self.config, type_arg)
                    input_arg = next(
                        x for x in list_type if x["name"] == arg_name
                    )

                    if type_arg == "inputs":
                        from_value: str = input_arg["from"]
                        if from_value is not None:
                            # the input is the output of another process
                            value = Matrix(
                                self.external_inputs[from_value][arg_name]
                            )
                        else:
                            value = Matrix(input_arg["value"])
                        # i_logger.logger.debug(f"input {arg_name} = {value}")
                    else:
                        # value is a constant
                        value = input_arg["value"]

                args[arg_name] = value
                i_logger.logger.debug(f"arg {arg_name} = {value}")

            # calculate the output & Store and Print the Result
            fn = outputs["function"]
            result = fn(**args)
            self.results[variable_name] = result
            print(f"{variable_name} = {result}")
        i_logger.logger.debug(f"finished calculating {self.config.name}")
        return None

    def print_diagram(self):
        """generates and exports a diagram in PNG format that visually represents
        the inputs, outputs, and processing flow of a model.

        Args: None
        Returns: None
        """
        i_logger.logger.debug(f"printing diagram (png) {self.config.name}")

        # Initialize Graphviz - Initializes a new directed graph (Digraph) with a comment identifying the model (self.config.name).
        graphviz.set_default_engine("neato")
        dot = graphviz.Digraph(comment=self.config.name)

        # Graph attributes - Adjusts visual: Padding, margins, and spacing are set for better readability.
        # Direction left-to-right layout (LR), Node shapes are set to BOX.
        # Adds a placeholder node input_line to organize inputs && add a central node representing
        #      the model (self.config.name) at position (0, 0).
        dot.attr(
            pad="0.5", margin="0.5", ranksep="0.5", nodesep="0.5", rankdir="LR"
        )
        dot.node_attr.update(shape="box")
        dot.node("input_line", shape="point", width="0")
        dot.node(self.config.name, label=self.config.name, pos="0,0!")

        # print inputs
        # Enumerate the inputs and generate a list of positions centered around 0.
        inputs_blocks = enumerate(self.config.inputs)
        positions_list = generate_centered_list(len(self.config.inputs))
        for i, input_block in inputs_blocks:
            """Add Input Nodes and Edges for each input block"""
            position = f"-2,{positions_list[i]}!"
            # input nodo name and value
            input_nodo = f"*{input_block['name']} = {input_block['value']}"
            # dot.node(input_nodo, shape='point', width='0', rank='same', pos=position)
            dot.node(
                input_block["name"],
                shape="point",
                width="0",
                rank="same",
                pos=position,
            )
            dot.edge(
                input_block["name"],
                self.config.name,
                label=input_block["label"],
                color="black",
                fontcolor="black",
                tailport="e",
                headport="w",
            )

        # print outputs and edges for each output block
        outputs_blocks = enumerate(self.config.outputs)
        positions_list = generate_centered_list(len(self.config.outputs))
        for i, output_block in outputs_blocks:
            position = f"2,{positions_list[i]}!"
            dot.node(
                output_block["name"],
                shape="point",
                width="0",
                orientation="90",
                pos=position,
            )
            dot.edge(
                self.config.name,
                output_block["name"],
                label=output_block["label"],
                color="black",
                fontcolor="black",
                tailport="e",
                headport="w",
            )

        # Export the diagram in PNG format.
        dot.render(
            filename="model",
            directory=self.directory,
            format="png",
            cleanup=True,
        )
        i_logger.logger.debug(f"finished printing {self.config.name}")
        pass

    def script_generator(
        self, template_path: str, generated_model_script_filename: str
    ) -> None:
        """Generates a Python script that contains the constants and operations of the model.
        Args:
            template_path (str): The path to the template file.
        Returns: None
        """
        import os
        from string import Template

        # Initialize variables for template placeholders
        log_library = ""
        log_message = ""
        constants_code = ""
        args_code = ""
        operations_code = ""
        results_code = "{"  # Start of dictionary
        return_code = ""

        i_logger.logger.debug(
            f"Generating script for model: {self.config.name}"
        )
        i_logger.logger.debug(f"Template path: {template_path}")

        # Load the template content
        try:
            with open(template_path, "r") as template_file:
                template_content = template_file.read()
        except FileNotFoundError:
            i_logger.logger.error(f"Template file not found: {template_path}")
            raise
        except Exception as e:
            i_logger.logger.error(f"Error reading template file: {e}")
            raise

        # Create a Template object
        script_template = Template(template_content)

        # Generate constants dynamically from model configuration
        constants_code = "\n".join(
            f"{constant['name']} = {constant['value']}  # {constant['description']}"
            for constant in self.config.constants
        )

        # Process functions map
        for variable_name, outputs in self.functions_map.items():
            # Operations and results
            operations_code += f"# {outputs['description']}\n    {variable_name} = {outputs['expression']}\n"
            results_code += f' "{variable_name}" : {variable_name},'
            return_code += f' "{variable_name}" : {variable_name},'
            i_logger.logger.debug(f"Processing variable: {variable_name}")

            # Prepare arguments
            args = {}
            for arg in outputs["args"]:
                arg_type = arg["type"]
                arg_name = arg["name"]

                if arg_type == "outputs":
                    # Value from previous results
                    if isinstance(self.results[arg_name], Matrix):
                        value = Matrix(self.results[arg_name])
                    else:
                        value = Matrix([[self.results[arg_name]]])
                else:
                    # Input or constant
                    source_list = getattr(self.config, arg_type)
                    input_data = next(
                        x for x in source_list if x["name"] == arg_name
                    )
                    if arg_type == "inputs":
                        args_code += f" {arg_name},"
                        from_value = input_data.get("from")
                        value = (
                            Matrix(self.external_inputs[from_value][arg_name])
                            if from_value
                            else Matrix(input_data["value"])
                        )
                    else:
                        value = input_data["value"]

                args[arg_name] = value
                i_logger.logger.debug(f"Argument {arg_name}: {value}")

        # Process and clean arguments list
        args_list = sorted(set(args_code.split(",")[:-1]))
        args_code = ", ".join(args_list)

        # Directory adjustments
        dir_path = (
            self.directory.replace(os.getcwd(), ".")
            .replace(".\\", "")
            .replace("\\", ".")
        )

        # Prepare logging details if in debug mode
        if self.config.debug:
            log_library = (
                "import logging\n"
                "# Configure logging\n"
                "logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')"
            )
            log_message = "logging.debug(results)"

        # Finalize results dictionary
        results_code = results_code[:-1] + "}"

        # Substitute template variables
        script_content = script_template.substitute(
            log_library=log_library,
            directory=f'"{dir_path}"',
            method_name=self.config.name,
            method_description=self.config.description,
            args=args_code,
            constants=constants_code,
            function_industrial_method=self.config.id.replace("-", "_"),
            operations=operations_code,
            results=results_code,
            log_msg=log_message,
            return_values=return_code[:-1],
        )

        # Define output path and write script
        script_path = os.path.join(
            self.directory, generated_model_script_filename
        )
        i_logger.logger.debug(f"Saving script to: {script_path}")

        try:
            with open(script_path, "w") as script_file:
                script_file.write(script_content)
        except Exception as e:
            i_logger.logger.error(f"Error writing script to file: {e}")
            raise

        i_logger.logger.debug(
            f"Script successfully generated at: {script_path}"
        )


run = Model()

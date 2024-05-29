__package__ = "models"

from functools import partial
import graphviz
import yaml
from sympy import parse_expr, Array, Matrix
from idr_iisim.utils.logger import i_logger
from idr_iisim.utils.types import ModelStruct, ArgumentStruct


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
    directory: str
    model_config: str
    config: ModelStruct
    functions_map: dict
    results: dict[str, Matrix] = {}
    external_inputs: dict[str, dict[str, Matrix]] = {}  # dict[model_id, dict[arg_name, value]]

    def setup(self) -> None:
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
            self.functions_map[key] = dict(function=f, args=output["args"], expression=operation)
        pass

    def prepare_calculation(self, model_id: str, outputs: dict[str, float]) -> None:
        self.external_inputs[model_id] = outputs
        pass

    def calculate(self) -> None:
        i_logger.logger.debug(f"calculating {self.config.name}")
        for variable_name in self.functions_map:
            # get the value of the args
            outputs = self.functions_map[variable_name]
            args = {}
            for arg in outputs["args"]:
                type_arg = arg["type"]
                arg_name = arg["name"]
                value: Matrix | float
                if type_arg == "outputs":
                    value = Matrix(self.results[arg_name])
                else:
                    list_type = getattr(self.config, type_arg)
                    input_arg = next(x for x in list_type if x["name"] == arg_name)

                    if type_arg == "inputs":
                        from_value: str = input_arg["from"]
                        if from_value is not None:
                            # the input is the output of another process
                            value = Matrix(self.external_inputs[from_value][arg_name])
                        else:
                            value = Matrix(input_arg["value"])
                    else:
                        # value is a constant
                        value = input_arg["value"]

                args[arg_name] = value

            # calculate the output
            fn = outputs["function"]
            result = fn(**args)
            self.results[variable_name] = result
            print(f"{variable_name} = {result}")
        i_logger.logger.debug(f"finished calculating {self.config.name}")
        return None

    def print_diagram(self):
        i_logger.logger.debug(f"printing {self.config.name}")
        graphviz.set_default_engine("neato")
        dot = graphviz.Digraph(comment=self.config.name)

        dot.attr(pad='0.5', margin='0.5', ranksep='0.5', nodesep='0.5', rankdir='LR')
        dot.node_attr.update(shape='box')
        dot.node('input_line', shape='point', width='0')
        dot.node(self.config.name, label=self.config.name, pos='0,0!')

        # print inputs
        inputs_blocks = enumerate(self.config.inputs)
        positions_list = generate_centered_list(len(self.config.inputs))
        for (i, input_block) in inputs_blocks:
            position = f'-2,{positions_list[i]}!'
            dot.node(input_block["name"], shape='point', width='0', rank='same', pos=position)
            dot.edge(input_block["name"], self.config.name, label=input_block["label"], color='black',
                     fontcolor='black', tailport='e', headport='w')

        # print outputs
        outputs_blocks = enumerate(self.config.outputs)
        positions_list = generate_centered_list(len(self.config.outputs))
        for (i, output_block) in outputs_blocks:
            position = f'2,{positions_list[i]}!'
            dot.node(output_block["name"], shape='point', width='0', orientation='90', pos=position)
            dot.edge(self.config.name, output_block["name"], label=output_block["label"], color='black',
                     fontcolor='black', tailport='e', headport='w')

        dot.render(filename="model", directory=self.directory, format="png", cleanup=True)
        i_logger.logger.debug(f"finished printing {self.config.name}")
        pass


run = Model()

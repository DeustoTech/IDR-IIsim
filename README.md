# IDR-IIsim
Repository with industry models tailored to the integration on large scale energy system models and circular economy assessment

## Data Model
Check the [data model](docs/model.md) to understand how the data is structured.

## Execution
The tool can be executed by running the following commands:
```bash
# install dependencies
pip install -r requirements.txt

# run the tool
python setup.py
```

As a result of the execution, the tool will print the results in the console and will generate the model diagrams in the
method folders. The diagrams will be saved as `model.png`.

## Next steps
- [ ] Add support for vectorized outputs. For the moment, the tool only supports scalar values.
- [ ] Add support for recursive operations.
- [ ] Improve diagrams visualizations.
- [ ] Add support for debug mode.
- [ ] Add results folder where the results of the execution will be saved. It might be necessary to include a new
      section in the `model.yaml` file to define the values that are considered as results.
__package__ = "utils"

from idr_iisim.utils.models_dict import models_dict


def walk_dependencies(q: list[str], key: str):
    deps = models_dict.dependencies
    if not key in deps:
        return q

    for i in deps[key]:
        q.append(i)
        return walk_dependencies(q, i)


def generate_execution_queue(model_id: str) -> list[str]:
    execution_queue: list[str] = [model_id]

    # walk dependencies recursively
    execution_queue = walk_dependencies(q=execution_queue, key=model_id)

    return execution_queue[::-1]

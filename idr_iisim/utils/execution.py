__package__ = "utils"

from idr_iisim.utils.models_dict import models_dict


def walk_dependencies(q: list[str], key: str):
    deps = models_dict.dependencies
    if not key in deps:
        return q

    for i in deps[key]:
        q.append(i)
        return walk_dependencies(q, i)


def generate_execution_queue2(model_id: str) -> list[str]:
    execution_queue: list[str] = [model_id]

    # walk dependencies recursively
    execution_queue = walk_dependencies(q=execution_queue, key=model_id)

    return execution_queue[::-1]


def generate_execution_queue(
    processes: list[str], dependencies: dict[str, set[str]]
):
    queue: list[str] = []

    # Include processes without dependencies
    for process in processes:
        if process not in dependencies:
            queue.append(process)

    # Add the rest of the processes once their dependencies are fullfilled
    while len(queue) != len(processes):
        for process in dependencies:
            if process not in queue:
                should_include_process = True
                for dependency in dependencies[process]:
                    if dependency not in queue:
                        should_include_process = False
                        break
                if should_include_process:
                    queue.append(process)

    return queue

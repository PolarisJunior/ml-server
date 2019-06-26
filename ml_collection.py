# import importlib

# mapping of func_ids to algorithms
algorithms = {
}

def register_algo(algo_id, algo_class):
    print("Registered:", algo_class)
    global algorithms
    algorithms[algo_id] = algo_class


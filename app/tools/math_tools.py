def add(args: dict) -> int:
    return args["a"] + args["b"]

def subtract(args: dict) -> int:
    return args["a"] - args["b"]

def multiply(args: dict) -> int:
    return args["a"] * args["b"]

TOOLS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
}

import sys, os

from .TestingEngine import TestingEngine

__all__ = ["TestPerformer"]

# Remove test_ prefix and capitalize remaining words
def _decorated_name(name):
    words = name.lower().split("_")
    words.pop(0)
    readable = " ".join(x.capitalize() for x in words)
    return readable


# method MUST NOT have parameters
# Method MUST start with "test_" prefix
# Method MUST BE a boolean return type
def _operate(container: TestingEngine, method, transparency) -> bool:
    output = False
    if transparency:
        output = getattr(container, method)()
    else:
        old_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")
        try:
            # hide on-screen error messages and print() messages
            output = getattr(container, method)()
        except:
            pass
        sys.stdout = old_stdout

    return output == True


class TestPerformer:
    _success = "\033[1;32m[ v ]\033[0m"
    _failure = "\033[1;31m[ x ]\033[0m"

    def perform(self, container: TestingEngine, transparency: bool) -> tuple[int, int]:
        methods_list = [
            method
            for method in dir(container)
            if callable(getattr(container, method)) and method.startswith("test_")
        ]
        # passed: How many tests executed truthy result?
        # total: Total number of test_* methods available with the container
        passed = 0
        total: int = len(methods_list)
        for method in methods_list:
            status = self._failure
            output = _operate(container, method, transparency)
            if output:
                status = self._success
                passed += 1
            print(status, _decorated_name(method))
        return passed, total

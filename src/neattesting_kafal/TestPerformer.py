import sys, os

from .TestingEngine import TestingEngine

__all__ = ["TestPerformer", "_module_name_from_file_name"]


# Remove test_ prefix and capitalize the remaining words
def _decorated_name(name):
    words = name.lower().split("_")
    words.pop(0)
    readable = " ".join(x.capitalize() for x in words)
    return readable


# Method MUST NOT have parameters
# Method MUST start with "test_" prefix
# Method MUST return a boolean value
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


# @todo Convert case file into module name
# Importing: ./cases\nested\logic2\Logic2.py
# convert to: cases.nested.logic2.Logic2
# remove slashes and empty ones
def _module_name_from_file_name(path: str) -> str:
    path = ".".join(list(filter(None, path.replace(".py", "").replace("\\", "/").replace("/", ".").split("."))))
    return path


class TestPerformer():
    _success = "\033[1;32m[ v ]\033[0m"
    _failure = "\033[1;31m[ x ]\033[0m"

    def perform(self, container: TestingEngine, transparency: bool) -> tuple[int, int, str]:
        methods_list = [
            method
            for method in dir(container)
            if callable(getattr(container, method)) and method.startswith("test_")
        ]
        # passed: How many tests executed truthy result?
        # total: Total number of test_* methods available with the container
        passed: int = 0
        total: int = len(methods_list)
        cls = container.__class__
        for method in methods_list:
            status = self._failure
            output = _operate(container, method, transparency)
            if output:
                status = self._success
                passed += 1
            print(f"{status} {_decorated_name(method)}")
        print(f"\033[0;36m====( {passed}/{total} )==== \033[1;33m{cls}\033[0m\r\n")
        return passed, total, cls

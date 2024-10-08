import os
import sys

from .TestPerformer import TestPerformer

__all__ = ["TestIndividual"]


def _module_name_from_file_name(path: str) -> str:
    path = path.replace(".py", "").replace("\\", "/").replace("/", ".")
    return path



class TestIndividual(TestPerformer):
    def individual(self, dot_cases_test_file):
        if os.path.isfile(dot_cases_test_file):
            # @todo Convert case file into module name
            # Importing:  ./cases\nested\logic2\Logic2.py
            # cases.nested.logic2.Logic2

            # eg: cases.nested.logic2.Logic2
            case_module_name = _module_name_from_file_name(dot_cases_test_file)
            # module = __import__(case_file, fromlist=["*"])
            module = __import__(case_module_name, globals(), locals(), [], 0)
            classes = [
                getattr(module, x)
                for x in dir(module)
                if isinstance(getattr(module, x), type)
            ]

            for cls in classes:
                setattr(sys.modules[__name__], cls.__name__, cls)
                processor = getattr(sys.modules[__name__], cls.__name__)()
                if str(processor).startswith("<cases."):
                    transparency = True
                    passed, total = self.perform(processor, transparency)
                    print(f"====( {passed}/{total} )==== in \033[0;33m{processor}\033[0m")

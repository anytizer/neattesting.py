import os
import sys
from importlib import import_module
from .TestPerformer import TestPerformer, _module_name_from_file_name

__all__ = ["TestIndividual"]


class TestIndividual(TestPerformer):
    def perform(self, dot_cases_test_file):
        if os.path.isfile(dot_cases_test_file):
            case_module_name = _module_name_from_file_name(dot_cases_test_file)
            module = import_module(case_module_name)
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
                    passed, total, cls = super().perform(processor, transparency)

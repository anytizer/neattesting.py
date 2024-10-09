import os
import sys
from importlib import import_module
from .TestPerformer import TestPerformer, _module_name_from_file_name

__all__ = ["TestIndividual"]


class TestIndividual(TestPerformer):

    def perform(self, dot_cases_test_file, transparency=True):
        if os.path.isfile(dot_cases_test_file):
            case_module_name = _module_name_from_file_name(dot_cases_test_file)

            module = import_module(case_module_name)
            classes = [
                getattr(module, x)
                for x in dir(module)
                if isinstance(getattr(module, x), type)
            ]

            for cls0 in classes:
                setattr(sys.modules[__name__], cls0.__name__, cls0)
                processor = getattr(sys.modules[__name__], cls0.__name__)()
                if str(processor).startswith("<cases."):
                    passed, total, cls = super().perform(processor, transparency)

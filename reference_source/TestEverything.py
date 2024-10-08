import os
import sys
from glob import glob
from importlib import import_module

from .TestPerformer import TestPerformer, _module_name_from_file_name

__all__ = ["TestEverything"]

class TestEverything(TestPerformer):

    def perform(self, cases_dir="cases/"):
        if os.path.basename(cases_dir) == "cases":
            # @todo use case_dir

            for py in glob("./cases/*.py") + glob("./cases/*/*.py"):  # *.py, */*.py
                if os.path.basename(py) not in [".", "..", "__init__.py"]:
                    module = import_module(_module_name_from_file_name(py))
                    classes = [
                        getattr(module, x)
                        for x in dir(module)
                        if isinstance(getattr(module, x), type)  # and "cases." in x
                    ]

                    for cls in classes:
                        setattr(sys.modules[__name__], cls.__name__, cls)
                        processor = getattr(sys.modules[__name__], cls.__name__)()
                        if str(processor).startswith("<cases."):
                            transparency = True
                            passed, total, cls = super().perform(processor, transparency)
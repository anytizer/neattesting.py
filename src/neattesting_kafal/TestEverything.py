import os
import sys
from glob import glob
from importlib import import_module

from .TestPerformer import TestPerformer, _module_name_from_file_name

__all__ = ["TestEverything"]

class TestEverything(TestPerformer):

    def perform(self, cases_dir="./cases/", transparency=True):
        if os.path.basename(cases_dir) == "cases":

            # @todo implement the case_dir
            # @todo ensure that case_dir is a relative path
            for py in glob("./cases/*.py") + glob("./cases/*/*.py"):  # *.py, */*.py
                if os.path.basename(py) not in [".", "..", "__init__.py"]:
                    module = import_module(_module_name_from_file_name(py))
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

import os
import sys
from glob import glob

from .TestPerformer import TestPerformer

__all__ = ["TestEverything"]

class TestEverything(TestPerformer):

    def everything(self, cases_dir="cases/"):
        if os.path.basename(cases_dir) == "cases":
            # @todo use case_dir

            for py in glob("./cases/*.py") + glob("./cases/*/*.py"):  # *.py, */*.py
                if os.path.basename(py) not in [".", "..", "__init__.py"]:

                    py = py.replace(".py", "").replace("\\", "/").replace("/", ".")

                    module = __import__(py, fromlist=["*"])
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
                            passed, total = self.perform(processor, transparency)
                            print(
                                f"====( {passed}/{total} )==== in \033[0;33m{processor}\033[0m"
                            )

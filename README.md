# neattesting.py
This repository will host public repository of **neattesting** tool.
For now, it is the documentation for this.

## Usage example 1

```
from neattesting import TestPerformer

from cases import BusinessLogicTests

if __name__ == "__main__":
    tp = TestPerformer()

    tp.perform(BusinessLogicTests(), True)
```

In this example, `businessLogcTests` is a test suite which contains test_* methods.

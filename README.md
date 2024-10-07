# neattesting.py
This repository will host public repository of **neattesting** tool in order to accept contributions.
For now, it is the documentation for this.

## Considetaions

* All test cases need to return boolean flag to mention if the logic passed successfully.
* It loads entire test suites.
* Decision making methods must return a boolean (True or False) values.
* This is not the unit test mechanism.

## Usage example 1

```
from neattesting import TestPerformer

from cases import BusinessLogicTests

if __name__ == "__main__":
    tp = TestPerformer()

    tp.perform(BusinessLogicTests(), True)
```

In this example, `BusinessLogcTests` is a test suite which contains test_* methods, each returning boolean flags.
One example of `BusinessLogcTests` is `MathematicalTests` below as:

```
from business import BusinessLogic

class MathematicalTests(BusinessLogic):

    def test_summation(self) -> bool:
        a: int = 1
        b: int = 2
        expected_sum: int = 3
        actual_sum = a + b
        return expected_sum == actual_sum
```

The method should return a boolean decision. Perform the tests like:
```
from neattesting import TestPerformer
from cases import MathematicalTests

testhost = MathematicalTests()
transparency = True

tp = TestPerformer()
tp.perform(testhost, transparency)
```
The test engine will look for test_* methods, and perform the call.
Expected output is something simlar to:

```
[ v ] Summation
```

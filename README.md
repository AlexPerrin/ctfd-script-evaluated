# CTFd Custom Python Evaluator Template

CTFd requires an enterprise liscence to use the built-in python evaluator.
So for the QCTF 2022 competition, I wrote plugin a instead.

## Install

Clone this repository into the CTFd/plugins folder.

Modify the following classmethod with your own evaluator, such as casting to other types, applying crpytography, etc.

```python
@classmethod
def evaluatorScript(cls, submission):
  evaluated = submission
  return evaluated
```

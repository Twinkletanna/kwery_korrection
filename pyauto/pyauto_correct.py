"""
Refer: https://github.com/PandaWhoCodes/pyautocorrect and https://github.com/phatpiglet/autocorrect/ and https://pypi.org/project/autocorrect/
Works in mappy2 env but might have to shift this to py3.
WHat about Unicode?
"""

import pyautocorrect
print(pyautocorrect.correct("this is a simple taste to see if this works peiperly"))
print(pyautocorrect.correct("Spellin is difficult, whch is wyh you need to study everyday."))

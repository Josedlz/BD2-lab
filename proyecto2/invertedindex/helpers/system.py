import sys
from typing import Optional, Set

def getSize(obj, seen: Optional[Set[int]] = None) -> int:
  """Recursively finds size of objects. Needs: import sys """
  seen = set() if seen is None else seen

  if id(obj) in seen: return 0  # to handle self-referential objects
  seen.add(id(obj))

  size = sys.getsizeof(obj, 0) # pypy3 always returns default (necessary)
  if isinstance(obj, dict):
    size += sum(getSize(v, seen) + getSize(k, seen) for k, v in obj.items())
  elif hasattr(obj, '__dict__'):
    size += getSize(obj.__dict__, seen)
  elif hasattr(obj, '__slots__'): # in case slots are in use
    slotList = [getattr(C, "__slots__", []) for C in obj.__class__.__mro__]
    slotList = [[slot] if isinstance(slot, str) else slot for slot in slotList]
    size += sum(getSize(getattr(obj, a, None), seen) for slot in slotList for a in slot)
  elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
    size += sum(getSize(i, seen) for i in obj)
  return size
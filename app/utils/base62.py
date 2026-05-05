import string

CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits

def encode(count: int) -> str:
  if count == 0:
    return CHARS[0]
  
  result = ""
  while count > 0:
    count, rem = divmod(count, 62)
    result = CHARS[rem] + result
  
  return result

import re

name = "Apple__123"

name = name.replace(re.findall(r"__.*", name)[0], "")

print(name)
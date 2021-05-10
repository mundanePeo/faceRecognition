import requests
import json

# API地址
create_url = "http://0.0.0.0:10091/createdb"
del_url = "http://0.0.0.0:10091/deltable"

# 删除原始旧库
r = requests.post(del_url)
result = r.content
result = result.decode()
print(result)

# 重新建库
r = requests.post(create_url)
result = r.content
result = result.decode()
print(result)

with open("doc/face_ids.txt", "w") as f:
    f.write("10000000")
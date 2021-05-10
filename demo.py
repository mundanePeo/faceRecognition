import requests
import base64
import os
import json

# API地址
url = "http://0.0.0.0:10091/faceRec"

BASE_DIR = os.getcwd()
# 图片地址
file_path = os.path.join(BASE_DIR, 'static/image/img1.png')

# 二进制打开图片
with open(file_path, 'rb') as f:
    img = base64.b64encode(f.read()).decode()


# 拼接参数
files = {'info_cam': '1_1', 'image': img}
# 发送post请求到服务器端
r = requests.post(url, json=files)
# 获取服务器返回的图片，字节流返回
result = r.content
result = result.decode()
print(result)
# 字节转换成图片
result = json.loads(result)
id, accurarcy = int(result['faceid']), float(result['accurarcy'])
print('{} {}'.format(id, accurarcy))

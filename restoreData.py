from App.settings import BASE_DIR
import requests
import base64
import os
import json

INFOs = [
        [os.path.join(BASE_DIR, 'static/people/10000001/10000001_2.jpg'),
        os.path.join(BASE_DIR, 'static/people/10000001/10000001_1.jpg'),
        os.path.join(BASE_DIR, 'static/people/10000001/10000001_0.jpg')],
        [os.path.join(BASE_DIR, 'static/people/10000002/10000002_1.jpg'),
        os.path.join(BASE_DIR, 'static/people/10000002/10000002_0.jpg'),
        os.path.join(BASE_DIR, 'static/people/10000002/10000002_2.jpg')],
         [os.path.join(BASE_DIR, 'static/people/10000003/10000003_1.jpg'),
         os.path.join(BASE_DIR, 'static/people/10000003/10000003_0.jpg'),
         os.path.join(BASE_DIR, 'static/people/10000003/10000003_2.jpg')],
         [os.path.join(BASE_DIR, 'static/people/10000004/10000004_1.jpg'),
         os.path.join(BASE_DIR, 'static/people/10000004/10000004_0.jpg'),
         os.path.join(BASE_DIR, 'static/people/10000004/10000004_2.jpg')],
         [os.path.join(BASE_DIR, 'static/people/10000005/10000005_1.jpg'),
         os.path.join(BASE_DIR, 'static/people/10000005/10000005_0.jpg'),
         os.path.join(BASE_DIR, 'static/people/10000005/10000005_2.jpg')],
        [os.path.join(BASE_DIR, 'static/people/10000006/10000006_1.jpg'),
         os.path.join(BASE_DIR, 'static/people/10000006/10000006_0.jpg'),
         os.path.join(BASE_DIR, 'static/people/10000006/10000006_2.jpg')],
        [os.path.join(BASE_DIR, 'static/people/10000007/10000007_1.jpg'),
         os.path.join(BASE_DIR, 'static/people/10000007/10000007_0.jpg'),
         os.path.join(BASE_DIR, 'static/people/10000007/10000007_2.jpg')],
        [os.path.join(BASE_DIR, 'static/people/10000008/10000008_1.jpg'),
         os.path.join(BASE_DIR, 'static/people/10000008/10000008_0.jpg'),
         os.path.join(BASE_DIR, 'static/people/10000008/10000008_2.jpg')],
        [os.path.join(BASE_DIR, 'static/people/10000009/10000009_0.jpg'),
         os.path.join(BASE_DIR, 'static/people/10000009/10000009_1.jpg'),
         os.path.join(BASE_DIR, 'static/people/10000009/10000009_2.jpg')],
        ]


# API??????
url = "http://0.0.0.0:10091//faceRecData"

for files in INFOs:
    BASE_DIR = os.getcwd()

    img = []
    for file in files:
        # ?????????????????????
        with open(file, 'rb') as f:
            img.append(base64.b64encode(f.read()).decode())

    # ????????????
    data = {
        "IMAGE1": img[0],
        "IMAGE2": img[1],
        "IMAGE3": img[2]
    }
    # ??????post?????????????????????
    r = requests.post(url, json=data)
    # ????????????????????????????????????????????????
    result = r.content
    result = result.decode()
    print(result)
    # ?????????????????????
    try:
        result = json.loads(result)
        print('faceid: ', result['faceid'])
        print('accurarcy:', result['accurarcy'])
    except Exception as e:
        print(e)


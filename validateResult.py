from requests_toolbelt import MultipartEncoder
from datetime import date, timedelta
from tqdm import tqdm
from config.configLoad import config_data

import requests
import base64
import os
import json
import argparse

BASE_DIR = 'static/people'

people_list = os.listdir(BASE_DIR)

url = 'https://api-cn.faceplusplus.com/facepp/v3/compare'

getDay = None


def getSomeday(day=1):
    today = date.today()
    oneday = timedelta(days=day)
    someday = today-oneday
    return someday


def prepare():
    global getDay
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", type=int, default=1, help="验证指定日期的识别结果，1代表以今天为基准向前一天也即昨天")
    args = parser.parse_args()
    d = args.date
    getDay = getSomeday(d)
    test_pair = os.path.join('static', f'{getDay}_resultRecord.txt')
    return test_pair


def getData(file_path):
    if not os.path.exists(file_path) or not (isinstance(file_path, str) and file_path.endswith('.txt')):
        raise FileExistsError
    with open(file_path, 'r') as f:
        test_data = f.readlines()
    return test_data


def validation(test_data: list):
    if len(people_list) == 0:
        raise FileNotFoundError
    count = 0.
    far = 0.
    frr = 0.
    sum = len(test_data)
    runningLog = []
    runningLog.append(str(getDay))
    runningLog.append("\n")
    print("————————————————————validation start!————————————————————")
    for i in tqdm(range(len(test_data))):
        file1, _ = test_data[i].split(' ')
        # print("now : ", file1)
        runningLog.append(file1)
        runningLog.append("\t")
        _ = _.strip('\n')
        respeo = 0
        end = 0.
        with open(file1, 'rb') as f:
            img1 = base64.b64encode(f.read()).decode()
        for j in range(len(people_list)):
            peo = people_list[j]
            peo_dir = os.path.join(BASE_DIR, peo)
            img_list = os.listdir(peo_dir)
            index = 0
            while True:
                file2 = os.path.join(peo_dir, img_list[index])
                # print("validate image ", file2)
                with open(file2, 'rb') as f:
                    img2 = base64.b64encode(f.read()).decode()
                params = MultipartEncoder(fields={'api_key': config_data['validate']['api_key'],
                        'api_secret': config_data['validate']['api_secret'],
                        'image_base64_1': img1,
                        'image_base64_2': img2
                        },)

                r = requests.post(url, data=params, headers={'Content-Type': params.content_type})
                result = r.content
                result = result.decode()
                result = dict(json.loads(result))
                # print(result)
                if 'error_message' not in result.keys():
                    if 'confidence' not in result.keys() or 'thresholds' not in result.keys():
                        break
                    confidence = result['confidence']
                    thresh = result['thresholds']
                    if confidence <= thresh['1e-3']:
                        output = 0
                    elif confidence >= thresh['1e-5']:
                        output = 1
                    else:
                        output = 1
                    if output == 1:
                        respeo = int(peo)
                        break
                    index += 1
                else:
                    if str(result['error_message']) not in runningLog:
                        runningLog.append(str(result['error_message']))
                        runningLog.append("\t")
                        break
                    index += 1
                if index == 3:
                    end = j
                    break
            if respeo != 0:
                break
            elif end == len(people_list)-1 and index == 3:
                respeo = -3
            elif end < len(people_list)-1 and index < 3:
                respeo = -2
                break
        # print("final id is ", respeo)
        # print("initial id is ", _)
        runningLog.append(f"final:{respeo}\t")
        runningLog.append(f"initial:{_}\n")
        with open('runningLog.txt', 'a+') as f:
            f.writelines(runningLog)
        runningLog.clear()

        if respeo == int(_):
            count += 1
        elif respeo == -3 or ((10000001<=respeo<=10000009) and respeo != int(_)):
            far += 1
        else:
            sum -= 1

    with open('validateResult.txt', 'a+') as f:
        line = [str(getDay), '\t',  f'precision: {count/sum}\t', f'far: {far}\t', f'frrProb: {far/sum}\n']
        f.writelines(line)
    print("————————————————————validation   end!————————————————————")


if __name__ == "__main__":
    try:
        file_name = prepare()
        test_data = getData(file_name)
        validation(test_data)
    except FileExistsError as e:
        print("The record of your input day is not exist!")
    except FileNotFoundError as e:
        print("Don't find images in static/people")


from flask_restful import Resource, fields, marshal_with, reqparse
from flask import jsonify
from ..exts import model
from ..exts.instance import fr
from ..settings.fr_config import versionOfFaceDetection,versionOfFaceRecognize, updateOfFaceRecognize
from ..settings import BASE_DIR

import time
import base64
import numpy as np
import cv2
from math import sqrt
import os

# 人脸识别请求参数转换器
parse = reqparse.RequestParser()
# required确认参数是否必须
# help是输入不符合时出现的内容
# 当需要获取同一个字段的一组值时用action="append"
parse.add_argument("info_cam", type=str, location=['json', 'args'], required=False, help="输入参数必须是str")
parse.add_argument("image", type=str, location=['json', 'args'], required=True, help="输入参数必须是str")


# 人脸注册请求参数转换器
parseDet = reqparse.RequestParser()
# parseDet.add_argument("ID", type=str, location=['json', 'args'], required=True, help="输入参数必须是str")
parseDet.add_argument("IMAGE1", type=str, location=['json', 'args'], required=True, help="输入参数必须是str")
parseDet.add_argument("IMAGE2", type=str, location=['json', 'args'], required=True, help="输入参数必须是str")
parseDet.add_argument("IMAGE3", type=str, location=['json', 'args'], required=True, help="输入参数必须是str")


class createdb(Resource):
    def post(self):
        model.create_all()
        return 'create success!'

    def get(self):
        model.create_all()
        return 'create success!'


class deltable(Resource):
    def post(self):
        model.drop_all()
        return 'delete success!'

    def get(self):
        model.drop_all()
        return 'delete success!'


class faceRecData(Resource):
    """
    用于初始人脸建库识别
    """
    def process(self, info_cam, faces):
        if len(faces) != 3:
            return 4, None, None
        index = 0
        api_data = []
        for image in faces:
            # get image from b64code to cv2
            try:
                img = base64.b64decode(image)
                image_data = np.fromstring(img, np.uint8)
                image_data = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
            except Exception as e:
                print("Exception is occur, ", e)
                return 4, None, None

            if image_data is None:
                print("Image format is wrong!")
                return 1, None, None

            if image_data.shape[-1] != 3:
                print("Image format is wrong!")
                return 1, None, None

            # 构造数据格式
            face_path = os.path.join(BASE_DIR, f'doc/register_tmp_{index}.jpg')
            cv2.imwrite(face_path, image_data)

            api_data.append(face_path)
            index += 1

        # 传入数据结构
        fr.input(info_cam, api_data)

        # 运行得到结果
        result = fr.run()
        faceid, accurarcy = str(result[0]), str(result[1])

        return 0, faceid, accurarcy

    def post(self):
        msg = {"0": "ok", "1": "format error", "2": "number error", "3": "content error", "4": "parse error", "5": "Server Error"}
        status = {"0": "200", "1": "400", "2": "401", "3": "402", "4": "300", "5": "500"}
        data = {
            "pose": "None",
            "version": versionOfFaceRecognize,
            "update": updateOfFaceRecognize
        }
        parser = parseDet.parse_args()

        info_cam = '1_1'

        image = parser.get("IMAGE1")
        image2 = parser.get("IMAGE2")
        image3 = parser.get("IMAGE3")

        try:
            stat, face_id, accurarcy = self.process(info_cam, [image, image2, image3])

            data["msg"] = msg[str(stat)]
            data["status"] = status[str(stat)]

            if stat == 0:
                data["faceid"] = face_id
                data["accurarcy"] = accurarcy

            return jsonify(data)
        except Exception as e:
            data['status'] = status["5"]
            data['msg'] = msg["5"]
            print('Register Server Error: ', e)
            return jsonify(data)


class faceRec(Resource):
    def process(self, info_cam, image):
        # get image from b64code to cv2
        img = base64.b64decode(image)
        image_data = np.fromstring(img, np.uint8)
        image_data = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

        pose = "Unknow"

        # 构造数据格式
        image_path = os.path.join(BASE_DIR, 'doc/rec_tmp.jpg')
        cv2.imwrite(image_path, image_data)
        api_data = [image_path]

        # 传入数据结构
        fr.input(info_cam, api_data)
        # 运行得到结果
        result = fr.run()

        faceid, accurarcy = str(result[0]), str(result[1])
        return pose, faceid, accurarcy

    def post(self):
        data = {
            "msg": "ok",
            "status": "200",
            "pose": "None",
        }
        parser = parse.parse_args()
        # info_cam = parser.get("info_cam")
        info_cam = "1_1"
        image = parser.get("image")
        try:
            pose, face_id, accurarcy = self.process(info_cam, image)

            data['pose'] = pose
            data['faceid'] = face_id
            data['accurarcy'] = accurarcy
            return jsonify(data)
        except Exception as e:
            data['status'] = 500
            data['msg'] = 'Server Error'
            print('Recognize Server Error: ', e)
            return jsonify(data)


from ..settings import FILE_FACE_IDS, BASE_DIR
from ..models.Model import get, add
from .face_sdk.api_usage.face_recogntion import Prediction
from .face_sdk.api_usage.concatImageAndTest import faceRec_pipline, inference_on_image
from .utils import saveImage, saveImageForIteration, readFeature, saveFeature

import multiprocessing as mp
import numpy as np
import os
import threading
from time import perf_counter
import cv2
from random import randint
from datetime import date


class Recognizer:
    class worker:
        def __init__(self, lock, logger):
            # self.samples = []
            self.recognize_worker = Prediction.getInstance()
            self.res = {}
            self.__face_ids = []
            self.__features = []
            self.info_data = None
            self.len_of_face = 0
            self.lock = lock
            self.logger = logger
            super(Recognizer.worker, self).__init__()
            with open(FILE_FACE_IDS, 'r') as f:
                len = f.readlines()
                self.len_of_face = int(len[0])

        def input(self, info_data):

            self.info_data = info_data
            results = get(self.info_data[0])
            if results is None:
                self.res = {}
            else:
                for info in results:
                    if info[1] not in self.res.keys():
                        self.res[info[1]] = []
                    if len(self.res[info[1]]) < 3:
                        self.res[info[1]].append(readFeature(info[3]))
                self.logger.info(f'search face result {self.res.keys()}')

                for index in self.res.keys():
                    if index not in self.__face_ids:
                        self.__face_ids.append(index)
                        self.__features.extend(self.res[index])

        def __compare(self, image_path):
            res_id = [0, 0.0, 0.0]
            if self.res.keys():
                image = cv2.imread(image_path)
                ans = faceRec_pipline(image, self.__features, self.recognize_worker)
                result = 0.
                score = 0.
                ids = 0
                seq = 0
                for sim, sc in ans:
                    if sim == -1:
                        seq += 1
                        continue
                    result += sim
                    score = max(score, sc)
                    seq += 1
                    if seq == 3:
                        self.logger.info(f"id:{self.__face_ids[ids]}, acc:{score}")
                        if res_id[1] < score and res_id[2] <= result:
                            res_id[0] = int(self.__face_ids[ids])
                            res_id[1] = score
                            res_id[2] = result
                        ids += 1
                        seq = 0
                        result = 0.
                        score = 0.

            if res_id[1] < 0.71:
                res_id = [-3, 0., 0.]

            return res_id

        def run(self):
            res_id = []
            # 注册选项
            if self.info_data[-1]:
                # 获取人脸ID
                res_id = self.__compare(self.info_data[2])

                if res_id[0] == -3:
                    # 如果未发现该人脸，则原人脸ID自增，考虑到多线程争用，先加锁
                    if self.lock.acquire():
                        self.len_of_face += 1
                        res_id[0] = self.len_of_face
                        with open(FILE_FACE_IDS, 'w') as f:
                            f.writelines(f'{self.len_of_face}\n')
                    self.lock.release()
                    self.logger.info(f"NOT FOUND THE FACE, BUILDING NEW ID {res_id[0]}")
                else:
                    self.logger.info(f"FOUND FACE ID {res_id[0]}")

                for i in range(3):
                    # 获取人脸特征
                    feature0 = inference_on_image(self.info_data[2 + i], self.recognize_worker)
                    # 保存人脸图像和特征
                    save_face_path = saveImage(str(res_id[0]), self.info_data[2+i])
                    save_feat_path = saveFeature(str(res_id[0]), feature0=feature0)
                    if save_feat_path is not None:
                        add([self.info_data[0], self.info_data[1], res_id[0], save_face_path, save_feat_path])
                        self.logger.info("Save success!")
                    else:
                        self.logger.info("Save failed!")

            # 人脸查找选项
            else:
                res_id = self.__compare(self.info_data[2])
                self.logger.info(f"FOUND FACE ID {res_id[0]}")
            return res_id[:-1]

    def __init__(self, logger):
        self.input_data = []
        self.img_path = None
        self.lock = threading.Lock()
        self.logger = logger
        self.workers = Recognizer.worker(self.lock, self.logger)

    def input(self, info_cam, api_data):
        if info_cam and isinstance(info_cam, str):
            area, cam = info_cam.split('_')  # 1_1
        else:
            self.logger.info('info_cam format wrong!')
            raise ValueError('info_cam format wrong!')
        try:
            isRegister = False
            # image, landmark = api_data[0], api_data[1]  # [image, landmark]
            if len(api_data) == 1:
                isRegister = False
                self.input_data = [int(area), int(cam), api_data[0], isRegister]
            elif len(api_data) == 3:
                isRegister = True
                self.input_data = [int(area), int(cam), api_data[0], api_data[1], api_data[2], isRegister]
            else:
                raise Exception("Input data number must be 1 or 3!")
            self.img_path = saveImageForIteration(api_data[0])
            self.logger.info("INPUT DATA: area, cam, face, landmark")
            self.logger.info(f"area:{self.input_data[0]}")
            self.logger.info(f"cam:{self.input_data[1]}")
            self.logger.info(f"face:main")
            self.logger.info(f"Register:{isRegister}")
            self.logger.info(f"Collect face image is {self.img_path}")
        except Exception as e:
            self.logger.info("ERROR:", e)

    def run(self):
        self.logger.info("Recognizer starts!")
        if self.input_data:
            starttime = perf_counter()
            self.workers.input(self.input_data)
            res = self.workers.run()
            self.logger.info("Find face spend time is %f" % (perf_counter() - starttime))
            if res[0] != -3:
                txtname = os.path.join('static', f'{date.today()}_resultRecord.txt')
                with open(txtname, 'a+') as f:
                    record = [f'{self.img_path} ', f'{res[0]}\n']
                    f.writelines(record)
            return res
        else:
            self.logger.info("input is None!")
            return [0, 0.]

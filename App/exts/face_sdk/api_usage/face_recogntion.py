import sys
sys.path.append('.')

from .logFile import logger

import yaml
import cv2
import numpy as np
import torch

from time import perf_counter
from ..core.model_loader.face_detection.FaceDetModelLoader import FaceDetModelLoader
from ..core.model_handler.face_detection.FaceDetModelHandler import FaceDetModelHandler
from ..core.model_loader.face_alignment.FaceAlignModelLoader import FaceAlignModelLoader
from ..core.model_handler.face_alignment.FaceAlignModelHandler import FaceAlignModelHandler
from ..core.image_cropper.arcface_cropper.FaceRecImageCropper import FaceRecImageCropper
from ..core.model_loader.face_recognition.FaceRecModelLoader import FaceRecModelLoader
from ..core.model_handler.face_recognition.FaceRecModelHandler import FaceRecModelHandler

with open('App/exts/face_sdk/config/model_conf.yaml') as f:
    model_conf = yaml.load(f)
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

class Prediction:
    def __init__(self, image=None, feature=None):
        super()
        self.__image = image
        self.__faceDetModelHandler = None
        self.__faceAlignModelHandler = None
        self.__faceRecModelHandler = None
        self.__init_model()
        self.__score = np.array([0., 0., 0.])
        self.__feature = feature

    @staticmethod
    def getInstance(image=None, feature=None):
        instance = Prediction(image, feature)
        return instance

    def __init_model(self):
        # common setting for all models, need not modify.
        model_path = 'App/exts/face_sdk/models'
        faceDetStartTime = perf_counter()
        # face detection model setting.
        scene = 'non-mask'
        model_category = 'face_detection'
        model_name = model_conf[scene][model_category]
        logger.info('Start to load the face detection model...')
        try:
            faceDetModelLoader = FaceDetModelLoader(model_path, model_category, model_name)
            model, cfg = faceDetModelLoader.load_model()
            self.__faceDetModelHandler = FaceDetModelHandler(model, 'cuda:0', cfg)
        except Exception as e:
            logger.error('Falied to load face detection Model.')
            logger.error(e)
            sys.exit(-1)
        else:
            logger.info('Success!')
        faceDetEndTime = perf_counter()

        # face landmark model setting.
        model_category = 'face_alignment'
        model_name = model_conf[scene][model_category]
        logger.info('Start to load the face landmark model...')
        try:
            faceAlignModelLoader = FaceAlignModelLoader(model_path, model_category, model_name)
            model, cfg = faceAlignModelLoader.load_model()
            self.__faceAlignModelHandler = FaceAlignModelHandler(model, 'cuda:0', cfg)
        except Exception as e:
            logger.error('Failed to load face landmark model.')
            logger.error(e)
            sys.exit(-1)
        else:
            logger.info('Success!')
        FaceLMEndTime = perf_counter()

        # face recognition model setting.
        model_category = 'face_recognition'
        model_name = model_conf[scene][model_category]
        logger.info('Start to load the face recognition model...')
        try:
            faceRecModelLoader = FaceRecModelLoader(model_path, model_category, model_name)
            model, cfg = faceRecModelLoader.load_model()
            self.__faceRecModelHandler = FaceRecModelHandler(model, 'cuda:0', cfg)
        except Exception as e:
            logger.error('Failed to load face recognition model.')
            logger.error(e)
            sys.exit(-1)
        else:
            logger.info('Success!')
        FaceRecEndTime = perf_counter()
        print("face detect model load time: ", faceDetEndTime - faceDetStartTime)
        print("face landmark model load time: ", FaceLMEndTime - faceDetEndTime)
        print("face rec model load time: ", FaceRecEndTime - FaceLMEndTime)

    def setImage(self, image):
        self.__image = image

    def setFeature(self, feature):
        self.__feature = np.array(feature).T.astype(np.float32)
        # print(self.__feature.shape)

    def getScore(self):
        return self.__score.tolist()

    def run(self):
        self.__pipeline()

    def inference_on_image(self, image_path):
        image = cv2.imread(image_path)
        face_cropper = FaceRecImageCropper()
        try:
            dets = self.__faceDetModelHandler.inference_on_image(image)
            face_nums = dets.shape[0]
            # if face_nums != 2:
            #     logger.info('Input image should contain two faces to compute similarity!')
            landmarks = self.__faceAlignModelHandler.inference_on_image(image, dets[0])
            landmarks_list = []
            for (x, y) in landmarks.astype(np.int32):
                landmarks_list.extend((x, y))
            cropped_image = face_cropper.crop_image_by_mat(image, landmarks_list)
            feature = self.__faceRecModelHandler.inference_on_image(cropped_image)
        except Exception as e:
            logger.error('Inference failed!')
            logger.error(e)
            return None
            # sys.exit(-1)
        else:
            logger.info('Success!')
            return feature

    def __pipeline(self):
        # read image and get face features.
        # image_path = 'api_usage/test_images/test1.jpg'
        # image = cv2.cvtColor(np.asarray(self.__image), cv2.COLOR_RGB2BGR)
        image = self.__image
        face_cropper = FaceRecImageCropper()
        try:
            dets = self.__faceDetModelHandler.inference_on_image(image)
            face_nums = dets.shape[0]
            # if face_nums != 2:
            #     logger.info('Input image should contain two faces to compute similarity!')
            landmarks = self.__faceAlignModelHandler.inference_on_image(image, dets[0])
            landmarks_list = []
            for (x, y) in landmarks.astype(np.int32):
                landmarks_list.extend((x, y))
            cropped_image = face_cropper.crop_image_by_mat(image, landmarks_list)
            feature = self.__faceRecModelHandler.inference_on_image(cropped_image)
            score = 0.5 + 0.5 * self.__dot(feature, self.__feature)
            # score = 0.5 + 0.5*np.dot(feature, self.__feature)
            self.__score = score
            # logger.info('The similarity score of two faces: %f' % score)
        except Exception as e:
            logger.error('Pipeline failed!')
            logger.error(e)
            self.__score = np.zeros((self.__feature.shape[1]))
            # sys.exit(-1)
        else:
            logger.info('Success!')

    def __dot(self, mat1: np.ndarray, mat2: np.ndarray) -> np.ndarray:
        import time
        starttime = time.perf_counter()
        feature1 = torch.from_numpy(mat1.reshape(1, 512)).to(device)
        feature_mat = torch.from_numpy(mat2).to(device)
        loadtime = time.perf_counter()
        print("load data to gpu time is ", loadtime-starttime)
        comsttime = time.perf_counter()
        with torch.no_grad():
            ans = torch.mm(feature1, feature_mat).cpu().numpy()
        comentime = time.perf_counter()
        print("computer torch tensor time is ", comentime - comsttime)
        return np.squeeze(ans)

    def __pipeline_detached(self):
        # read image and get face features.
        # image_path = 'api_usage/test_images/test1.jpg'
        image = cv2.cvtColor(np.asarray(self.__image), cv2.COLOR_RGB2BGR)
        face_cropper = FaceRecImageCropper()
        try:
            dets = self.__faceDetModelHandler.inference_on_image(image)
            face_nums = dets.shape[0]
            if face_nums != 2:
                logger.info('Input image should contain two faces to compute similarity!')
            feature_list = []
            for i in range(face_nums):
                landmarks = self.__faceAlignModelHandler.inference_on_image(image, dets[i])
                landmarks_list = []
                for (x, y) in landmarks.astype(np.int32):
                    landmarks_list.extend((x, y))
                cropped_image = face_cropper.crop_image_by_mat(image, landmarks_list)
                feature = self.__faceRecModelHandler.inference_on_image(cropped_image)
                feature_list.append(feature)
            score = 0.5 + 0.5*np.dot(feature_list[0], feature_list[1])
            self.__score = score
            logger.info('The similarity score of two faces: %f' % score)
        except Exception as e:
            logger.error('Pipeline failed!')
            logger.error(e)
            self.__score = None
            # sys.exit(-1)
        else:
            logger.info('Success!')
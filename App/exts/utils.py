from ..settings import BASE_DIR, DIR_FEATURE_SAVE

import os
import cv2
import numpy as np


osdir = os.path.join(BASE_DIR, 'static/image')


# 根据本地人脸集数量存储新接收人脸
def saveImage(personId, image_path, nums=None):
    personDir = os.path.join(osdir, personId)
    os.makedirs(personDir, exist_ok=True)
    sizeFeat = len(os.listdir(personDir))
    if sizeFeat >= 3:
        return None

    if nums is None:
        nums = sizeFeat
    image_name = f"{personId}_{nums}.jpg"
    print(os.path.join(personDir, image_name))
    image = cv2.imread(image_path)
    cv2.imwrite(os.path.join(personDir, image_name), image)
    return os.path.join(personDir, image_name)


# 收集人脸数据用作本地迭代
def saveImageForIteration(img_path, nums=None):
    thisOsDir = os.path.join(BASE_DIR, 'static/dataset')
    os.makedirs(thisOsDir, exist_ok=True)
    sizeFeat = len(os.listdir(thisOsDir))
    if nums is None:
        nums = sizeFeat
    image_name = f"imageFace_{nums}.jpg"
    image_path = os.path.join(thisOsDir, image_name)
    print("Collecting face image success")
    image = cv2.imread(img_path)
    cv2.imwrite(image_path, image)
    return image_path


# 存储人脸特征
def saveFeature(id, feature0, num=None):
    personDir = os.path.join(DIR_FEATURE_SAVE, id)
    os.makedirs(personDir, exist_ok=True)
    sizeFeat = len(os.listdir(personDir))
    if sizeFeat >= 3:
        return None

    if num is None:
        num = sizeFeat
    name = '{}_{}_feature.txt'.format(id, num)
    save_path = os.path.join(personDir, name)
    print(os.path.join(personDir, save_path))
    np.savetxt(save_path, feature0, delimiter=',')
    return save_path


# 读入人脸特征
def readFeature(feature_path):
    if not os.path.exists(feature_path):
        print(f"{feature_path} is not exist!")
        return None
    return np.loadtxt(feature_path, delimiter=',')

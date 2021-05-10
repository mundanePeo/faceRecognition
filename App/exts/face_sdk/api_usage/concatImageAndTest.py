
from .face_recogntion import Prediction
from PIL import Image
from time import perf_counter
from os import path
from App.settings.fr_config import thresh

import sys
import os
import cv2


def concate(img1_path, img2_path, flag='horizontal'):
    """
    :param img1_path: The path of the first image
    :param img2_path: The path of the second image
    :param flag: Concate orient: horizontal or vertical
    :return: image
    """
    img1, img2 = Image.open(img1_path), Image.open(img2_path)
    size1, size2 = img1.size, img2.size
    if size1[0]*size1[1] < size2[0]*size2[1]:
        img1 = img1.resize((size2[0], size2[1]), Image.ANTIALIAS)
    else:
        img2 = img2.resize((size1[0], size1[1]), Image.ANTIALIAS)
    size1 = img1.size
    size2 = img2.size
    if flag == 'horizontal':
        joint = Image.new('RGB', (size1[0]+size2[0], size1[1]))
        loc1, loc2 = (0, 0), (size1[0], 0)
        joint.paste(img1, loc1)
        joint.paste(img2, loc2)
        # joint.save("./api_usage/test_images/concate.jpg")
        return joint
        # joint.show("horizontal")

    elif flag == 'vertical':
        joint = Image.new('RGB', (size1[0], size1[1]+size2[1]))
        loc1, loc2 = (0, 0), (0, size1[1])
        joint.paste(img1, loc1)
        joint.paste(img2, loc2)
        # joint.save("./api_usage/test_images/concate.jpg")
        return joint
        # return "./api_usage/test_images/concate.jpg"
        # joint.show("vertical")
    else:
        print("no this option, please choose horizontal or vertical and try again")


def faceRec_pipline(img1, img2, prediction, name=None):
    # try:
    #     if not path.exists(img1) or img2 is None:
    #         return -1, None
    #     if not img1.endswith('jpg'):
    #         return -1, None
    # except Exception as e:
    #     print(e)
    #     return -1, None
    if img1 is None or img2 is None:
        return -1, None
    # img = concate(img1, img2)
    prediction.setImage(img1)
    prediction.setFeature(img2)
    prediction.run()
    return filterRes(prediction.getScore())


def inference_on_image(image_path, prediction):
    if path.exists(image_path) is None or prediction is None:
        return None
    return prediction.inference_on_image(image_path)


def filterRes(scores: list, threshold: float=thresh):
    ans = []
    for score in scores:
        if score is None or score < 0:
            ans.append([-1, None])
        else:
            if score > 1:
                score = 1.
            if score >= threshold:
                ans.append([1, score])
            else:
                ans.append([0, score])
    return ans


def test(img1, img2, prediction, name=None):
    # starttime = perf_counter()
    img = concate(img1, img2)
    # concatetime = perf_counter()
    # small:Concate two images spend time is  0.013338482938706875
    #   big:Concate two images spend time is  0.03890702594071627
    # print("", name, ": Concate two images spend time is ", concatetime - starttime)

    prediction.setImage(img)
    # small: acc 0.65
    #   big: acc 0.68
    prediction.run()
    # small:Face Recognize spend time is 6.613808409310877
    #   big:Face Recognize spend time is 7.027754046022892
    # print("", name, ": Face Recognize spend time is ", perf_counter() - concatetime)
    # small:Spending whole time is  6.627187718637288
    #   big:Spending whole time is  7.066712011583149
    # print("", name, ": Spending whole time is ", perf_counter() - starttime,"\n")
    return prediction.getScore()


def evaluation(data_dir, data_list):
    try:
        prediction = Prediction()
        maxacc = 0.
        maxthresh = 0.5
        scores = []
        with open(data_list) as f:
            image_pair_list = f.readlines()
        count = 0

        for pair in image_pair_list:
            img1_name, img2_name, ans = pair.split()
            print(img1_name, " ", img2_name)
            img1_path, img2_path = path.join(data_dir, img1_name), path.join(data_dir, img2_name)
            score = test(img1_path, img2_path, prediction)
            if score is None:
                continue
            scores.append((int(ans), score))
            count += 1

        thresh = 0.5
        while True:
            acc = 0.
            for score in scores:
                if score[1] >= thresh and score[0] or score[1] < thresh and not score[0]:
                    acc += 1.
            print("The test dataset's acc is ", acc / count, "\n")
            print("The test dataset's thresh is ", thresh, "\n")
            if maxacc < acc/count:
                maxacc = acc/count
                maxthresh = thresh
            thresh += 0.01
            if thresh >= 0.80:
                break
        # 注意人脸图像的大小不能太小，最好在112*112左右
        print("The test dataset's maxacc is ", maxacc, "\n")
        print("The test dataset's maxthresh is ", maxthresh, "\n")
        print("image's count is ", count)
    except EOFError as e:
        print("file route error or pair list error")


if __name__ == '__main__':
    # prediction = Prediction()
    # img1 = './api_usage/test_images/imageFace_147.jpg'
    # img2 = './api_usage/test_images/imageFace_173.jpg'
    # test(img1, img2, prediction, "img1")
    #
    # img3 = './api_usage/test_images/imageFace_20.jpg'
    # img4 = './api_usage/test_images/imageFace_19.jpg'
    # test(img3, img4, prediction, "img2")
    #
    # img5 = './api_usage/test_images/imageFace_131.jpg'
    # img6 = './api_usage/test_images/imageFace_130.jpg'
    # test(img5, img6, prediction, "img3")
    evaluation("./data/myself", "./data/myself_test_pair.txt")

import os
import torch

from App.settings import BASE_DIR

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')  # sets device for model and PyTorch tensors

# jdai
thresh = 0.7000

# Version information
# 修复了多次请求会导致同一个人的识别能力下降问题
# 修复了摄像头编号变更导致的问题
# 更新了人脸识别模型和框架，使用Pipline优化了识别流程，使用了SST训练法, jdai
# 更新了人脸识别过程，优化比对方式，重构识别架构，提升比对速度
# 优化识别算子(采用矩阵运算和GPU加速)，提升识别速度(稳定80ms以内)，解决了服务报错时返回异常的问题
versionOfFaceRecognize = 'v2.2'

# Update time
updateOfFaceRecognize = '2021.04.07'  # v2.2

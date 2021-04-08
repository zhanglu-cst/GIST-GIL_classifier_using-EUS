
from PIL import Image
from torchvision.transforms import transforms
import json
from set_logger import get_logger
import socket
import time


import torch
from model import Deep_Net
import os

logger = get_logger()

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    model_path = config['model_path']
    image_dir = config['image_dir']
except Exception as e:
    logger.info(str(e))
    logger.info('using the default setting.')
    model_path = 'model'
    image_dir = 'C:/imageX'

if (os.path.exists(image_dir) == False):
    os.makedirs(image_dir)

device = torch.device('cpu')

model = Deep_Net(load_pretrain_for_train = False)

if (os.path.exists(model_path)):
    model.load_state_dict(torch.load(model_path, map_location = device))
    logger.info('load model:{}'.format(model_path))
else:
    logger.error('can not find model')
    raise Exception('can not find model')

model.eval()

normalize_mean = 55
normalize_std = 40
transform = transforms.Compose([
    transforms.Resize((500,500)),
    transforms.ToTensor(),
    transforms.Normalize([normalize_mean], [normalize_std]),
])

# all_imgs = []
# for i in range(1,4):
#     img = Image.open('{}.jpg'.format(i))
#     img = transform(img)
#     all_imgs.append(img)
# all_imgs = torch.stack(all_imgs,dim=0)
# print(all_imgs.shape)
#
# result = model(all_imgs)
# print(result)


top_socket = socket.socket()  # 创建 socket 对象
ip = '127.0.0.1'  # 获取本地主机名
port = 10853  # 设置端口
buffer_size = 1024

top_socket.bind((ip, port))  # 绑定端口
top_socket.listen(5)  # 等待客户端连接并设置最大连接数


def send_string(client, s = 'success'):
    client.send(s.encode())
    receive_ACK = client.recv(1024).decode()
    if (receive_ACK == 'ACK'):
        return True
    else:
        return False


def receive_string(client):
    receive_string = client.recv(1024).decode()
    client.send('ACK'.encode())
    return receive_string


def get_classify_result():
    all_images_filenames = os.listdir(image_dir)
    all_imgs = []
    for filename in all_images_filenames:
        path = os.path.join(image_dir, filename)
        img = Image.open(path).convert('RGB')
        img = transform(img)
        print(img.shape)
        all_imgs.append(img)
    all_imgs = torch.stack(all_imgs, dim = 0)
    result = model(all_imgs)
    result = result.squeeze()
    result = result.tolist()
    print(result)
    if(isinstance(result,float)):
        result = [result]
    for i, item in enumerate(result):
        result[i] = str(item)
    result = ','.join(result)

    for filename in all_images_filenames:
        path = os.path.join(image_dir, filename)
        os.remove(path)

    all_images_filenames = ','.join(all_images_filenames)
    return result, all_images_filenames

    # del the images


while True:
    logger.info('waiting for task...')
    cur_client, addr = top_socket.accept()  # 建立客户端连接。
    logger.info('client connected, addr:{}, time:{}'.format(addr, time.ctime()))
    notify = receive_string(cur_client)
    logger.info('notify:{}'.format(notify))
    if (notify == 'helloworld'):
        logger.info('notify correct OK')

        result, filename_order = get_classify_result()

        send_string(cur_client, result)
        send_string(cur_client, filename_order)
    else:
        logger.info('error notify:{}'.format(notify))

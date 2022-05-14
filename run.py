import argparse

import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image
import os

# parser = argparse.ArgumentParser(description='SRCNN run parameters')
# parser.add_argument('--model', type=str, required=True)
# parser.add_argument('--image', type=str, required=True)
# parser.add_argument('--zoom_factor', type=int, required=True)
# parser.add_argument('--cuda', action='store_true')
# args = parser.parse_args()

def run_scale(zoom_amt, img_path, out_path):
    if zoom_amt == 2:
        model_path = f"{os.getcwd()}/models/model_2x.pth"
    elif zoom_amt == 3:
        model_path = f"{os.getcwd()}/models/model_3x.pth"
    elif zoom_amt == 4:
        model_path = f"{os.getcwd()}/models/model_4x.pth"
    else:
        raise Error("Invalid zoom")


    img = Image.open(img_path).convert('YCbCr')
    img = img.resize((int(img.size[0]*zoom_amt), int(img.size[1]*zoom_amt)), Image.BICUBIC)  # first, we upscale the image via bicubic interpolation
    y, cb, cr = img.split()

    img_to_tensor = transforms.ToTensor()
    input = img_to_tensor(y).view(1, -1, y.size[1], y.size[0])  # we only work with the "Y" channel

    device = torch.device("cuda:0" if (torch.cuda.is_available()) else "cpu")
    # print(device)
    model = torch.load(model_path).to(device)
    input = input.to(device)

    out = model(input)
    out = out.cpu()
    out_img_y = out[0].detach().numpy()
    out_img_y *= 255.0
    out_img_y = out_img_y.clip(0, 255)
    out_img_y = Image.fromarray(np.uint8(out_img_y[0]), mode='L')

    out_img = Image.merge('YCbCr', [out_img_y, cb, cr]).convert('RGB')  # we merge the output of our network with the upscaled Cb and Cr from before
                                                                        # before converting the result in RGB
    out_img.save(out_path)

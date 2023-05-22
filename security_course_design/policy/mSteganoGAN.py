from steganogan import SteganoGAN
import imageio
import os
import torch
from PIL import Image
from imageio import imread, imwrite
from torch.nn.functional import binary_cross_entropy_with_logits, mse_loss
from torch.optim import Adam


def my_steganogan_encode(steganogan, cover, text):
    """Encode an image.
    Args:
        cover (str): Path to the image to be used as cover.
        text (str): Message to hide inside the image.
    """
    cover = imread(cover, pilmode='RGB') / 127.5 - 1.0
    cover = torch.FloatTensor(cover).permute(2, 1, 0).unsqueeze(0)

    cover_size = cover.size()
    # _, _, height, width = cover.size()
    payload = steganogan._make_payload(cover_size[3], cover_size[2], steganogan.data_depth, text)

    cover = cover.to(steganogan.device)
    payload = payload.to(steganogan.device)
    generated = steganogan.encoder(cover, payload)[0].clamp(-1.0, 1.0)

    generated = (generated.permute(2, 1, 0).detach().cpu().numpy() + 1.0) * 127.5
    return generated.astype('uint8')


if __name__ == '__main__':
    steganoGAN = SteganoGAN.load(architecture='dense')
    input_file = "../sources/test.png"
    output_file = "../sources/test_out.png"
    text = input()
    output_image = my_steganogan_encode(steganoGAN, input_file, text)

    print(steganoGAN.decode_image(output_image))
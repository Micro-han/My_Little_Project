from PIL import Image, ImageDraw, ImageFont
import numpy as np
from matplotlib import pyplot as plt


def draw_water_img(img_size, img_mode, secret_text):
    new_img = Image.new(img_mode, img_size, "white")
    draw_img = ImageDraw.Draw(new_img)
    font_size = 14
    message_size = len(secret_text)
    x_per_step = img_size[0] // font_size
    y_per_step = img_size[1] // font_size

    cnt = 0
    for i in range(x_per_step):
        for j in range(y_per_step):
            draw_img.text((i * font_size, j * font_size), secret_text[cnt % message_size]) # , font=ImageFont.truetype("msyh.ttc", font_size), fill="black")
            cnt += 1

    return new_img


def make_bit_0(img):
    img_list = list(img.getdata())
    new_img_list = [(r >> 1 << 1, g >> 1 << 1, b >> 1 << 1) for [r, g, b] in img_list]
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_img_list)
    return new_img


def set_msg_img(lsb0_img, water_img):
    lsb_0_enum = enumerate(list(lsb0_img.getdata()))
    water_mark_list = list(water_img.getdata())

    result = [(r, g, b) if (water_mark_list[index] < (255, 255, 255)) else (r | 1, g | 1, b | 1) for index, (r, g, b) in
              lsb_0_enum]
    new_result = Image.new(lsb0_img.mode, lsb0_img.size)
    new_result.putdata(result)
    return new_result


def encode_img(img, secret_text):
    water_img = draw_water_img(img.size, img.mode, secret_text)

    lsb0_img = make_bit_0(img)

    out_img = set_msg_img(lsb0_img, water_img)

    return out_img


def decode_img(img):
    img_enum = enumerate(list(img.getdata()))
    decode_img_list = [(0, 0, 0) if (r & 1 == 0 and g & 1 == 0 and b & 1 == 0) else (255, 255, 255) for index, [r, g, b]
                       in img_enum]
    out_img = Image.new(img.mode, img.size)
    out_img.putdata(decode_img_list)
    return out_img


if __name__ == '__main__':
    secret_text = input()
    img = Image.open("../sources/test.png").convert("RGB")
    img = img.resize((512, 512))
    lsb_img = encode_img(img, secret_text)
    lsb_img.save('encode.png')

    lsb2_img = Image.open("../policy/encode.png").convert("RGB")
    decode_one = decode_img(lsb2_img)
    decode_one.save('decode.png')
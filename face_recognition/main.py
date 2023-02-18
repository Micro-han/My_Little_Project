import os

import cv2 as cv
import numpy as np


def read_img(path):
    img = cv.imread(path)
    # cv.imshow('face', img)
    # cv.waitKey(0)
    return img


def convert_grey(img):
    grey_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # cv.imwrite('grey_img.png', grey_img)
    return grey_img


def change_size(img, height=200, width=200):
    resize_img = cv.resize(img, dsize=(height, width))
    # print(img.shape)
    # print(resize_img.shape)
    return resize_img


# def draw_rectangle(img, x, y, w, h):
    # rectangle
    # cv.rectangle(img, (x, y, x + w, y + h), color=(0, 0, 255), thickness=1)
    # circle
    # cv.circle(img, center=(x+w, y+h), radius=100, color=(255, 0, 0), thickness=1)
    # cv.imshow('1', img)
    # cv.waitKey(0)


def face_detect_cv2(img):
    grey_img = convert_grey(img)
    face_detector = cv.CascadeClassifier('D:\Softwares\Anaconda\envs\mlearning\Lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml')
    face = face_detector.detectMultiScale(grey_img, 1.08, 5, 0)
    for x, y, w, h in face:
        cv.rectangle(img, (x,y), (x+w, y+h), color=(0,0,255), thickness=2)
        print(x, y, w, h)
    cv.imshow('result', img)
    # cv.waitKey(0)


def video_face_detect_cv2():
    cap = cv.VideoCapture('video1.mp4')
    while True:
        flag, frame = cap.read()
        if flag is False:
            break
        face_detect_cv2(frame)
        if ord('q') == cv.waitKey(0):
            break


def pic_save():
    cap = cv.VideoCapture(0)
    flag = 1
    num = 1
    name = "yxh"
    while cap.isOpened():
        ret_flag, frame = cap.read()
        cv.imshow('Capture_Test', frame)
        k = cv.waitKey(1) & 0xFF
        if k == ord('s'):
            print('./data' + '/' + str(num) + '_' + name + '.jpg')
            cv.imwrite('./data' + '/' + str(num) + '_' + name + '.jpg', frame)
            num += 1
        elif k == ord(' '):
            break


def get_image_and_save_label(path):
    face_samples, ids, image_paths = [], [], [os.path.join(path, f) for f in os.listdir(path)]
    face_detector = cv.CascadeClassifier('D:\Softwares\Anaconda\envs\mlearning\Lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml')
    # 这边逻辑有点问题，对于存储照片的人应该是 num_name_id.jpg
    # 但是我这边仅仅做了单张人脸，即 num_name.jpg
    # 实际上所有的 标签id都应该对应name 而不是对应前面的num 前面的num表示 名字为name标签为id的人的第num张照片数据
    for image_path in image_paths:
        tmp_img = read_img(image_path)
        tmp_img = convert_grey(tmp_img)
        tmp_img_np = np.array(tmp_img, 'uint8')
        faces = face_detector.detectMultiScale(tmp_img_np)
        id_num = 0
        for i in image_path:
            if ord('0') <= ord(i) <= ord('9'):
              id_num = id_num * 10 + ord(i) - ord('0')
        for x, y, w, h in faces:
            ids.append(1)
            # ids.append(id_num)
            face_samples.append(tmp_img_np[y: y + h, x: x + w])
    print('id:', ids)
    # print('fs:', face_samples)
    return face_samples, ids


def train():
    faces, ids = get_image_and_save_label("./data/")
    recognizer = cv.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(ids))
    recognizer.write('./train/trainer.yml')


def face_detect_demo(img_path):
    img = read_img(img_path)
    gray = convert_grey(img)
    face_detector = cv.CascadeClassifier('D:\Softwares\Anaconda\envs\mlearning\Lib\site-packages\cv2\data\haarcascade_frontalface_alt2.xml')
    face = face_detector.detectMultiScale(gray, 1.1, 5, cv.CASCADE_SCALE_IMAGE, (100, 100), (300, 300))
    names = ["yxh"]
    recognizer = cv.face.LBPHFaceRecognizer_create()
    recognizer.read('./train/trainer.yml')
    for x, y, w, h in face:
        cv.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=2)
        cv.circle(img, center=(x + w // 2, y + h // 2), radius=w // 2, color=(0, 255, 0), thickness=1)
        ids, confidence = recognizer.predict(gray[y: y + h, x: x + w])
        if confidence > 80:
            cv.putText(img, 'unKown', (x + 10, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
        else:
            print(ids)
            cv.putText(img,  names[ids - 1], (x + 10, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
    cv.imshow('result', img)
    cv.waitKey(0)


if __name__ == '__main__':
    # img = read_img('face1.png')
    # grey_img = convert_grey(img)
    # resize_img = change_size(img)
    # draw_rectangle(img, 100, 100, 100, 100)
    # face_detect_cv2(img)
    # video_face_detect_cv2()
    # pic_save()
    train()
    face_detect_demo('face1.png')

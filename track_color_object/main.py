from __future__ import division
import cv2
import numpy as np

if __name__ == '__main__':
    cap = cv2.VideoCapture('IMG_2123.mp4')
    height, width = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    black_img = np.random.randint(0, 1, size=(height, width, 3), dtype=np.uint8)

    color = (0, 204, 0, 255, 255, 255)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    frame_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_count = 0

    img = np.random.randint(0, 1, size=(360, 640, 3), dtype=np.uint8)  # Создаем черную картинку
    while frame_length > frame_count:
        frame_count += 1
        lowHue, lowSat, lowVal, highHue, highSat, highVal = color

        _, frame = cap.read()

        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frameHSV, np.array([lowHue, lowSat, lowVal]), np.array([highHue, highSat, highVal]))
        cv2.imshow('Mask', mask)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
        contour = max(contour_sizes, key=lambda x: x[0])[1]

        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)

        cv2.circle(black_img, (x, y), radius=3, color=(0, 0, 255), thickness=-1)

        cv2.imshow('Video', frame)
        cv2.imshow('Traectory', black_img)
        k = cv2.waitKey(50)
        # if k == 27:  # Esc key to stop
        #     break

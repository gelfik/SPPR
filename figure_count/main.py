import numpy as np
import cv2

def get_data(contours):
    arguments = {}
    arguments.update(triangle={"approx": 0, "count": 0, "name": "Треугольник"})
    arguments.update(square={"approx": 0, "count": 0, "name": "Квадрат"})
    arguments.update(rectangle={"approx": 0, "count": -1, "name": "Прямоугольник"})
    arguments.update(diamonds={"approx": 0, "count": 0, "name": "Ромб"})
    arguments.update(circle={"approx": 0, "count": 0, "name": "Круг"})
    arguments.update(oval={"approx": 0, "count": 0, "name": "Овал"})

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        x,y = approx.ravel()[0], approx.ravel()[1] - 5
        x1, y1, w, h = cv2.boundingRect(approx)
        aspect_ratio = float(w) / float(h)
        if len(approx) == 3:
            # cv2.putText(img, "triangle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
            arguments.update(triangle={"approx": len(approx), "count": int(arguments['triangle']['count']) + 1,
                                       "name": "Треугольник"})
        elif len(approx) == 4:
            if aspect_ratio >= 0.95 and aspect_ratio <= 1.05:
                # cv2.putText(img, "square", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                arguments.update(
                    square={"approx": len(approx), "count": int(arguments['square']['count']) + 1, "name": "Квадрат"})
            elif aspect_ratio >= 1.20:
                # cv2.putText(img, "diamonds", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                arguments.update(diamonds={"approx": 0, "count": int(arguments['diamonds']['count']) + 1, "name": "Ромб"})
            else:
                # cv2.putText(img, "rectangle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                arguments.update(rectangle={"approx": len(approx), "count": int(arguments['rectangle']['count']) + 1,
                                            "name": "Прямоугольник"})
        else:
            if aspect_ratio >= 0.95 and aspect_ratio <= 1.05:
                # cv2.putText(img, "circle", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
                arguments.update(
                    circle={"approx": len(approx), "count": int(arguments['circle']['count']) + 1, "name": "Круг"})
            else:
                # cv2.putText(img, "oval", (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
                arguments.update(
                    oval={"approx": len(approx), "count": int(arguments['oval']['count']) + 1, "name": "Овал"})

        box = np.int0(cnt)
        cv2.drawContours(img, [box], 0, (255, 0, 0), 2)
    return arguments

if __name__ == '__main__':
    img = cv2.imread('my_fig.png')
    gray_main_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray_main_image, (5, 5), 0)
    T, thresh_img = cv2.threshold(blurred, 215, 255, cv2.THRESH_BINARY)
    contours0, hierarchy = cv2.findContours(thresh_img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    height, width = img.shape[:2]
    x, y = width - 200, height - 125
    arguments = get_data(contours0)
    for i, item in enumerate(arguments):
        cv2.putText(img, f"{item}: {arguments[item]['count']}", (x, y+i*20), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 255), 1)

    cv2.imshow('contours', img)
    cv2.waitKey()
    cv2.destroyAllWindows()

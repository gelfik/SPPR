import cv2


def find_counters(img):
    img = cv2.medianBlur(img, 5)
    ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    return cv2.findContours(th1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


def find_coordinate(counters, image):
    coordinate_list = []
    for i in range(0, len(counters)):
        x, y, w, h = cv2.boundingRect(counters[i])
        if w > 30 and h > 40:
            new_img = get_img(counters[i], image, x, y, w, h)
            coordinate_list.append(new_img)
    return coordinate_list


def get_img(counter, image, x, y, w, h):
    img_crop = image[y:y + h, x:x + w]
    center = (w // 2, h // 2)
    _, _, angle = rect = cv2.minAreaRect(counter)
    if 90 >= angle >= 45:
        angle = angle - 90
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img_crop, M, (int(w), int(h)), flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_CONSTANT)


def print_doc(counters, image, image_name):
    for i in range(0, len(counters)):
        x, y, w, h = cv2.boundingRect(counters[i])
        if w > 30 and h > 40:
            new_img = get_img(counters[i], image, x, y, w, h)
            cv2.imshow(image_name, new_img)


if __name__ == '__main__':
    img = cv2.imread('docs.jpg')
    cv2.imshow('Image orig', img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours, hierachy = find_counters(img_gray)
    coordinate_list = find_coordinate(contours, img)
    for i, item in enumerate(coordinate_list):
        img_gray = cv2.cvtColor(item, cv2.COLOR_BGR2GRAY)
        contours, hierachy = find_counters(img_gray)
        print_doc(contours, item, f'Image_{i}')
    cv2.waitKey(0)

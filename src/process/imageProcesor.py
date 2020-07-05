# -*- coding: utf-8 -*-

import cv2
from cv2.dnn import readNet
import numpy as np
import traceback

def anonimize(img, alg, mode=15,path="."):
    net = cv2.dnn.readNet(path+"/model/deploy.prototxt", 
                          path+"/model/res10_300x300_ssd_iter_140000.caffemodel")

    (h, w) = img.shape[:2]

    blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            face = img[startY:endY, startX:endX]
            face = alg(face, mode)
            img[startY:endY, startX:endX] = face

    return img


#Anonimizado
# From: https://github.com/jlgarridol/Python-OpenCV-Guide/blob/master/src/2%20-%20Introducci%C3%B3n%20a%20openCV.ipynb
def blur(img, factor):
    ret = img
    try:
        (h, w) = img.shape[:2]
        kW = int(w / factor)
        kH = int(h / factor)

        if kW % 2 == 0:
            kW -= 1
        if kH % 2 == 0:
            kH -= 1
        ret = cv2.GaussianBlur(img, (kW, kH), 0)
    except:
        pass

    return ret

# From: https://www.pyimagesearch.com/2020/04/06/blur-and-anonymize-faces-with-opencv-and-python/
def pixel(image, blocks=3):
	(h, w) = image.shape[:2]
	xSteps = np.linspace(0, w, blocks + 1, dtype="int")
	ySteps = np.linspace(0, h, blocks + 1, dtype="int")

	for i in range(1, len(ySteps)):
		for j in range(1, len(xSteps)):

			startX = xSteps[j - 1]
			startY = ySteps[i - 1]
			endX = xSteps[j]
			endY = ySteps[i]


			roi = image[startY:endY, startX:endX]
			(B, G, R) = [int(x) for x in cv2.mean(roi)[:3]]
			cv2.rectangle(image, (startX, startY), (endX, endY),
				(B, G, R), -1)

	return image

# Reparación de brillo y contraste
# From https://stackoverflow.com/questions/57030125/automatically-adjusting-brightness-of-image-with-opencv

def repair_bright_and_contrast(img, bright, contrast):
    alpha, beta = automatic_brightness_and_contrast(img)
    if not bright:
        alpha = 1
    if not contrast:
        beta = 0
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def automatic_brightness_and_contrast(image, clip_hist_percent=25):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate grayscale histogram
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    return alpha, beta
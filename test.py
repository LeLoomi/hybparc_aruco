import cv2 as cv

i = cv.imread("./alignment-save.png")
c = cv.cvtColor(i, cv.COLOR_BGRA2RGBA)
cv.imwrite("aaaaaa.png", c)
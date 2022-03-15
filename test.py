import cv2 as cv

cv.namedWindow('test', cv.WND_PROP_FULLSCREEN)
cv.setWindowProperty('test', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

img = cv.imread('screenshot_simulator.png')
resized = cv.resize(img, (2560, 1600))

cv.imshow('test', resized)
cv.waitKey()

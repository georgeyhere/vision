# https://stackoverflow.com/questions/63195577/how-to-locate-qr-code-in-large-image-to-improve-decoding-performance
#
# This is a set a functions to:
#   - configure a capture object
#   - capture a frame
#   - perform preprocessing
#   - detect QR codes in frame
#
import string
from tokenize import String
import cv2
import numpy as np
import sys 
import time
import pyzbar.pyzbar as pyzbar
#

# 
def printInfo():
    print('OpenCV Version', cv2.__version__)
    print("QR Scanner initialized.")

# Utility function to get a video frame from webcam.
# @param:  cap is a cv2.videoCapture object.
# @return: The captured frame.
def captureFrame(cap):
    ret, frame = cap.read()
    if ret == False:
        print("Capture failed.")
    return frame

# Utility function to perform preprocessing (blur + thresholding)
# @param:  img is a frame to perform preprocessing on.
# @return: The preprocessed frame.
def preProcess(img):
    img = cv2.medianBlur(img, 3)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.adaptiveThreshold(img_gray, 
                                 255,
	                             cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY, 
                                 151, 
                                 10)
    
# Function to display frame and bbox
# @param:  img is a frame barcodes were detected in.
# @param:  barcodes are barcode objects returned by pyzbar.
#
# @return: img is the input frame with detected qr codes highlighted w/ rectangle and text.
# @return: centerId is the ID of the detected barcode, starting from 0
# @return: centerPts is the center point of the detected barcode (x,y)
# @return: centerDat is the data encoded in the barcode.
def decodeAndDraw(img, barcodes):
    centerId  = np.empty(shape=(16))
    centerPts = np.empty(shape=(16,16))
    centerDat = [String] * 16
    
    # iterate through detected barcodes:
    i = 0
    for barcode in barcodes:
        # draw bbox
        (x,y,w,h) = barcode.rect
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
        
        # draw decoded data on image
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        
        # put barcode data
        dataLabel = "{} {}".format(barcodeData, barcodeType)
        cv2.putText(img, dataLabel, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0,0,255), 2)
        
        # draw circle at center of qr
        centerCoord = (int(x+w/2), int(y+h/2))
        cv2.circle(img, centerCoord, 3, (0,0,255), 3)
        
        # put center coordinates
        coordLabel = "{}, {}".format(centerCoord[0], centerCoord[1])
        cv2.putText(img, coordLabel, (centerCoord[0]+8, centerCoord[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0,0,255), 2)
        
        #
        
        np.append(centerId, i)
        np.append(centerPts, centerCoord)
        np.append(centerDat, barcodeData)
        i = i+1
        
    return img, centerId, centerPts, centerDat

# Function to compare detected QR code locations against a predefined reference.
def posCompare(img, cap, centerIds, centerPts):
    offSets = np.empty(shape=(16))
    
    # get capture res
    x_res = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    y_res = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # demo ref is center of frame
    refCoord = (x_res/2, y_res/2)
    
    print(centerIds)
    print(centerPts)
    
    i=0
    for centerId in centerIds:
        codeId = int(centerId[i])
        offSets = (x_res-int(centerPts[codeId][0]), y_res-int(centerPts[codeId][1]) )

        # annote onto frame
        coordLabel = "Delta: {}, {}".format(offSets[0], offSets[1])
        cv2.putText(img, coordLabel, (int(centerPts[codeId][0])+8, int(centerPts[codeId][1])+8), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0,0,255), 2)
        i = i+1
        
    return img, offSets
    
# Function to detect QR code in an input image
def qrDetect(img):
    # detect barcodes in input image
    barcodes = pyzbar.decode(img)
    return barcodes

# Main function.  
def main():
    printInfo();
    
    # Stream webcam frames until 'q' is pressed.
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
    while True:
        frame = captureFrame(cap)
        prepFrame = preProcess(frame)
        barcodes = qrDetect(prepFrame)
        frame, centerIds, centerPts, codeData = decodeAndDraw(frame, barcodes)
        frame, codeOffsets = posCompare(frame, cap, centerIds, centerPts)
        
        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
#
if __name__ == "__main__":
    main()
    


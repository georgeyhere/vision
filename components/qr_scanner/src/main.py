# https://stackoverflow.com/questions/63195577/how-to-locate-qr-code-in-large-image-to-improve-decoding-performance
#
# This is a set a functions to:
#   - configure a capture object
#   - capture a frame
#   - perform preprocessing
#   - detect QR codes in frame
#
from cProfile import label
import string
from tokenize import String
import cv2
import numpy as np
import sys 
import time
import pyzbar.pyzbar as pyzbar
import pandas as pd


#

# 
def print_info():
    print('OpenCV Version', cv2.__version__)
    print("QR Scanner initialized.")

# Utility function to get a video frame from webcam.
# @param:  cap is a cv2.videoCapture object.
# @return: The captured frame.
def capture_frame(cap):
    ret, frame = cap.read()
    if ret == False:
        print("Capture failed.")
    return frame

# Utility function to perform preprocessing (blur + thresholding)
# @param:  img is a frame to perform preprocessing on.
# @return: The preprocessed frame.
def pre_process(img):
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
def decode_and_draw(img, barcodes, cap):
    centerId  = [None] * 16
    centerPts = np.empty(shape=(16,16))
    centerDat = [String] * 16
    
    #print("Number of detected barcodes: ", len(barcodes))
    # get capture res
    x_res = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    y_res = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # reference coordinate
    x_ref = int(x_res/2)
    y_ref = int(y_res/2)
    refCoord = (x_ref, y_ref)
    
    # draw circle at ref
    # draw circle at center of qr
    cv2.circle(img, (x_ref, y_ref), 3, (0,255,0), 3)
    
    # iterate through detected barcodes:
    i = int(0)
    for barcode in barcodes:
        # draw bbox
        (x,y,w,h) = barcode.rect
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
        
        # draw decoded data on image
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        
        # put barcode data
        dataLabel = "{} {}".format(barcodeData, barcodeType)
        cv2.putText(img, dataLabel, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX ,
                    0.5, (0,0,255), 2)
        
        # draw circle at center of qr
        centerCoord = (int(x+w/2), int(y+h/2))
        cv2.circle(img, centerCoord, 1, (0,0,255), 1)
        
        # put center coordinates
        coordLabel = "{}, {}".format(centerCoord[0], centerCoord[1])
        cv2.putText(img, coordLabel, (centerCoord[0]+8, centerCoord[1]), cv2.FONT_HERSHEY_COMPLEX ,
                    0.5, (0,0,255), 2)
        
        # get offset values
        offset_x = x_ref - centerCoord[0]
        offset_y = y_ref - centerCoord[1]
        
        # put offset values
        offsetLabel = "{}, {}".format(offset_x, offset_y)
        cv2.putText(img, offsetLabel, (centerCoord[0]+8, centerCoord[1]+15), cv2.FONT_HERSHEY_COMPLEX ,
                    0.5, (255,0,0), 2)
        
        # draw line from center of qr to reference
        cv2.line(img, centerCoord, refCoord, (255,0,0), 1)
        
        centerId[i] = i
        np.append(centerPts, centerCoord)
        np.append(centerDat, barcodeData)
        i = i+1
        
    return img, centerId, centerPts, centerDat
    
# Function to detect QR code in an input image
def qr_detect(img):
    # detect barcodes in input image
    barcodes = pyzbar.decode(img)
    return barcodes

# Main function.  
def main():
    print_info()
    
    # Stream webcam frames until 'q' is pressed.
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
    while True:
        frame = capture_frame(cap)
        prepFrame = pre_process(frame)
        barcodes = qr_detect(prepFrame)
        frame, centerIds, centerPts, codeData = decode_and_draw(frame, barcodes, cap)
        
        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
#
if __name__ == "__main__":
    main()
    


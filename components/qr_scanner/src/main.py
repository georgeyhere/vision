# https://stackoverflow.com/questions/63195577/how-to-locate-qr-code-in-large-image-to-improve-decoding-performance
#
# This is a set a functions to:
#   - configure a capture object
#   - capture a frame
#   - perform preprocessing
#   - detect QR codes in frame
#
import cv2
import numpy as np
import sys 
import time
import pyzbar
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
# @return: Barcode encoded data.
def decodeAndDisplay(img, barcodes):
    # iterate through detected barcodes:
    for barcode in barcodes:
        # draw bbox
        (x,y,w,h) = barcode.rect
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
        
        # draw decoded data on image
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        labelText = "{} {{}}".format(barcodeData, barcodeType)
        cv2.putText(img, labelText, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0,0,255), 2)
    
    # display frame
    cv2.imshow("Video", img)
    return barcodeData;
    
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
        frame = preProcess(frame)
        barcodes = qrDetect(frame)
        frame, barcodeData = decodeAndDisplay(frame, barcodes)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
#
if __name__ == "__main__":
    main()
    


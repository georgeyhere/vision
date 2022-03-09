# https://stackoverflow.com/questions/63195577/how-to-locate-qr-code-in-large-image-to-improve-decoding-performance
#
import cv2
import numpy as np
import sys 
import time
#
# Sanity Check
print("QR Scanner initialized.")


# Utility function to get a video frame from webcam.
# @param: cap is a cv2.videoCapture object.
def captureFrame(cap):
    ret, frame = cap.read()
    if ret == False:
        print("Capture failed.")
    return frame

# Utility function to perform preprocessing (blur + thresholding)
def preProcess(img):
    img = cv2.medianBlur(img, 3)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.adaptiveThreshold(img_gray, 
                                 255,
	                             cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                 cv2.THRESH_BINARY, 
                                 151, 
                                 10)
    

# Utility function to draw bounding box on frame.
def display(img, bbox):
    n = len(bbox)
    
    for j in range(n):
        cv2.line(img, 
                 tuple(bbox[j][0]), 
                 tuple(bbox[ (j+1) % n][0]), 
                 (255,0,0), 
                 3)
        cv2.imshow("Video", img)
    
# Function to detect QR code in an input image
def qrDetect(inputImage):
    qrDecoder = cv2.QRCodeDetector()

    # Look for a qr code.    
    t = time.time()
    data, bbox, rectifiedImage = qrDecoder.detectAndDecode(inputImage)
    print("Time Taken for Detect and Decode : {:.3f} seconds.".format(time.time() - t))
    
    # Print and return applicable outputs.
    if len(data) > 0:
        data = format(data)
        return 1, inputImage, bbox, data
    else:
        return 0, inputImage, 0, 0


# Main function.  
def main():
    print("I'm alive!")
    
    # Stream webcam frames until 'q' is pressed.
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
    while True:
        frame = captureFrame(cap)
        frame = preProcess(frame)
        ret, img, bbox, data = qrDetect(frame)
        
        if ret:
            # display(img, bbox) # breaks app
            cv2.imshow("Video", img) # works but no bbox
            print("Decoded Data : ", data)
        else:
            cv2.imshow("Video", img)
            print("QR Code not detected")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
#
if __name__ == "__main__":
    main()
    


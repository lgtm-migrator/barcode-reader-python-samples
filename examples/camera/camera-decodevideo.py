import cv2
from dbr import DynamsoftBarcodeReader
dbr = DynamsoftBarcodeReader()
import time
import os

import sys
sys.path.append('../')
# import config

results = None
# The callback function for receiving barcode results
def onBarcodeResult(data):
    global results
    results = data

def get_time():
    localtime = time.localtime()
    capturetime = time.strftime("%Y%m%d%H%M%S", localtime)
    return capturetime

def read_barcode():
    global results
    video_width = 0
    video_height = 0
    testVideo = r"D:\Work\TestVideoOrImage\QQ视频20191202145135.mp4"
    
    # vc = cv2.VideoCapture(testVideo)
    vc = cv2.VideoCapture(0)
    video_width  = vc.get(cv2.CAP_PROP_FRAME_WIDTH)
    video_height = vc.get(cv2.CAP_PROP_FRAME_HEIGHT)
    vc.set(3, video_width) #set width
    vc.set(4, video_height) #set height

    stride = 0
    if vc.isOpened():  
        dbr.InitLicense('Input your license')
        rval, frame = vc.read()
        stride = frame.strides[0]
    else:
        return

    windowName = "Barcode Reader"
    parameters = dbr.InitFrameDecodingParameters()
    parameters["MaxQueueLength"] = 30
    parameters["MaxResultQueueLength"] = 30
    parameters["Width"] = video_width
    parameters["Height"] = video_height
    parameters["Stride"] = stride
    parameters["ImagePixelFormat"] = dbr.IPF_RGB_888
    parameters["RegionTop"] = 0
    parameters["RegionLeft"] = 0
    parameters["RegionRight"] = 100
    parameters["RegionBottom"] = 100
    parameters["RegionMeasuredByPercentage"] = 1
    parameters["Threshold"] = 0.01
    parameters["FPS"] = 0


    dbr.StartVideoMode(parameters, onBarcodeResult)

    count = 0
    while True:
        if results != None:
            # thickness = 2
            # color = (0,255,0)
            for result in results:
                # print("barcode format: " + result[0])
                # print("barcode text: " + result[1])
                print("barcode format: " + str(result["BarcodeFormat"]))
                print("barcode format: " + result["BarcodeFormatString"])
                print("barcode text: " + result["BarcodeText"])
                localizationResult = result["LocalizationResult"]
                x1 = localizationResult["X1"]
                y1 = localizationResult["Y1"]
                x2 = localizationResult["X2"]
                y2 = localizationResult["Y2"]
                x3 = localizationResult["X3"]
                y3 = localizationResult["Y3"]
                x4 = localizationResult["X4"]
                y4 = localizationResult["Y4"]
                localizationPoints = [(x1,y1),(x2,y2),(x3,y3),(x4,y4)]
                print(localizationPoints)

                # cv2.line(frame, (x1, y1), (x2, y2), color, thickness)
                # cv2.line(frame, (x2, y2), (x3, y3), color, thickness)
                # cv2.line(frame, (x3, y3), (x4, y4), color, thickness)
                # cv2.line(frame, (x4, y4), (x1, y1), color, thickness)
            results = None

        rval, frame = vc.read()
        if rval == False:
            break
        # cv2.imshow(windowName, frame)
        
        # if count == 1000:
        #     break
        # else:
        #     count = count + 1
        # print(count)
        # start = time.time()
        try:
            ret = dbr.AppendVideoFrame(frame)
        except:
            pass
        

        # cost = (time.time() - start) * 1000
        # print('time cost: ' + str(cost) + ' ms')
        # 'ESC' for quit
        # key = cv2.waitKey(1)
        # if key == 27:
        #     break

    dbr.StopVideoMode()
    # cv2.destroyWindow(windowName)


if __name__ == "__main__":
    print("OpenCV version: " + cv2.__version__)
    read_barcode()
    print("over")

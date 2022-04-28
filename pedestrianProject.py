#!/usr/bin/python3

import jetson.inference
import jetson.utils

import argparse
import sys

parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.")

parser.add_argument("input_URI", type=str, default="", nargs='?', help="input video")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="output video")
parser.add_argument("--network", type=str, default="ssd-mobilenet-2", help="pre trained model we are using")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use")

try:  
    opt = parser.parse_known_args()[0] 
except:  
    print("")  
    parser.print_help()  
    sys.exit(0)

# setting up network object
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)

# our files that include the videos from our args at start
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv) 
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)

while True:
    img = input.Capture()   

    # detect objects in the image (with overlay)  
    detections = net.Detect(img, overlay=opt.overlay)   

    pCount = 0
    bCount = 0;
    cCount = 0;
    personId = 1;
    bikeId = 2;
    carId = 3;
    busId = 6;

    minAccuracy = 100;

    for detection in detections:   

        if detection.ClassID == personId:
            minAccuracy = min(minAccuracy, detection.Confidence*100);        
            pCount += 1
            
        if detection.ClassID == bikeId:
            minAccuracy = min(minAccuracy, detection.Confidence*100);        
            bCount += 1

        if detection.ClassID == carId or detection.ClassID == busId:
            minAccuracy = min(minAccuracy, detection.Confidence*100);        
            cCount += 1
        
    # render the image  
    output.Render(img)   

    # update the title bar  
    output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))   

    # print out performance info  
    net.PrintProfilerTimes()   
        
    # exit on input/output EOS  
    if not input.IsStreaming() or not output.IsStreaming():   
            break
        
print("there are " + str(pCount) + " pedestrians, " + str(cCount) + " automobiles, and " + str(bCount) + " bikes in your field of vision. This is with a mininum of " + str(minAccuracy) + "% confidence.")


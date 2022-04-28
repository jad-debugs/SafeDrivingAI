# SafeDrivingAI
#### Drivers alerted to automobiles and pedestrians around them
![model in action](https://i.imgur.com/TxXyTJr.jpg)

## How it Works
#### We load the ```ssd-movilenet-v2``` model on a ```detectnet``` object. We use the ```MS COCO``` dataset, which has 91 objects.  
#### We only check for buses, cars, pedestrians, and bikers though. We then render the image, highlighting the boundries of the detected objects and print what is located.

## To run this project
##### You need to make the normal preparations for your jetson, such as download the jetpack sdk and install pytorch and the ssd-mobilenet-v2 library.
##### Once completed simply follow the commands below to get the project into your home dir
```
$ cd
$ git clone https://github.com/jad-debugs/SafeDrivingAI/
$ ./pedestrianProject.py sanfran.jpg output.jpg
```
##### you can change the network by simply doing
```
$ ./pedestrianProject.py --network=<network cli arg>
```
##### a generic example (input files can be videos)
```
$ ./pedestrianProject.py --network=<your networks cli arg> --overlay=<overlay wanted> <input file> <output file>
```
## Refrences
[DetectNet](https://github.com/dusty-nv/jetson-inference/blob/master/docs/detectnet-console-2.md)






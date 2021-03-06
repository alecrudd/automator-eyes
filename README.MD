

### Running on linux system
* Clone the repo
` git clone https://github.com/alecrudd/automator-eyes.git `
* Navigate to the folder location
* Make a new virtual environment.
``` shell
virtualenv .
``` 
This will make the virtual environment in the folder that you are currently in.
* Install the python dependencies
``` shell
pip install -r requirements.txt
``` 
 * Run the open-eyes.sh script
 ``` shell
 . /Path/to/script/open-eyes.sh
 ```

### Command Line Args
Arg               | Value      | Description
----------------- | ---------- | -------
--local           | N/A        | starts the stream on local host rather than the computer's IP
--rotate          | decimal    | Rotates the image by the given value. Ex --rotate -3
--zoom            | decimal    | Zooms in as a percent of the given value. Ex. --zoom 0.50 would be 1/2 the size of the webcam resolution
--crop            | width height | Crops by the given number of pixels in the width and height. Crop is always symmetric. ex. --crop 10 20 would crop 10 pixels off each side of the width, and 20 off of each side of the height

### End Points

The webcam streams are hosted on the computer's IP address (or localhost, if --local option is used). The end points are below. Note that ` n ` is the camera number on the server.

Url | Description
-------------- | -------
/stream/n      | raw webcam feed. n = camera number
/end           | stops the server

Query Params   | Description
-------------  | -------------
transform      | the transform to apply. Values: `{'glyph', 'stream', 'barcode'}`

The ID of the camera must be appended onto the URL as well. An example of a full url would be
```
192.168.1.100:5000/stream/0    # returns a stream from 192.168.1.100's camera 0, looking for glyphs
192.168.1.120:5000/stream/4?transform=glyph   # returns a stream from 192.168.1.120's camera 4,  trying to find glyphs
```

To end the server, simply navigate to the server's IP (with port) with then ` /end ` end point.
For example
```
192.1.100:5000/end       # stops the webcam server
```
Usually this would be done from a command line
``` shell
$ curl 192.1.100:500/end
> Stopped all cameras.
```

### Dev Set up
* Install python 2.7 (if you don't have it)
* Install opencv 3.2
  * Do something like
> http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/
* Create a virtual environment (see instructions in the link above)
* link the python binaries to the virutal env
``` shell
ln -s /usr/local/lib/python2.7/site-packages/cv2.so ~/.virtualenvs/MyVirtualEnv/lib/python/site-packages/cv2.so 
```

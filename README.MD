

### Running on linux system
* Clone the repo
` git clone https://github.com/alecrudd/automator-eyes.git `
* Navigate to the folder location
* Make a new virtual environment.
``` 
virtualenv . 
```
This will make the virtual environment in the folder that you are currently in. 
* Install the python dependencies 
```
pip install -r requirements.txt
```
 * Run the open-eyes.sh script
 ```
 . /Path/to/script/open-eyes.sh
 ```

### Command Line Args
Arg | Value | Description
----------------- | ---------- | -------
--local           | N/A | starts the stream on local host rather than the computer's IP
--rotate          | decimal | Rotates the image by the given value. Ex --rotate -3
--zoom            | decimal | Zooms in as a percent of the given value. Ex. --zoom 0.50 would be 1/2 the size of the webcam resolution
--crop            | width height | Crops by the given number of pixels in the width and height. Crop is always symetric. ex. --crop 10 20 would crop 10 pixels off each side of the width, and 20 off of each side of the height 

### Streams

The webcam streams are hosted on the computer's IP address (or localhost, if --local option is used). The end points are below. Note that ` n ` is the camera number on the server. 

Url | Description
-------------- | -------
/stream/n      | raw webcam feed
/barcode/n     | looks for barcodes
/glyph/n       | looks for glyphs
/end           | stops the server

The ID of the camera must be appended onto the URL as well. An example of a full url would be 
```
192.168.1.100:5000/glyph/0    # returns a stream from 192.168.1.100's camera 0, looking for glyphs
192.168.1.120:5000/stream/4   # returns a stream from 192.168.1.120's camera 4, raw webcam footage
```

To end the server, simply navigate to the server's IP (with port) with then ` /end ` end point.
For example
```
192.1.100:5000/end       # stops the webcam server
```
Usually this would be done from a command line 
```
$ curl 192.1.100:500/end
> Stopped all cameras.
```

### Dev Set up
* Install python 2.7 (if you don't have it)
* Install opencv 3.2
  * Do something like
> http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/
* Create a virtual environment (see instructions in the link above)

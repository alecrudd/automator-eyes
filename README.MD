

### Running on automator
* The easiest way is to just clone the repository onto the automator
* Navigate to the folder location
* Make a new virtual environment.
> virtualenv .
  This will make the virtual environment in the folder that you are currently in. This should probably be in ~/.virtualenvs or something
* Run open-eyes.sh
 * This tries to set some camera parameters then starts the virtualenvironnment (with `workon automator-eyes`). Output gets logged into the same folder that the main script is in

### Dev Set up
* Install python 2.7 (if you don't have it)
* Install opencv 3.2
  * Do something like
> http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/
* Create a virtual environment (see instructions in the link above)

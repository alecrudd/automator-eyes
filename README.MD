

### Running on automator
* The easiest way is to just clone the repository onto the automator
* Make the startup script runnable
> chmod 700 /path/to/open-eyes.sh
*   Edit the crontab so that it runs the script on boot
> crontab -e
* Add the line
> @reboot /path/to/open-eyes.sh
* Save the file
> ctrl + X K

### Dev Set up
* Install python 2.7 (if you don't have it)
* Install opencv 3.2
  * Do something like
> http://www.pyimagesearch.com/2015/06/22/install-opencv-3-0-and-python-2-7-on-ubuntu/
* Create a virtual environment (see instructions above)

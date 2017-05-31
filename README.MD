

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

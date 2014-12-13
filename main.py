__author__ = "Saptarshi Gan"
__copyright__ = "Copyright (C) 2014 Saptarshi Gan"
__license__ = "GNU GENERAL PUBLIC LICENSE Version 2"
__version__ = "1.0"

SOURCE = ""
#comment out above line and uncomment following line to use a custom video folder
#SOURCE = "/storage/sdcard/videos"

from front import VideoManagerApp
if __name__ == '__main__':
	VideoManagerApp().run()
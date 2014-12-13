from kivy.uix.button import Button
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.actionbar import ActionBar,ActionButton
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
from kivy.logger import Logger  
from glob import glob
from random import randint
from os.path import join, dirname,isdir
import ntpath as NT

class CustomPlayer(VideoPlayer):
	"""Override methods of VideoPlayer"""
	def on_touch_down(self, touch):
		if not self.collide_point(*touch.pos):
			return False
		#pause and play on double tap
		if touch.is_double_tap:
			if self.state == 'play':
				self.state = 'pause'
			else:
				self.state = 'play'
			return True
		return super(VideoPlayer, self).on_touch_down(touch)

class MyScatter(Scatter):
	"""Override Scatter class to include bring to focus function for the class"""
	__events__ = ('on_transform_with_touch', 'on_bring_to_front')
	
	def _bring_to_front(self, touch):
		# auto bring to front
		if self.auto_bring_to_front and self.parent:
			parent = self.parent
			if parent.children[0] is self:
				return
			parent.remove_widget(self)
			parent.add_widget(self)
			self.dispatch('on_bring_to_front', touch)

	def on_touch_down(self, touch):
		x, y = touch.x, touch.y

		# if the touch isnt on the widget we do nothing
		if not self.do_collide_after_children:
			if not self.collide_point(x, y):
				return False

		# let the child widgets handle the event if they want
		touch.push()
		touch.apply_transform_2d(self.to_local)
		if super(Scatter, self).on_touch_down(touch):
			# ensure children don't have to do it themselves
			if 'multitouch_sim' in touch.profile:
				touch.multitouch_sim = True
			touch.pop()
			self._bring_to_front(touch)
			return True
		touch.pop()

		# if our child didn't do anything, and if we don't have any active
		# interaction control, then don't accept the touch.
		if not self.do_translation_x and \
				not self.do_translation_y and \
				not self.do_rotation and \
				not self.do_scale:
			return False

		if self.do_collide_after_children:
			if not self.collide_point(x, y):
				return False

		if 'multitouch_sim' in touch.profile:
			touch.multitouch_sim = True
		# grab the touch so we get all it later move events for sure
		self._bring_to_front(touch)
		touch.grab(self)
		self._touches.append(touch)
		self._last_touch_pos[touch] = touch.pos

		return True

	def on_bring_to_front(self,touch):
		if not self.collide_point(*touch.pos):
			return False
		else:
			mychild = self.children[0]
			parent = self.parent
			for child in parent.children:
				if (child != self) :
					child.children[0].state = 'pause'
			#print "PARENT125",self.parent
			self.children[0].state = 'play'
			return True

class VideoLayout(FloatLayout):
	"""docstring for VideoLayout"""
	def __init__(self, folder,par_folder):
		super(VideoLayout, self).__init__()
		self.folder = folder
		self.par_folder = par_folder
		self.size_hint = (1,1)
		self.pos_hint = {'top':0.8}

	def body_layout(self):
		layout = self
		curdir = join(dirname(__file__),self.par_folder)
		pos_x = pos_y =0
		thumb_folder = "thumbs"
		for filename in glob(join(curdir,self.folder,'*')):
			if(not isdir(filename)):
				try:
					file_parts = NT.basename(filename).rsplit('.',1)
					thumbnail = join(curdir,self.folder,thumb_folder,file_parts[0]) + '.png'
					video = CustomPlayer(source=filename, state='stop',size_hint=(None,None),size=(400, 200),\
					 allow_fullscreen=False,allow_stretch=True, thumbnail=thumbnail)
					scatter = MyScatter(height=200, width=400,size_hint=(None, None),rotation=randint(-30,30), \
					scale_min=.5,scale_max=4.,auto_bring_to_front = True)
					scatter.add_widget(video)
					layout.add_widget(scatter) #combine image widget with scatter
					video.parent.size = video.size
					video.parent.pos = pos_x,pos_y
					if (pos_x+400 >= 1200):
						pos_y += 220
					else:
						pos_y = pos_y
					pos_x = (pos_x+420)%1200
				except Exception as e:
					Logger.exception('Videos: Unable to load <%s>' % filename)
		return layout

class TopAction(ActionBar):
    """docstring for TopAction"""
    def __init__(self,dirs):
        super(TopAction, self).__init__()
        #self.canvas.add(Color(1,1,0))
        av = self.children[0]
        #av =ActionView(use_seperator=True)
        for d in dirs:
            b = ActionButton(text=d)
            b.bind(on_release=self.callback)
            av.add_widget(b)
        #self.add_widget(av)
    def callback(self,button):
        screen = self.parent
        text = button.text
        videos = screen.children[0].children
        self.pause_videos(videos)
        screen.manager.current = text
        #screen.manager.current = text

    def pause_videos(self,videos):
        for scatter in videos:
            video = scatter.children[0]
            video.state = 'pause'
        return
                    
class CustomScreen(Screen):
    hue = NumericProperty(0)
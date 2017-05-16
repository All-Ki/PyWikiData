import pprint , re , json , sys
import json 
import gi
gi.require_version('Gtk', '3.0')
# import pygtk
from gi.repository import GObject
from gi.repository import Gtk as gtk

""" http.://.*\..*. """ #links regexp

interface = gtk.Builder() #hopefully there is only one layout file
interface.add_from_file('kb_output.glade') #so i can set this to global

linktag=gtk.TextTag(name="LinkTag") #todo : implement


class OutputDisplay:
	def __init__(self):

		window=interface.get_object("window3")
		self.textDisp = interface.get_object("outputText")
		interface.connect_signals(self)
		window.show_all()
		
	
	def setText(self,target):
		self.textDisp.get_buffer().set_text(target)
			
	def setBuffer(self,tar):
		self.textDisp.set_buffer(tar)

		
class InputBox:
	def __init__(self):
		self.window = interface.get_object("window3")
		self.textInput = interface.get_object("textInput")
		self.textInput.connect("activate", self.enter_callback, self.textInput)
		self.window.connect("delete-event",self.on_mainWindow_destroy)
		interface.connect_signals(self)
		self.window.show_all()

	def on_mainWindow_destroy(self, widget):
		gtk.main_quit()
		exit(0)
	
	
	def enter_callback(self,widget,entry):
		text=entry.get_text()
		print(text)
		outputWindow =OutputDisplay()
		do(text,outputWindow)
		
	
"""
Properties (&prop)  :

!categories 
!pageprops !iwlinks
!links !images

?extlinks ?fileusage
?redirects ?info

//linkshere //langlinks//imageinfo//categoryinfo
//contributors //deletedrevisions//duplicatefiles
//revisions//stashimageinfo//templates//transcludedin
"""
import pywikibot

# shit_to_remove=[
# "}","{","]","[",
# ]

def do(word,target):
	site = pywikibot.Site('en', 'wikipedia')  # any site will work, this is just an example
	page = pywikibot.Page(site, word)
	itempage=pywikibot.ItemPage.fromPage(page)
	
	pageprops=page.properties()
	links=itempage.iterlinks()
	
	pagetext=page.text  #full text
	catgen=page.categories()
	
	
	#####TEXT CLEANUP######
	# pagetext = re.sub('<.*>', '', pagetext)
	# for  item in shit_to_remove :
		# pagetext=pagetext.replace(item,'')
	# pagetext=pagetext.replace("\n","<br>")
	########################

	target.setText(pagetext) #Display text
	
	wikibase_item=pageprops["wikibase_item"]
	print(wikibase_item) # good
	

if __name__ == "__main__":
	a = InputBox()
	if(len(sys.argv)!=1): #rainmeter <3
		b=OutputDisplay()
		do(sys.argv[1],b)
		
	gtk.main()
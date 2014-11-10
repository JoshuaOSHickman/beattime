from gi.repository import Gtk, GObject
from gi.repository import AppIndicator3 as appindicator
import time
import os

def menuitem_response(w, buf):
  print buf

os.environ['TZ'] = 'Europe/Zurich'
time.tzset()
def current_beattime():
	swisstime = time.localtime()
	t = float(swisstime.tm_hour) / 24.0
	t += float(swisstime.tm_min) / (24.0 * 60.0)
	t += float(swisstime.tm_sec) / (24.0 * 60.0 * 60.0)
	return 'd{}.{}.{}@{}'.format(swisstime.tm_year % 100, 
		swisstime.tm_mon, swisstime.tm_mday, 
		int(1000 * t))

UPDATE_TIMEOUT = .1
updating_timeout = None
counter = 0
def update(ind):
	global updating_timeout, counter
        if updating_timeout is not None: 
            GObject.source_remove(updating_timeout)

        #self.updater.add_update(self.done_updating) # returns immediately
	counter += 1
	ind.set_label(current_beattime(), "right")
        # call in UPDATE_TIMEOUT seconds
        updating_timeout = GObject.timeout_add(int(UPDATE_TIMEOUT*1000), lambda: update(ind))

if __name__ == "__main__":
  """
Some general resources about this weirdo barely documented API

You need to add this ppa
https://launchpad.net/~indicator-applet-developers/+archive/ubuntu/indicator-core-ppa

and then run

sudo apt-get install gtk2hs-buildtools

And then read
https://wiki.ubuntu.com/DesktopExperienceTeam/ApplicationIndicators
and 
https://wiki.ubuntu.com/MenuBar#GTK2.2BAC8-GTK3_application_integration

Which doesn't have enough detail to do anything but copy paste

so then read

http://developer.ubuntu.com/api/devel/ubuntu-13.10/python/AppIndicator3-0.1.html



"""
# so, that application-running was selected from /usr/share/icons, looking for subfolders that had the indicator-messages file, and choosing something else that was less intrusive. Not many "not intrusive" options.
  ind = appindicator.Indicator.new (
                        "beattime",
                        "application-running", #"indicator-messages",
                        appindicator.IndicatorCategory.APPLICATION_STATUS)
  ind.set_status (appindicator.IndicatorStatus.ACTIVE)
  #ind.set_attention_icon ("indicator-messages-new")
  ind.set_label("initializing beat time...", "right")

  # create a menu (
  menu = Gtk.Menu()
  # create some 
  #for i in range(3):
    #buf = "Test-undermenu - %d" % i
    #menu_items = Gtk.MenuItem(buf)
    #menu.append(menu_items)
    # this is where you would connect your menu item up with a function:
    # menu_items.connect("activate", menuitem_response, buf)
    # show the items
    #menu_items.show()
  ind.set_menu(menu)
  update(ind)
  Gtk.main()


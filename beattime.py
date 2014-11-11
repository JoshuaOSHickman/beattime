from gi.repository import Gtk, GObject
from gi.repository import AppIndicator3 as appindicator
from datetime import datetime, tzinfo, timedelta
import os

ONE_HOUR = timedelta(hours = 1)
NO_DST = timedelta(0)
class SwissTime(tzinfo):
	def utcoffset(self, dt):
		return ONE_HOUR

	def tzname(self, dt):
		return "Europe/Zurich"

	def dst(self, dt):
		return NO_DST

def current_beattime():
	swisstime = datetime.now(SwissTime())
	normaltime = datetime.now()
	t = float(swisstime.hour) / 24.0
	t += float(swisstime.minute) / (24.0 * 60.0)
	t += float(swisstime.second) / (24.0 * 60.0 * 60.0)
	return 'd{:02d}.{:02d}.{:02d}@{:03d}'.format(normaltime.year % 100, 
		normaltime.month, normaltime.day, 
		int(1000 * t))

UPDATE_TIMEOUT = .1
updating_timeout = None
def update(ind):
	global updating_timeout
        if updating_timeout is not None: 
            GObject.source_remove(updating_timeout)

	ind.set_label(current_beattime(), "right") # this value "right" is completely made up, all I know is it can't be None

        # call in UPDATE_TIMEOUT seconds
        updating_timeout = GObject.timeout_add(int(UPDATE_TIMEOUT*1000), lambda: update(ind))

if __name__ == "__main__":
  """
Some general resources about this weirdo barely documented API

You need to add this ppa
https://launchpad.net/~indicator-applet-developers/+archive/ubuntu/indicator-core-ppa

and then run

sudo apt-get install gtk2hs-buildtools # there is probably a python specific thing I should use here, but this seemed to work

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


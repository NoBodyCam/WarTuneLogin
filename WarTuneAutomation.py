# Script to show walking a WarTune character around in a circle
# NobodyCam@gmail.com 10.5.2013

from splinter import *
from Tkinter import *

from pymouse import PyMouse
from pykeyboard import PyKeyboard


from gi.repository import Gtk
from gi.repository import Wnck
import time

# define the steps for WarTune
def WarTune():
    """Logic for WarTune character control."""
    # Define values for WarTune
    website_name = 'WarTune'
    print ' - Setting up the vars for: %s' % website_name
    browser_type = 'firefox' # 'phantomjs' or 'firefox'
    url = 'http://www.wartune.com/index.action'
    username = '<CharacterName>'
    password = '<Password>'
    login_to_server = 's45'
    character_window_title = 'Wartune Server 45 - Mozilla Firefox'

    main_window_id = ''
    character_window = ''
    screen_max_x = 0
    screen_max_y = 0

    # set up whats needed for mouse and keyboard control
    print ' - Creating required objects.'
    mouse = PyMouse()
    keyboard = PyKeyboard()

    # get the screen size
    print ' - Get screen size'
    screen_max_x, screen_max_y = mouse.screen_size()

    # don't forget the browser
    print ' - Starting the browser..'
    browser = Browser(browser_type)

    # get the window id so we can switch to the popup window after we login
    main_window_id = browser.windows[0]
    print ' - Main window Id: %s' % main_window_id

    # login to WarTune as character defined above.
    attemptLogin(url, username, password, website_name, browser, login_to_server)

    # get second window that was spwaned
    character_window = findWindow(main_window_id, browser)

    # select Character window
    browser.switch_to_window(character_window)

    # handle fullscreen alert
    with browser.get_alert() as window_size_alert:
        window_size_alert.accept()

    # close the left side pannel
    browser.find_by_id('bt_turn').click()

    # ensure character window is the active window
    selectCharacterWindow(character_window_title)

    # click in the center of the screen
    mouse.click(screen_max_x/2, screen_max_y/2, 1)

    # wait for the screen to load
    print ' - wait for %s to load.' % website_name
    time.sleep(45)

    # walk the caracter in a circle x times
    walkinCircle(mouse, screen_max_x, screen_max_y, 15)

    # end of example
    print '- eoe'

# Functions #
def walkinCircle(mouse, max_x, max_y, times=10):
    """Simple mouse click loop to walk in a circle."""
    # test walking around
    # for something like world boss it would be: walk up, walk upper right,
    # fight
    for tmp_counter in range(1, times):
        print ' - click mouse in upper left side of the screen'
        mouse.click(max_x/4, max_y/4, 1)
        time.sleep(3)
        print ' - click mouse in middle of the screen'
        mouse.click(max_x/2, max_y/2, 1)
        time.sleep(3)

def selectCharacterWindow(window_to_select):
    """Select the characters window."""
    Gtk.init([])  # necessary only if not using a Gtk.main() loop
    screen = Wnck.Screen.get_default()
    screen.force_update()  # recommended per Wnck documentation

    # loop all windows
    for window in screen.get_windows():
        if window.get_name() == window_to_select:
            print ' - Getting window %s info' % window_to_select
            window.get(window.get_xid())
            print ' - Activating window %s' % window_to_select
            window.activate(int(time.time()))
            print ' - Setting window %s fullscreen' % window_to_select
            window.set_fullscreen(True)

    # clean up Wnck (saves resources, check documentation)
    window = None
    screen = None
    Wnck.shutdown()

def findWindow(main_window_id, browser):
    """Find the spwaned window."""
    # Find window other then the main and return its id
    print 'Looking for windows other then: %s' % main_window_id
    window_list =  browser.windows
    window_found = ''
    for window in window_list:
        if window == main_window_id:
            continue
        print 'Found Window: %s' % window
        if window != '':
            window_found = window
    return window

def attemptLogin(url, username, password, website_name, browser, login_to_server):
    """Login as character and select server."""
    print '## Attempting to login to ' + website_name + ', please wait.'

    # Visit in the url
    print '- Visiting the login url: %s' % url
    browser.visit(url)

    # Find the username form and fill it with the defined username
    print '- Filling the username form with the defined username..'
    browser.fill('userName', username)

    # Find the password form and fill it with the defined password
    print '- Filling the password form with the defined password..'
    browser.fill('password1', password)

    # Find the Play Now button and click
    print '- Clicking the Login button..'
    browser.find_by_name('send').click()

    # Ckick the link to the correct server
    tmp_server_link = 'loginGameServerEx.action?serverNo=%s' % login_to_server
    browser.find_link_by_href(tmp_server_link).first.click()

    # Find, click and display page with order history
    print '- Visiting the defined web page..'
    current_token = browser.url[57:97]
    print 'current_token: %s' % current_token

# The actual program
WarTune()

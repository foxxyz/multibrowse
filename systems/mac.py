from functools import lru_cache
import os
from subprocess import call, Popen, DEVNULL
import sys
from time import sleep

# Only available on MacOS
try:
    from AppKit import NSScreen
except ImportError:
    raise ImportError("PyObjC does not seem to be installed. Install it with `pip install -U pyobjc`")

from . import BaseSystem


class System(BaseSystem):

    def __init__(self):
        self.tasks = []

    def apple_script(self, script):
        "Perform apple script via call()"
        commands = [arg for statement in script.split('\n') for arg in ['-e', statement.strip()] if statement.strip()]
        return call(['osascript'] + commands)

    @property
    def browser_path(self):
        return os.path.join('/', 'Applications', 'Google Chrome.app', 'Contents', 'MacOS', 'Google Chrome')

    def clean_up(self):
        "Perform clean up tasks"
        for index, task in enumerate(self.tasks, 1):
            task(index)

    def close_existing_browsers(self):
        result = call(['killall', 'Google Chrome'], stdout=DEVNULL, stderr=DEVNULL)
        # Give some time to shut down
        sleep(2)
        return result

    @property
    @lru_cache()
    def displays(self):
        screens = NSScreen.screens()
        connected = []
        for screen in screens:
            screen = screen.frame()
            origin_y = screen.origin.y
            # Flip coordinate space because Apple is weird
            # https://developer.apple.com/documentation/coregraphics/cgrect
            if len(connected) > 0:
                origin_y = -screen.size.height - (origin_y - connected[0]["y"])
            connected.append({
                "x": int(screen.size.width),
                "y": int(screen.size.height),
                "offset_x": int(screen.origin.x),
                "offset_y": int(origin_y)
            })
        return connected

    def fullscreen(self, window_num=1):
        # Send the command for switching Chrome windows (command-`)
        # and the command for full screen (command-ctrl-F)
        #
        # Before we switch windows here, we need to reindex this window to
        # the *next* window (I.E. 2), which will be switched to when pressing
        # command-`. We also need to add a tiny delay, which seems to remedy
        # inconsistent window-switching behavior that occurs otherwise. Thanks Apple.
        self.apple_script("""
            tell application "Google Chrome"
                activate
                set index of window {} to {}
                delay 0.05
                tell application "System Events"
                    keystroke "`" using {{command down}}
                    keystroke "f" using {{control down, command down}}
                end tell
            end tell
        """.format(window_num, 2 if len(self.tasks) > 1 else 1))

        # Wait for the OSX fullscreen animation to complete
        sleep(1)

    def open_browser(self, url, display_num=0):
        # Get current display
        try:
            display = self.displays[display_num]
        except IndexError:
            print('Error: No display number {}'.format(display_num + 1), file=sys.stderr)
            return

        # Open browser window
        args = [
            self.browser_path,
            '--app={}'.format(url),
            '--new-window',
            '--disable-pinch',
            '--disable-infobars',
            '--window-position={},{}'.format(display['offset_x'], display['offset_y']),
            '--no-first-run',  # Skip dialog boxes asking for default browser and sending usage statistics to google
        ]
        Popen(args, stdout=DEVNULL, stderr=DEVNULL)

        # Give Chrome a second to open
        sleep(1)

        # Move the window to the other monitor
        self.apple_script("""
            tell application "Google Chrome"
                set bounds of window 1 to {{{}, {}, {}, {}}}
            end tell
        """.format(display['offset_x'], display['offset_y'], display['offset_x'] + 500, display['offset_y'] + 500))

        # Add a fullscreen task after all windows have been opened
        self.tasks.append(self.fullscreen)

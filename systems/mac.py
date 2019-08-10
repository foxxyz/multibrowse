from functools import lru_cache
from operator import itemgetter
import os
from shutil import rmtree
from subprocess import call, Popen, DEVNULL
import sys
from tempfile import gettempdir
from time import sleep

# Only available on MacOS
try:
    from AppKit import NSScreen
except ImportError:
    raise ImportError("PyObjC does not seem to be installed. Install it with `pip install -U pyobjc`")

from . import BaseSystem


class System(BaseSystem):

    @property
    def browser_path(self):
        return os.path.join('/', 'Applications', 'Google Chrome.app', 'Contents', 'MacOS', 'Google Chrome')

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
                "width": int(screen.size.width),
                "height": int(screen.size.height),
                "x": int(screen.origin.x),
                "y": int(origin_y)
            })
        # Sort displays by y, then by x for consistent ordering
        return sorted(sorted(connected, key=itemgetter('x')), key=itemgetter('y'))

    def open_browser(self, url, display_num=0):
        # Get current display
        try:
            display = self.displays[display_num]
        except IndexError:
            print('Error: No display number {}'.format(display_num + 1), file=sys.stderr)
            return

        user_dir = os.path.join(gettempdir(), str((display_num + 1) * 100))

        # Remove previous user data dir folder to bust cache and prevent session restore bubble from appearing
        rmtree(user_dir, ignore_errors=True)

        args = [
            self.browser_path,
            '--no-first-run',
            '--disable-pinch',
            '--user-data-dir={}'.format(user_dir),
            '--window-size={},{}'.format(display['width'], display['height']),
            '--window-position={},{}'.format(display['x'], display['y']),
            '--kiosk',
            '--app={}'.format(url),
        ]
        Popen(args, stdout=DEVNULL, stderr=DEVNULL)

from functools import lru_cache
import re
from subprocess import run, check_output, Popen, DEVNULL
from uuid import uuid4

from . import System


class PosixSystem(System):
    OS_NAME = 'posix'

    @property
    @lru_cache()
    def browser_path(self):
        return check_output(['which', 'google-chrome-stable'])[:-1].decode('utf8')

    def close_existing_browsers(self):
        return run(['killall', '-9', 'chrome'], stdout=DEVNULL, stderr=DEVNULL)

    @property
    @lru_cache()
    def displays(self):
        connected = []
        for line in check_output(['xrandr']).decode('utf8').split('\n'):
            if ' connected' in line:
                matches = re.match(r".* (?P<x>[0-9]+)x(?P<y>[0-9]+)\+(?P<offset_x>[0-9]+)\+(?P<offset_y>[0-9]+)", line)
                connected.append(matches.groupdict())
        return connected

    def open_browser(self, url, display_num=0):
        display = self.displays[display_num]
        Popen([
            self.browser_path,
            url,
            '--new-window',
            '--kiosk',
            '--window-position={},{}'.format(display['offset_x'], display['offset_y']),
            '--user-data-dir=/tmp/{}'.format(uuid4()),  # Create a random user data dir so chrome will see every instance as independent and not open them in the same window
            '--no-first-run',  # Skip dialog boxes asking for default browser and sending usage statistics to google
        ], stdout=DEVNULL, stderr=DEVNULL)

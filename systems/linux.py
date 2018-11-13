from functools import lru_cache
import os
import re
from subprocess import call, check_output, Popen, DEVNULL
import sys
from time import sleep

from . import BaseSystem


class System(BaseSystem):

    def __init__(self):
        self.open_windows = set()

    @property
    @lru_cache()
    def browser_path(self):
        return check_output(['which', 'google-chrome-stable'])[:-1].decode('utf8')

    def close_existing_browsers(self):
        return call(['killall', '-9', 'chrome'], stdout=DEVNULL, stderr=DEVNULL)

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
        # Get current display
        try:
            display = self.displays[display_num]
        except IndexError:
            print('Error: No display number {}'.format(display_num + 1), file=sys.stderr)
            return

        # Open browser window
        args = [
            self.browser_path,
            url,
            '--new-window',
            '--disable-pinch',
            '--disable-infobars',
            '--window-position={},{}'.format(display['offset_x'], display['offset_y']),
            '--no-first-run',  # Skip dialog boxes asking for default browser and sending usage statistics to google
        ]
        Popen(args, stdout=DEVNULL, stderr=DEVNULL)
        sleep(1)

        # Find browser process handle
        # This will always return a number of window IDs, but only one of them is the actual window, so compare
        # them to window_ids we're seen earlier to find the new one
        try:
            window_ids = check_output(['xdotool', 'search', '--class', 'Chrome']).decode('utf-8').split('\n')
        except FileNotFoundError:
            print('Looks like xdotool is not installed. Install it with `sudo apt-get install xdotool`', file=sys.stderr)
            return
        if not self.open_windows:
            self.open_windows = set(window_ids)
            win_id = window_ids[0]
        else:
            win_id = next(iter(set(window_ids) - self.open_windows))
            self.open_windows.add(win_id)

        # Move to correct position
        call(['xdotool', 'windowmove', win_id, display['offset_x'], display['offset_y']])

        # Set to full screen and refresh
        for key in ['F11', 'F5']:
            call(['xdotool', 'windowactivate', '--sync', win_id, 'key', key])

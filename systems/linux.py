from functools import lru_cache
import re
from subprocess import call, check_output, DEVNULL

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
        for idx, line in enumerate(check_output(['xrandr']).decode('utf8').split('\n')):
            if ' connected' in line:
                matches = re.match(r".* (?P<width>[0-9]+)x(?P<height>[0-9]+)\+(?P<x>[0-9]+)\+(?P<y>[0-9]+)", line)
                display = matches.groupdict()
                display['id'] = idx
                connected.append(display)
        return connected

from functools import lru_cache
import re
from subprocess import call, check_output, DEVNULL, CalledProcessError

from . import BaseSystem

BINARIES = [
    'chromium-browser',     # ubuntu/debian
    'chromium',             # arch
    'google-chrome-stable', # arch
]

class System(BaseSystem):

    @property
    @lru_cache()
    def browser_path(self):
        for binary in BINARIES:
            try:
                return check_output(['which', binary], stderr=DEVNULL)[:-1].decode('utf8')
            except CalledProcessError:
                pass
        raise FileNotFoundError("No supported browsers found!")

    @property
    @lru_cache()
    def displays(self):
        connected = []
        for idx, line in enumerate(check_output(['xrandr']).decode('utf8').split('\n')):
            if ' connected' in line:
                matches = re.match(r".* (?P<width>[0-9]+)x(?P<height>[0-9]+)\+(?P<x>[0-9]+)\+(?P<y>[0-9]+)", line)
                display = {k: int(v) for k, v in matches.groupdict().items()}
                display['id'] = idx
                connected.append(display)
        return connected

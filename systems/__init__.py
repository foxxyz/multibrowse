from abc import ABCMeta, abstractmethod
import os
from shutil import rmtree
from subprocess import Popen, DEVNULL
from tempfile import gettempdir


class BaseSystem(metaclass=ABCMeta):
    "Abstract system class to implement OS-specific methods"

    @property
    @abstractmethod
    def browser_path(self):
        "Return the path to the Chrome executable"
        pass

    @abstractmethod
    def displays(self):
        "Return info about attached displays and their properties"
        pass

    def open_browser(self, url, display, flags=[]):
        "Open an instance of Chrome with url on display number display_num"
        # Use unique user directory for this display
        user_dir = os.path.join(gettempdir(), str(display['id'] * 100))

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
        ] + flags
        Popen(args, stdout=DEVNULL, stderr=DEVNULL)

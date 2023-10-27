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
            # Disable "what's new" and "welcome" modals
            '--no-first-run',
            # Disable native pinch gestures
            '--disable-pinch',
            # Use basic password store so keyring access is not necessary
            '--password-store=basic',
            # Create a new profile so instances are not opened in the same window
            '--user-data-dir={}'.format(user_dir),
            # Spawn in correct location
            '--window-size={},{}'.format(display['width'], display['height']),
            '--window-position={},{}'.format(display['x'], display['y']),
            # Full-screen with no access to windowed mode or dev tools
            '--kiosk',
            # Prevent "Chrome is outdated" pop-up
            '--simulate-outdated-no-au="01 Jan 2199"',
            # Use application mode
            '--app={}'.format(url),
        ] + flags
        Popen(args, stdout=DEVNULL, stderr=DEVNULL)

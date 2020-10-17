import ctypes
from functools import lru_cache
from shutil import rmtree
import os
from subprocess import call, DEVNULL
import sys
from tempfile import gettempdir
import time

from . import BaseSystem

user = ctypes.windll.user32


class System(BaseSystem):

    @property
    def browser_path(self):
        dirs = ['Program Files (x86)', 'Program Files']
        paths = [os.path.join('C:\\', dir, 'Google', 'Chrome', 'Application', 'chrome.exe') for dir in dirs]
        for path in paths:
            if os.path.isfile(path):
                return path

        # For consistent failure behavior with respect to previous versions
        return paths[0]

    @property
    @lru_cache()
    def displays(self):
        monitors = []

        # Get monitor info via user32.EnumDisplayMonitors"
        def cb(handle, _, __, ___):
            monitors.append(handle)
            return 1
        winwrap = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(RECT), ctypes.c_double)
        user.EnumDisplayMonitors(0, 0, winwrap(cb), 0)

        # Get monitor area info returned via user32.GetMonitorInfoA
        areas = []
        for idx, handle in enumerate(monitors):
            mi = MONITORINFO()
            mi.cbSize = ctypes.sizeof(MONITORINFO)
            mi.rcMonitor = RECT()
            mi.rcWork = RECT()
            user.GetMonitorInfoA(handle, ctypes.byref(mi))
            bounds = mi.rcMonitor.dump()
            bounds.update({"id": idx})
            areas.append(bounds)
        return areas


# Windows Ctypes for interacting with the Windows API
class RECT(ctypes.Structure):
    _fields_ = (
        ('left', ctypes.c_long),
        ('top', ctypes.c_long),
        ('right', ctypes.c_long),
        ('bottom', ctypes.c_long),
    )

    def dump(self):
        return {
            'x': int(self.left),
            'y': int(self.top),
            'width': int(self.right) - int(self.left),
            'height': int(self.bottom) - int(self.top)
        }


class MONITORINFO(ctypes.Structure):
    _fields_ = (
        ('cbSize', ctypes.c_ulong),
        ('rcMonitor', RECT),
        ('rcWork', RECT),
        ('dwFlags', ctypes.c_ulong)
    )

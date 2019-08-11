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
        return os.path.join('C:\\', 'Program Files (x86)', 'Google', 'Chrome', 'Application', 'chrome.exe')

    def close_existing_browsers(self):
        return call('taskkill /f /im chrome.exe', stdout=DEVNULL, stderr=DEVNULL)

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

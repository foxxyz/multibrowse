import ctypes
from functools import lru_cache
from shutil import rmtree
import os
import subprocess
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
        return subprocess.call('taskkill /f /im chrome.exe')

    @lru_cache()
    def displays(self):
        monitors = []

        # Get monitor info via user32.EnumDisplayMonitors"
        def cb(handle, _, lprcMonitor, __):
            monitors.append([handle, lprcMonitor.contents.dump()])
            return 1
        winwrap = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(RECT), ctypes.c_double)
        user.EnumDisplayMonitors(0, 0, winwrap(cb), 0)

        # Get monitor area info returned via user32.GetMonitorInfoA
        areas = []
        for handle, _ in monitors:
            mi = MONITORINFO()
            mi.cbSize = ctypes.sizeof(MONITORINFO)
            mi.rcMonitor = RECT()
            mi.rcWork = RECT()
            user.GetMonitorInfoA(handle, ctypes.byref(mi))
            areas.append(mi.rcMonitor.dump())
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


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (
        ('dx', ctypes.c_long),
        ('dy', ctypes.c_long),
        ('mouseData', ctypes.c_ulong),
        ('dwFlags', ctypes.c_ulong),
        ('time', ctypes.c_ulong),
        ('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong))
    )


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (
        ('wVk', ctypes.c_ushort),
        ('wScan', ctypes.c_ushort),
        ('dwFlags', ctypes.c_ulong),
        ('time', ctypes.c_ulong),
        ('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong))
    )


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (
        ('uMsg', ctypes.c_ulong),
        ('wParamL', ctypes.c_ushort),
        ('wParamH', ctypes.c_ushort)
    )


class INPUTunion(ctypes.Union):
    _fields_ = (
        ('mi', MOUSEINPUT),
        ('ki', KEYBDINPUT),
        ('hi', HARDWAREINPUT)
    )


class INPUT(ctypes.Structure):
    _fields_ = (
        ('type', ctypes.c_ulong),
        ('union', INPUTunion)
    )

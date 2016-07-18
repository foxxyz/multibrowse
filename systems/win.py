import ctypes
import os
import subprocess
import time
try:
    user = ctypes.windll.user32
except AttributeError:
    user = None

from . import System


class WindowsSystem(System):

    @classmethod
    def is_current(self):
        return os.name == 'nt'

    @property
    def browser_path(self):
        return os.path.join('C:\\', 'Program Files (x86)', 'Google', 'Chrome', 'Application', 'chrome.exe')

    def close_existing_browsers(self):
        return subprocess.call('taskkill /f /im chrome.exe')

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
            areas.append([handle, mi.rcMonitor.dump(), mi.rcWork.dump()])
        return areas

    def open_browser(self, url, display_num=0):
        subprocess.Popen([self.browser_path, url, '--new-window', '--incognito'])
        time.sleep(2)

        # Find browser process handle
        titles = []
        winwrap = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

        def process_handler(handle, _):
            if user.IsWindowVisible(handle):
                length = user.GetWindowTextLengthW(handle)
                buff = ctypes.create_unicode_buffer(length + 1)
                user.GetWindowTextW(handle, buff, length + 1)
                if 'Chrome' in buff.value:
                    process_id = ctypes.c_int()
                    user.GetWindowThreadProcessId(handle, ctypes.byref(process_id))
                    titles.append((handle, buff.value))
            return True
        user.EnumWindows(winwrap(process_handler), 0)

        # Move browser to monitor position, 500x500 px
        monitors = self.displays()
        user.MoveWindow(titles[0][0], monitors[display_num][1]['left'], monitors[display_num][1]['top'], 500, 500, True)
        user.SetForegroundWindow(titles[0][0])

        # Send a fullscreen keypress event
        key = 0x7A  # F11
        key = INPUT(1, INPUTunion(ki=KEYBDINPUT(key, key, 0, 0, None)))
        n_inputs = 1
        LPINPUT = INPUT * n_inputs
        p_inputs = LPINPUT(key)
        cb_size = ctypes.c_int(ctypes.sizeof(INPUT))
        user.SendInput(n_inputs, p_inputs, cb_size)


# Windows Ctypes

class RECT(ctypes.Structure):
    _fields_ = (
        ('left', ctypes.c_ulong),
        ('top', ctypes.c_ulong),
        ('right', ctypes.c_ulong),
        ('bottom', ctypes.c_ulong),
    )

    def dump(self):
        return {key: int(getattr(self, key)) for key in ('left', 'top', 'right', 'bottom')}


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

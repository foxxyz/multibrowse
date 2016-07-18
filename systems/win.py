import ctypes
import os
import subprocess
import time
try:
    user = ctypes.windll.user32
    from .win_types import RECT, MONITORINFO, KEYBDINPUT, INPUT, INPUTunion
except AttributeError:
    user = None

from . import System


class WindowsSystem(System):
    OS_NAME = 'nt'

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

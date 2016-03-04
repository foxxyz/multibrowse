#!/usr/bin/env python3
import ctypes
import os
import platform
import subprocess
import sys
import time
try:
    user = ctypes.windll.user32
    from wintypes import RECT, MONITORINFO, MOUSEINPUT, KEYBDINPUT, INPUT, INPUTunion
except AttributeError:
    user = None

# Set browser info
BROWSER = {
    'path': ['/usr', 'bin', 'google-chrome-stable'],
    'name': 'Chrome',
    'process': 'chrome',
}

# Override settings for Windows
if platform.system() == 'Windows':
    BROWSER['path'] = ['C:\\', 'Program Files (x86)', 'Google', 'Chrome', 'Application', 'chrome.exe']
    BROWSER['process'] = 'chrome.exe'


def get_monitors():
    "Get monitor info via user32.EnumDisplayMonitors"
    monitors = []

    def cb(handle, _, lprcMonitor, __):
        monitors.append([handle, lprcMonitor.contents.dump()])
        return 1

    winwrap = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(RECT), ctypes.c_double)
    user.EnumDisplayMonitors(0, 0, winwrap(cb), 0)
    return monitors


def monitor_areas():
    "Get monitor area info returned via user32.GetMonitorInfoA"
    areas = []
    for handle, _ in get_monitors():
        mi = MONITORINFO()
        mi.cbSize = ctypes.sizeof(MONITORINFO)
        mi.rcMonitor = RECT()
        mi.rcWork = RECT()
        res = user.GetMonitorInfoA(handle, ctypes.byref(mi))
        areas.append([handle, mi.rcMonitor.dump(), mi.rcWork.dump()])
    return areas


def open_browser(url, on_monitor=0):
    print('Opening {} on monitor {}'.format(url, on_monitor))
    task = subprocess.Popen([os.path.join(*BROWSER['path']), url, '--new-window', '--incognito'])
    time.sleep(2)

    # Find browser process handle
    titles = []
    winwrap = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

    def process_handler(handle, _):
        if user.IsWindowVisible(handle):
            length = user.GetWindowTextLengthW(handle)
            buff = ctypes.create_unicode_buffer(length + 1)
            user.GetWindowTextW(handle, buff, length + 1)
            if BROWSER['name'] in buff.value:
                process_id = ctypes.c_int()
                user.GetWindowThreadProcessId(handle, ctypes.byref(process_id))
                titles.append((handle, buff.value))
        return True
    user.EnumWindows(winwrap(process_handler), 0)

    # Move browser to monitor position, 500x500 px
    monitors = monitor_areas()
    user.MoveWindow(titles[0][0], monitors[on_monitor][1]['left'], monitors[on_monitor][1]['top'], 500, 500, True)
    user.SetForegroundWindow(titles[0][0])

    # Send a fullscreen keypress event
    key = 0x7A  # F11
    key = INPUT(1, INPUTunion(ki=KEYBDINPUT(key, key, 0, 0, None)))
    n_inputs = 1
    LPINPUT = INPUT * n_inputs
    p_inputs = LPINPUT(key)
    cb_size = ctypes.c_int(ctypes.sizeof(INPUT))
    user.SendInput(n_inputs, p_inputs, cb_size)

# Startup procedure
if __name__ == '__main__':
    urls = sys.argv[1:]
    if not urls:
        print('Usage: python run.py http://url1.com http://url2.com ...', file=sys.stderr)
        sys.exit()

    # Stop all existing browser instances
    try:
        subprocess.call('taskkill /f /im {}'.format(BROWSER['process']))  # Windows
    except FileNotFoundError:
        os.system('killall -9 {}'.format(BROWSER['process']))

    # Start new browser instance for each URL
    for index, url in enumerate(urls):
        open_browser(url, index)

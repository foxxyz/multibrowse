import ctypes


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
        ('union', _INPUTunion)
    )

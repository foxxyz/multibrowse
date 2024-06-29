use std::io::Error;
use std::mem;
use std::ptr;
use std::path::PathBuf;
use windows::{
    Win32::{
        Foundation::{BOOL, LPARAM, RECT, TRUE},
        Graphics::Gdi::{EnumDisplayMonitors, GetMonitorInfoW, HDC, HMONITOR, MONITORINFO, MONITORINFOEXW},
    }
};
use crate::shared::Screen;

const SEARCH_DIRECTORIES: [&str; 2] = [
    "Program Files",          // x64 chrome
    "Program Files (x86)",    // x86 chrome
];

pub fn browser_path() -> String {
    for directory in SEARCH_DIRECTORIES {
        let path: PathBuf = [r"C:\", directory, "Google", "Chrome", "Application", "chrome.exe"].iter().collect();
        if path.exists() {
            return path.display().to_string();
        }
    }
    panic!("No suitable browser found to launch!");
}

pub trait Rectangle {
    fn width(&self) -> u32;
    fn height(&self) -> u32;
    fn x(&self) -> i32;
    fn y(&self) -> i32;
}

impl Rectangle for RECT {
    fn width(&self) -> u32 {
        (self.right - self.left) as u32
    }
    fn height(&self) -> u32 {
        (self.bottom - self.top) as u32
    }
    fn x(&self) -> i32 {
        self.left as i32
    }
    fn y(&self) -> i32 {
        self.top as i32
    }
}

unsafe extern "system" fn monitor_callback(monitor: HMONITOR, _: HDC, _: *mut RECT, vec: LPARAM) -> BOOL {
   let monitors = &mut *(vec.0 as *mut Vec<HMONITOR>);
   monitors.push(monitor);
   TRUE
}

pub fn monitor_info(id: u8, monitor: HMONITOR) -> Screen {
    let mut wrapper = MONITORINFOEXW {
        monitorInfo: MONITORINFO {
            cbSize: u32::try_from(mem::size_of::<MONITORINFOEXW>()).unwrap(),
            rcMonitor: RECT::default(),
            rcWork: RECT::default(),
            dwFlags: 0,
        },
        szDevice: [0; 32],
    };
    if unsafe {
       !GetMonitorInfoW(monitor, std::ptr::addr_of_mut!(wrapper).cast()).as_bool()
    } {
        panic!("Unable to get monitor info: {}", Error::last_os_error());
    }

    Screen {
        id: id,
        width: wrapper.monitorInfo.rcMonitor.width(),
        height: wrapper.monitorInfo.rcMonitor.height(),
        x: wrapper.monitorInfo.rcMonitor.x(),
        y: wrapper.monitorInfo.rcMonitor.y(),
    }
}

pub fn displays() -> Vec<Screen> {
    let mut connected : Vec<Screen> = Vec::new();

    let mut monitors = Vec::<HMONITOR>::new();

    let result = unsafe {
	 EnumDisplayMonitors(None, None, Some(monitor_callback), LPARAM(ptr::addr_of_mut!(monitors) as isize)).as_bool()
    };
    
    if !result {
        panic!("Unable to get monitor info: {}", Error::last_os_error());
    }

    for (id, monitor) in monitors.iter().enumerate() {
        let screen = monitor_info(id as u8, *monitor);
        connected.push(screen);
    }

    connected
}

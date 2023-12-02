use std::io::Error;
use std::mem;
use std::ptr;
use std::path::PathBuf;
use winapi::shared::minwindef::{LPARAM, TRUE, BOOL};
use winapi::shared::windef::{HMONITOR, HDC, LPRECT, RECT};
use winapi::um::winuser::{EnumDisplayMonitors, GetMonitorInfoW, MONITORINFOEXW};
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

unsafe extern "system" fn monitor_callback(monitor: HMONITOR, _: HDC, _: LPRECT, results: LPARAM) -> BOOL {
    // Place to store results
    let monitors: &mut Vec<MONITORINFOEXW> = mem::transmute(results);
    // Place to store monitor info
    let mut monitor_info: MONITORINFOEXW = mem::zeroed();
    monitor_info.cbSize = mem::size_of::<MONITORINFOEXW>() as u32;
    let monitor_info_ptr = <*mut _>::cast(&mut monitor_info);
    // "W" indicates Unicode version, "A" indicates ANSI version
    let result = GetMonitorInfoW(monitor, monitor_info_ptr);
    if result == TRUE {
        monitors.push(monitor_info);
    }
    TRUE
}

pub fn displays() -> Vec<Screen> {
    let mut connected : Vec<Screen> = Vec::new();

    let mut monitors = Vec::<MONITORINFOEXW>::new();
    let results = &mut monitors as *mut _;

    let result = unsafe {
        EnumDisplayMonitors(ptr::null_mut(), ptr::null(), Some(monitor_callback), results as LPARAM)
    };
    
    if result != TRUE {
        panic!("Unable to get monitor info: {}", Error::last_os_error());
    }

    for (id, screen) in monitors.iter().enumerate() {
        connected.push(Screen {
            id: id as u8,
            width: screen.rcMonitor.width(),
            height: screen.rcMonitor.height(),
            x: screen.rcMonitor.x(),
            y: screen.rcMonitor.y()
        })
    }

    connected
}

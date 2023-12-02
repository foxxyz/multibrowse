use std::path::PathBuf;
use winapi::um::winuser::{EnumDisplayMonitors, GetMonitorInfoA

const SEARCH_DIRECTORIES: [&str; 2] = [
    "Program Files",          // x64 chrome
    "Program Files (x86)",    // x86 chrome
];

pub fn browser_path() -> String {
    for directory in SEARCH_DIRECTORIES {
        const path: PathBuf = ["C:", directory, "Google", "Chrome", "Application", "chrome.exe"].iter().collect();
        if path.exists() {
            return path;
        }
    }
    panic!("No suitable browser found to launch!");
}

pub trait Rectangle {
    fn width(&self) -> LONG;
    fn height(&self) -> LONG;
}

impl Rectangle for Rect {
    fn width(&self) -> LONG {
        self.right - self.left
    }
    fn height(&self) -> LONG {
        self.bottom - self.top
    }
}

unsafe fn monitor_callback(monitor: HMONITOR, _: HDC, _: LPRECT, results: LPARAM) -> BOOL {
    // Place to store results
    let monitors: &mut Vec<MONITORINFOEXW> = mem::transmute(results);
    // Place to store monitor info
    let mut monitor_info: MONITORINFOEXW = mem::zeroed();
    monitor_info.cbSize = mem::size_of::<MONITORINFOEXW>() as u32;
    let monitor_info_ptr = <*mut _>::cast(&mut monitor_info);

    let result = GetMonitorInfoA(monitor, monitor_info_ptr);
    if result == TRUE {
        results.push(monitor_info);
    }
    TRUE
}

pub fn displays() -> Vec<Screen> {
    let mut connected : Vec<Screen> = Vec::new();

    let mut monitors = Vec::<MONITORINFOEXW>::new();
    let results = &mut monitors as &mut _;

    let result = unsafe {
        EnumDisplayMonitors(ptr::null_mut(), ptr::null(), Some(monitor_callback), results as LPARAM)
    }
    
    if result != TRUE {
        panic!("Unable to get monitor info: {}", Error::last_os_error());
    }

    for screen in results {
        dbg!(screen);
    }

    // unsafe {
    //     let screens = NSScreen::screens();
    //     for (id, screen) in screens.iter().enumerate() {
    //         let CGRect { origin, size, .. } = screen.frame();
    //         // Flip coordinate space because Apple is weird
    //         // https://developer.apple.com/documentation/coregraphics/cgrect
    //         let mut origin_y = origin.y as i32;
    //         let height = size.height as u32;
    //         if connected.len() > 0 {
    //             origin_y = -(height as i32) - (origin_y - connected[0].y);
    //         }
    //         connected.push(Screen {
    //             id: id as u8,
    //             width: size.width as u32,
    //             height,
    //             x: origin.x as i32,
    //             y: origin_y,
    //         })
    //     }
    // }
    connected
}

use std::fs::remove_dir_all;
use std::env;
use subprocess::{Exec, NullFile};
use std::path::Path;
use std::process;

mod shared {
    #[derive(Debug)]
    pub struct Screen {
        pub id: u8,
        pub width: u32,
        pub height: u32,
        pub x: i32,
        pub y: i32
    }
}

#[cfg_attr(target_os = "macos", path = "platforms/macos.rs")]
#[cfg_attr(target_os = "linux", path = "platforms/linux.rs")]
mod platform;

use crate::shared::Screen;

fn open_browser(url: &str, screen: &Screen, flags: &Vec<String>) {
    // Use unique user directory for this display so we can open multiple windows
    let mut user_dir = env::temp_dir();
    user_dir.push((screen.id as u32 * 100).to_string());

    // If user data dir already exists, remove it to bust cache and prevent session restore bubble from appearing
    _ = remove_dir_all(&user_dir);
    
    // Browser path
    Exec::cmd(Path::new(&platform::browser_path()))
        // Disable "what's new" and "welcome" modals
        .arg("--no-first-run")
        // Disable native pinch gestures
        .arg("--disable-pinch")
        //Use basic password store so keyring access is not necessary
        .arg("--password-store=basic")
        //Create a new profile so instances are not opened in the same window
        .arg(format!("--user-data-dir={}", user_dir.display()))
        // Spawn in correct location
        .arg(format!("--window-size={},{}", screen.width, screen.height))
        .arg(format!("--window-position={},{}", screen.x, screen.y))
        // Full-screen with no access to windowed mode or dev tools
        .arg("--kiosk")
        // Prevent "Chrome is outdated" pop-up
        .arg("--simulate-outdated-no-au=\"01 Jan 2199\"")
        // Use application mode
        .arg(format!("--app={url}"))
        .stdout(NullFile)
        .stderr(NullFile)
        .detached()
        .popen()
        .expect("Unable to spawn browser window.");
}

fn main() {
    println!("Multibrowse v3.0");
    let args: Vec<String> = env::args().collect();

    // Not enough args, exit with help message
    if args.len() <= 1 {
        eprintln!("Usage: multibrowse https://url1.com https://url2.com ...");
        process::exit(1);
    }

    let mut urls: Vec<String> = Vec::new();
    let mut flags: Vec<String> = Vec::new();
    for arg in &args[1..] {
        if arg.starts_with("--") {
            flags.push(arg.to_string());
        } else {
            urls.push(arg.to_string());
        }
    }

    let screens: Vec<Screen> = platform::displays();
    for (idx, url) in urls.iter().enumerate() {
        if url == "-" {
            println!("Skipping display {}", idx + 1);
            continue
        }
        println!("Opening {} on display {}", url, idx + 1);
        open_browser(url, &screens[idx], &flags);
    }

}

use std::process::Command;
use crate::shared::Screen;
use regex::Regex;

const POSSIBLE_BROWSER_BINARIES: [&str; 3] = [
    "chromium-browser",    // ubuntu/debian
    "chromium",            // arch
    "google-chrome-stable" // arch
];

pub fn browser_path() -> String {
    for binary in POSSIBLE_BROWSER_BINARIES {
        let which = Command::new("which")
            .arg(binary)
            .output()
            .expect("unable to get browser location!");
        let location = String::from_utf8_lossy(&which.stdout);
	let location = location.trim_end_matches("\n").to_string();
        if location != "" {
	    return location;
	}
    }
    panic!("No suitable browser found to launch!");
}

pub fn displays() -> Vec<Screen> {
    let mut connected: Vec<Screen> = Vec::new();
    let xrandr = Command::new("xrandr")
    	.output()
	.expect("Please install xrandr to use multibrowse!");
    let output = String::from_utf8_lossy(&xrandr.stdout);
    let re = Regex::new(r" ([0-9]+)x([0-9]+)\+([0-9]+)\+([0-9]+)").unwrap();
    let lines = output.lines();
    for (id, line) in lines.enumerate() {
        if !line.contains(" connected") {
	    continue;
	}
    	let (_, [width, height, x, y]) = re.captures(line).unwrap().extract();
	connected.push(Screen {
	    id: id as u8,
	    width: width.parse::<u32>().unwrap(),
	    height: height.parse::<u32>().unwrap(),
	    x: x.parse::<i32>().unwrap(),
	    y: y.parse::<i32>().unwrap()
	})
    }
    connected
}
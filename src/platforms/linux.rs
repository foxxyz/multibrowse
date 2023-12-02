use std::process::Command;

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
        //dbg!(location);
        return location.trim_end_matches("\n").to_string();
    }
    panic!("No suitable browser found to launch!");
}

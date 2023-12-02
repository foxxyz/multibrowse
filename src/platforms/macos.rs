use icrate::AppKit::NSScreen;
use icrate::Foundation::CGRect;
use crate::shared::Screen;

pub fn browser_path() -> String {
    String::from("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
}

pub fn displays() -> Vec<Screen> {
    let mut connected : Vec<Screen> = Vec::new();
    unsafe {
        let screens = NSScreen::screens();
        for (id, screen) in screens.iter().enumerate() {
            let CGRect { origin, size, .. } = screen.frame();
            // Flip coordinate space because Apple is weird
            // https://developer.apple.com/documentation/coregraphics/cgrect
            let mut origin_y = origin.y as i32;
            let height = size.height as u32;
            if connected.len() > 0 {
                origin_y = -(height as i32) - (origin_y - connected[0].y);
            }
            connected.push(Screen {
                id: id as u8,
                width: size.width as u32,
                height,
                x: origin.x as i32,
                y: origin_y,
            })
        }
    }
    connected
}

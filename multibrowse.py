#!/usr/bin/env python3
from operator import itemgetter
import os
import sys

__version__ = '1.7.0'

# Conditionally import correct system
if sys.platform.startswith('linux'):
    from systems.linux import System
elif sys.platform.startswith('darwin'):
    from systems.mac import System
elif sys.platform.startswith('win32'):
    from systems.win import System
else:
    raise SystemExit('Sorry, multibrowse is not supported for your platform ({}).'.format(sys.platform))

# Startup procedure
if __name__ == '__main__':
    print('Multibrowse v{}'.format(__version__))

    # Get arguments
    urls = sys.argv[1:]
    if not urls:
        print('Usage: {} http://url1.com http://url2.com ...'.format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    # Init associated system
    system = System()

    # Close existing windows
    system.close_existing_browsers()

    # Get existing displays
    displays = system.displays

    # Sort displays by y, then by x for consistent ordering
    displays = sorted(sorted(displays, key=itemgetter('x')), key=itemgetter('y'))

    # Start new browser instance for each URL
    for index, url in enumerate(urls):
        # Skip blank URLs
        if url == '-':
            print('Skipping monitor {}'.format(index + 1))
            continue
        # Get current display
        try:
            display = displays[index]
        except IndexError:
            print('Error: No display number {}'.format(display_num + 1), file=sys.stderr)
            continue
        print('Opening {} on monitor {}'.format(url, index + 1))
        system.open_browser(url, display)

    # Finish up any tasks
    system.clean_up()

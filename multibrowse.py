#!/usr/bin/env python3
from operator import itemgetter
import os
import sys

__version__ = '1.9.0'

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
    urls, flags = [], []
    for arg in sys.argv[1:]:
        flags.append(arg) if arg.startswith('--') else urls.append(arg)
    if not urls:
        print('Usage: {} http://url1.com http://url2.com ...'.format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    # Init associated system
    platform = System()

    # Close existing windows
    platform.close_existing_browsers()

    # Sort displays by y, then by x for consistent ordering
    displays = sorted(sorted(platform.displays, key=itemgetter('x')), key=itemgetter('y'))

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
            print('Error: No display number {}'.format(index + 1), file=sys.stderr)
            continue
        print('Opening {} on monitor {}'.format(url, index + 1))
        try:
            platform.open_browser(url, display, flags)
        except FileNotFoundError as e:
            print("Error: {}".format(e))

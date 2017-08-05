#!/usr/bin/env python3
import os
import sys

__version__ = '1.3.0'

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

    # Start new browser instance for each URL
    for index, url in enumerate(urls):
        # Skip blank URLs
        if url == '-':
            print('Skipping monitor {}'.format(index + 1))
            continue
        print('Opening {} on monitor {}'.format(url, index + 1))
        system.open_browser(url, index)

    # Finish up any tasks
    system.clean_up()

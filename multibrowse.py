#!/usr/bin/env python3
import os
import sys

from systems import *

__version__ = '1.3.0'


# Startup procedure
if __name__ == '__main__':
    print('Multibrowse v{}'.format(__version__))

    # Get arguments
    urls = sys.argv[1:]
    if not urls:
        print('Usage: {} http://url1.com http://url2.com ...'.format(sys.argv[0]), file=sys.stderr)
        sys.exit()

    # Find associated system to make calls on
    try:
        system = next(system for system in System.__subclasses__() if system.is_current())()
    except StopIteration:
        print('Sorry, multibrowse is not supported for your platform ({}).'.format(os.name), file=sys.stderr)
        sys.exit()

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

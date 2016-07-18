#!/usr/bin/env python3
import os
import sys

from systems import *

# Startup procedure
if __name__ == '__main__':

    # Get arguments
    urls = sys.argv[1:]
    if not urls:
        print('Usage: python run.py http://url1.com http://url2.com ...', file=sys.stderr)
        sys.exit()

    # Find associated system to make calls on
    try:
        system = next(system for system in System.__subclasses__() if system.OS_NAME == os.name)()
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

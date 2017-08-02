from abc import ABCMeta, abstractmethod

__all__ = ['System', 'linux', 'win', 'mac']


# Abstract system class to implement OS-specific methods
class System(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def is_current(self):
        "Return True if this is the current system"
        pass

    @property
    @abstractmethod
    def browser_path(self):
        "Return the path to the Chrome executable"
        pass

    def clean_up(self):
        "Perform any remaining clean up tasks"
        pass

    @abstractmethod
    def close_existing_browsers(self):
        "Close all existing instances of Chrome"
        pass

    @abstractmethod
    def displays(self):
        "Return info about attached displays and their properties"
        pass

    @abstractmethod
    def open_browser(self, url, display_num=0):
        "Open an instance of Chrome with url on display number display_num"
        pass

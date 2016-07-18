from abc import ABCMeta, abstractmethod

__all__ = ['System', 'posix', 'win']


# Abstract system class to implement OS-specific methods
class System(metaclass=ABCMeta):

    @property
    @abstractmethod
    def browser_path(self):
        pass

    @abstractmethod
    def close_existing_browsers(self):
        pass

    @abstractmethod
    def displays(self):
        "Return info about attached displays and their properties"
        pass

    @abstractmethod
    def open_browser(self, url, display_num=0):
        pass

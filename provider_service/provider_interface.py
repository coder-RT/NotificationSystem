from abc import ABCMeta, abstractmethod
import abc

class ProviderInterface(abc.ABC):
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()

    @abstractmethod
    def calculate_priority(self):
        raise NotImplementedError

    @abstractmethod
    def send_notification(self):
        pass

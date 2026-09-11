from abc import ABC, abstractmethod


class EmailProvider(ABC):

    @abstractmethod
    def send(
        self,
        recipient,
        subject,
        text,
        html=None
    ):
        raise NotImplementedError

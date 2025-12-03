from abc import ABC, abstractmethod

class BaseComunicador(ABC):
    @abstractmethod
    def connect_mqtt(self):
        pass

    @abstractmethod
    def disconnect_mqtt(self):
        pass

    @abstractmethod
    def send_message(self, destination_id, message_text):
        pass

    @abstractmethod
    def send_position(self, lat, lon, alt):
        pass

import abc

from common.configuration import AgentConfiguration


class IControlChannel(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def should_agent_stop(self) -> bool:
        """
        Checks if the agent should stop
        return: True if the agent should stop, False otherwise
        rtype: bool
        """

    @abc.abstractmethod
    def get_config(self) -> AgentConfiguration:
        """
        :return: An AgentConfiguration object
        :rtype: AgentConfiguration
        """
        pass

    @abc.abstractmethod
    def get_credentials_for_propagation(self) -> dict:
        """
        :return: A dictionary containing propagation credentials data
        :rtype: dict
        """
        pass


class IslandCommunicationError(Exception):
    """Raise when unable to connect to control client"""

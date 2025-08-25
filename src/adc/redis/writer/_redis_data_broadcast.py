import argparse
import json
from typing import List

from wai.logging import LOGGING_WARNING

from kasperl.redis.writer import AbstractRedisBroadcaster
from adc.api import AudioData


class RedisDataBroadcast(AbstractRedisBroadcaster):

    def __init__(self, redis_host: str = None, redis_port: int = None, redis_db: int = None,
                 include_audio: bool = False, channel_out: str = None, logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param redis_host: the redis host to use
        :type redis_host: str
        :param redis_port: the port to use
        :type redis_port: int
        :param redis_db: the database to use
        :type redis_db: int
        :param include_audio: whether to send the image as well
        :type include_audio: bool
        :param channel_out: the channel to broadcast the data on
        :type channel_out: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(redis_host=redis_host, redis_port=redis_port, redis_db=redis_db,
                         channel_out=channel_out, logger_name=logger_name, logging_level=logging_level)
        self.include_audio = include_audio

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "redis-data-broadcast"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Broadcasts the incoming data on the specified channel."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--include_audio", action="store_true", help="Whether to send the audio data as well.", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.include_audio = ns.include_audio

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.include_audio is None:
            self.include_audio = False

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [AudioData]

    def _process_data(self, data):
        """
        For processing the incoming data.

        :param data: the incoming data
        :return: the generated data to broadcast
        """
        d = data.to_dict(source=False, metadata=False, audio=self.include_audio)
        return json.dumps(d)

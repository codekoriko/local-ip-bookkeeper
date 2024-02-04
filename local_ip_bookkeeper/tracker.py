import json
import logging
import socket
from typing import Optional
from dotenv import load_dotenv, find_dotenv

from gist_storage.manage import GistManager


class IPTracker(object):
    """
    IPTracker class for tracking IP addresses.

    This class is responsible for tracking the IP address of a device and
    updating it in a Gist. The device needs to have an internet connection to
    be able to determine the relevant IP address among all the installed
    interface. cf: https://stackoverflow.com/a/25850698
    """

    def __init__(
        self,
        device_id: str,
        gist_hash: str,
        filename: str,
        interface_uid: Optional[str] = None,
    ):
        """
        Initialize an IPTracker object.

        Args:
            gist_hash (str): The hash of the Gist where IP addresses are stored.
            filename (str): The name of the file in the Gist where
            IP addresses are stored.
            device_id (str): The ID of the device whose IP address is
            being tracked.
        """
        self.device_id = device_id
        self.interface_uid = interface_uid
        load_dotenv(find_dotenv())
        self.gist_manager = GistManager(gist_hash, filename)
        try:
            self.gist_ips = self.gist_manager.fetch_json()
        except json.decoder.JSONDecodeError as error:
            raise ValueError((
                'Check the file content in the gist ' +
                f'it seems not to be a valid json: {error}'
            ))

    def update_ip(self):
        """
        Update the IP address of the device in the Gist if it has changed.
        """
        current_ip = self.get_device_ip()
        if self.gist_ips.get(self.device_id) == current_ip:
            logging.info(f'IP address of {self.device_id} has not changed.')
        else:
            self.gist_ips[self.device_id] = current_ip
            self.gist_manager.update_json({self.device_id: current_ip})
            logging.info((
                f'IP address of {self.device_id} has changed from ' +
                f'{self.gist_ips[self.device_id]} ' +
                f'to {current_ip}. Gist was updated.',
            ))

    def get_device_ip(self) -> str:
        """
        Get the IP address of the device.

        Returns:
            str: The IP address of the device.

        Raises:
            ValueError: If no interface UID is specified.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
        return s.getsockname()[0]

    def print_registery(self):
        """
        Print the current registry of IP addresses.
        """
        for device_id, ip in self.gist_ips.items():
            print(f'{device_id}: {ip}')

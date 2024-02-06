import json
import logging
import socket
from pathlib import Path
from typing import Dict

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
        self.gist_manager = GistManager(gist_hash, filename)
        self.ip_registery: Dict[str, str] = {}
        self.fetch_ip_registry()

    def sync_ip_registry(self):
        """
        Synchronizes the IP registry by fetching the latest IP addresses,
        comparing them with the current device's IP address, and updating
        the registry if necessary.
        """
        self.fetch_ip_registry()
        current_ip = self.get_device_ip()
        if self.ip_registery.get(self.device_id) == current_ip:
            logging.info(f'IP address of {self.device_id} has not changed.')
        else:
            self.ip_registery[self.device_id] = current_ip
            self.gist_manager.update_json({self.device_id: current_ip})
            logging.info((
                f'IP address of {self.device_id} has changed from ' +
                f'{self.ip_registery[self.device_id]} ' +
                f'to {current_ip}. Gist was updated.',
            ))

    def fetch_ip_registry(self):
        """
        Fetch the IP registry from the Gist.
        """
        try:
            self.ip_registery = self.gist_manager.fetch_json()
        except json.decoder.JSONDecodeError as error:
            raise ValueError((
                'Check the file content in the gist ' +
                f'it seems not to be a valid json: {error}'
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

    def save_ip_to_disk(self):
        """
        Save each IP address in the registry to the disk.

        We save them to separate files for easy use in bash scripts.
        """
        directory = Path('local_ips')
        directory.mkdir(exist_ok=True)
        for hostname, ip in self.ip_registery.items():
            with open(directory / hostname, 'w') as file:
                file.write(ip)
            logging.info(f'IP for {hostname} saved to disk.')

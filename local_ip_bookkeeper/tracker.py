import logging
from typing import Optional
import json

import netifaces as ni
from gist_storage.manage import GistManager


class IPTracker(object):
    """
    IPTracker class for tracking IP addresses.

    This class is responsible for tracking the IP address of a device and
    updating it in a Gist.
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
            interface_uid (Optional[str], optional): The UID of the network
            interface to use. If not specified, the default interface will
            be used. Defaults to None.
        """
        if interface_uid is None:
            interface_uid = ni.gateways()['default'][ni.AF_INET][1]
            logging.info((
                f'No interface specified, using default: {interface_uid}\n' +
                f'   With device ip: {self.get_device_ip(interface_uid)}',
            ))
        self.device_id = device_id
        self.interface_uid = interface_uid
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
        if self.gist_ips.get(self.device_id) != current_ip:
            self.gist_ips[self.device_id] = current_ip
            self.gist_manager.update_json({self.device_id: current_ip})

    def get_device_ip(self, interface_uid: Optional[str] = None) -> str:
        """
        Get the IP address of the device.

        Args:
            interface_uid (Optional[str], optional): The UID of the network
            interface to use. If not specified,the interface UID specified
            during initialization will be used.Defaults to None.

        Returns:
            str: The IP address of the device.

        Raises:
            ValueError: If no interface UID is specified.
        """
        interface = interface_uid or self.interface_uid
        if interface is None:
            raise ValueError('No interface specified')
        return ni.ifaddresses(interface).get(ni.AF_INET, [])[0]['addr']

    def print_registery(self):
        """
        Print the current registry of IP addresses.
        """
        for device_id, ip in self.gist_ips.items():
            print(f'{device_id}: {ip}')

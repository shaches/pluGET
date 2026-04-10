"""Handles the logic for the config validation, reading, and creating.

This module defines the configuration structure and utilities to manage
the 'pluGET_config.yaml' file.
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict

import ruamel.yaml


class ConfigValue:
    """Holds all the available configuration values from the config file.

    Attributes:
        path_to_plugin_folder (Path): Local path to plugins.
        local_seperate_download_path (bool): Whether to use a separate download path locally.
        local_path_to_seperate_download_path (Path): The separate local download path.
    """

    def __init__(self) -> None:
        """Initializes ConfigValue by loading data from the YAML file."""
        yaml = ruamel.yaml.YAML()
        config_path = Path("pluGET_config.yaml")

        if not config_path.exists():
            # Fallback or error handling if file doesn't exist when class is instantiated
            # Ideally check_config() ensures existence before this class is called.
            pass

        try:
            with config_path.open("r", encoding="utf-8") as config_file:
                data: Dict[str, Any] = yaml.load(config_file)
        except (OSError, ruamel.yaml.YAMLError) as e:
            print(f"Critical Error: Could not read config file: {e}")
            sys.exit(1)

        self.path_to_plugin_folder: Path = Path(data["PathToPluginFolder"])
        self.local_seperate_download_path: bool = bool(
            data["SeperateDownloadPath"]
        )
        self.local_path_to_seperate_download_path: Path = Path(
            data["PathToSeperateDownloadPath"]
        )


# Backward compatibility alias if other files import 'config_value'
config_value = ConfigValue


def check_config() -> None:
    """Checks if the config file exists.

    If 'pluGET_config.yaml' does not exist in the current directory,
    it creates a new default configuration and exits the program.
    """
    if not os.path.isfile("pluGET_config.yaml"):
        create_config()
    return None


def create_config() -> None:
    """Creates the YAML config file with default values and exits the program.

    This function writes the default 'pluGET_config.yaml' to the disk
    and prompts the user to edit it before restarting.
    """
    configuration = """\
#
# Configuration File for pluGET
# https://www.github.com/Neocky/pluGET
#

# Local path to your plugins folder
PathToPluginFolder: C:/Users/USER/Desktop/plugins

# If a different folder should be used to store the updated plugins,
# change to True and set the path below
SeperateDownloadPath: False
PathToSeperateDownloadPath: C:/Users/USER/Desktop/plugins
"""
    yaml = ruamel.yaml.YAML()
    code = yaml.load(configuration)

    try:
        with open("pluGET_config.yaml", "w", encoding="utf-8") as config_file:
            yaml.dump(code, config_file)
    except OSError as e:
        print(f"Error creating config file: {e}")
        sys.exit(1)

    config_file_path = os.path.abspath("pluGET_config.yaml")
    print(f"Path of config file: {config_file_path}")
    print("Config created. Edit config before executing again!")
    input("Press any key + enter to exit...")
    sys.exit()


def validate_config() -> None:
    """Validates critical configuration variables.

    Currently no validation is needed for local-only mode.
    Kept for backward compatibility.
    """
    pass

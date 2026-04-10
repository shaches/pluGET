"""
Removes the specified plugin file from the ./plugins folder
"""

import os
import re
from pathlib import Path
from rich.console import Console

from src.handlers.handle_config import config_value
from src.utils.console_output import rich_print_error


def delete_plugin(plugin_name: str) -> None:
    """
    Deletes the specific plugin file

    :param plugin_name: Name of plugin file to delete

    :returns: None
    """
    config_values = config_value()
    rich_console = Console()
    plugin_list = os.listdir(config_values.path_to_plugin_folder)

    for plugin_file in plugin_list:
        # skip all other plugins
        if not re.search(re.escape(plugin_name), plugin_file, re.IGNORECASE):
            continue

        try:
            plugin_path = Path(f"{config_values.path_to_plugin_folder}/{plugin_file}")
            if plugin_path.is_dir():
                rich_console.print(f"[not bold][bright_yellow]Skipped directory: [bright_magenta]{plugin_file} [bright_yellow]- plugin configs are not removed automatically")
                continue
            
            os.remove(plugin_path)
            rich_console.print(f"[not bold][bright_green]Successfully removed: [bright_magenta]{plugin_file}")
        except Exception as e:
            rich_print_error(f"[not bold]Error: Couldn't remove [bright_magenta]{plugin_file}[bright_red] - {e}")
    return None

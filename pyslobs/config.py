from pathlib import Path
from typing import Optional
import configparser
from dataclasses import dataclass

DEFAULT_DOMAIN = "localhost"
DEFAULT_PORT = 59650


@dataclass
class ConnectionConfig:
    """Information required to connect to StreamLabs Desktop."""

    token: str
    domain: str = DEFAULT_DOMAIN
    port: int = DEFAULT_PORT


def config_from_ini() -> Optional[ConnectionConfig]:
    """Read ConnectionConfig from ini files.
    Looks in:
        - <current dir>/pyslobs.ini
        - <current dir>/.pyslobs
        - <home dir>/pyslobs.ini
        - <home dir>/.pyslobs
    May return None if no ini file is found.
    """
    ini_file_paths = [
        Path.cwd() / "pyslobs.ini",
        Path.cwd() / ".pyslobs",
        Path.home() / "pyslobs.ini",
        Path.home() / ".pyslobs",
    ]
    parser = configparser.ConfigParser()
    if not parser.read(ini_file_paths):
        # No ini file
        return None
    assert (
        "connection" in parser.sections()
    ), "Ini file contains no 'connection' section"
    assert "token" in parser["connection"], "Ini file contains no 'token' value"
    token = parser["connection"]["token"]
    domain = parser["connection"].get("domain", DEFAULT_DOMAIN)
    try:
        port = int(parser["connection"].get("port", DEFAULT_PORT))
    except ValueError:
        assert False, "Port in ini file is not an integer"

    return ConnectionConfig(token, domain, port)


def config_from_ini_else_stdin() -> ConnectionConfig:
    """Read ConnectionConfig from ini files, but if they are absent,
    ask for API token on StdIn."""
    return config_from_ini() or ConnectionConfig(input("API Token: "))

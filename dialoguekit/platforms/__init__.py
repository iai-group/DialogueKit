"""Module level init for the platforms."""
from dialoguekit.platforms.flask_socket_platform import FlaskSocketPlatform
from dialoguekit.platforms.platform import Platform
from dialoguekit.platforms.terminal_platform import TerminalPlatform

__all__ = ["Platform", "TerminalPlatform", "FlaskSocketPlatform"]

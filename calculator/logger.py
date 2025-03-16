"""
Logger Module

Configures and provides application-wide logging capabilities with flexible
output destinations and configurable levels based on environment variables.
"""
import os
import sys
import logging
import logging.handlers
from typing import Dict, Optional, Union

class LoggerSetup:
    """
    Sets up and manages logging throughout the application with configurable
    severity levels and output destinations.
    """
    DEFAULT_CONFIG = {
        "log_level": "INFO",
        "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "log_dir": "logs",
        "log_file": "calculator.log",
        "log_to_console": True,
        "log_to_file": True,
        "log_rotation": True
    }

    LOG_LEVELS: Dict[str, int] = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    def __init__(self):
        """Initialize the logger setup with default values."""
        self.config = self._load_config()
        self.root_logger = logging.getLogger()

        # Create log directory if it doesn't exist
        if self.config["log_to_file"] and not os.path.exists(self.config["log_dir"]):
            os.makedirs(self.config["log_dir"], exist_ok=True)

        # Initialize the logger
        self._setup_logger()

    def _load_config(self) -> Dict[str, Union[str, bool]]:
        """Load configuration from environment variables or use defaults."""
        return {
            "log_level": os.getenv("LOG_LEVEL", self.DEFAULT_CONFIG["log_level"]).upper(),
            "log_format": os.getenv("LOG_FORMAT", self.DEFAULT_CONFIG["log_format"]),
            "log_dir": os.getenv("LOG_DIR", self.DEFAULT_CONFIG["log_dir"]),
            "log_file": os.getenv("LOG_FILE", self.DEFAULT_CONFIG["log_file"]),
            "log_to_console": self._str_to_bool(os.getenv("LOG_TO_CONSOLE", "True")),
            "log_to_file": self._str_to_bool(os.getenv("LOG_TO_FILE", "True")),
            "log_rotation": self._str_to_bool(os.getenv("LOG_ROTATION", "True")),
        }

    def _str_to_bool(self, value: str) -> bool:
        """Convert string value to boolean."""
        return value.lower() in ("yes", "true", "t", "1", "y")

    def _setup_logger(self):
        """Configure the root logger with the specified settings."""
        # Clear existing handlers
        self.root_logger.handlers = []

        # Set the log level
        self.root_logger.setLevel(self.LOG_LEVELS.get(self.config["log_level"], logging.INFO))

        # Create formatter
        formatter = logging.Formatter(self.config["log_format"])

        # Add console handler if enabled
        if self.config["log_to_console"]:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.root_logger.addHandler(console_handler)

        # Add file handler if enabled
        if self.config["log_to_file"]:
            log_path = os.path.join(self.config["log_dir"], self.config["log_file"])

            if self.config["log_rotation"]:
                # Use rotating file handler for log rotation
                file_handler = logging.handlers.RotatingFileHandler(
                    log_path, maxBytes=10 * 1024 * 1024, backupCount=5
                )
            else:
                # Use regular file handler
                file_handler = logging.FileHandler(log_path)

            file_handler.setFormatter(formatter)
            self.root_logger.addHandler(file_handler)

        # Log initial setup
        self.root_logger.info("Logging system initialized with level: %s",
                              self.config["log_level"])
        if self.config["log_to_file"]:
            self.root_logger.info("Logging to file:"
            " %s", os.path.join(self.config["log_dir"], self.config["log_file"]))

    def get_logger(self, name: str) -> logging.Logger:
        """Get a named logger."""
        return logging.getLogger(name)

    def update_level(self, new_level: Union[str, int]) -> None:
        """Update the log level for all handlers."""
        if isinstance(new_level, str):
            new_level = self.LOG_LEVELS.get(new_level.upper(), logging.INFO)

        self.root_logger.setLevel(new_level)
        for handler in self.root_logger.handlers:
            handler.setLevel(new_level)

        self.root_logger.info("Log level updated to: %s", logging.getLevelName(new_level))

    def add_file_handler(self, filename: str, level: Optional[Union[str, int]] = None) -> None:
        """Add an additional file handler, useful for specific logs."""
        if not os.path.exists(self.config["log_dir"]):
            os.makedirs(self.config["log_dir"], exist_ok=True)

        log_path = os.path.join(self.config["log_dir"], filename)
        formatter = logging.Formatter(self.config["log_format"])

        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)

        if level:
            if isinstance(level, str):
                level = self.LOG_LEVELS.get(level.upper(), logging.INFO)
            file_handler.setLevel(level)

        self.root_logger.addHandler(file_handler)
        self.root_logger.info("Added file handler for: %s", log_path)

# Create a singleton instance for global use
logger_setup = LoggerSetup()

def get_logger(name: str) -> logging.Logger:
    """Convenience function to get a named logger."""
    return logger_setup.get_logger(name)

# logger/__init__.py
import logging
from datetime import datetime
import os

class CustomLogger:
    """Custom logger class for the application."""

    def __init__(self):
        self.log_dir = "logs"
        os.makedirs(self.log_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file = os.path.join(self.log_dir, f"app_{timestamp}.log")

        self.logger = logging.getLogger("custom_chatbot_logger")

        # Prevent duplicate handlers if logger is recreated
        if not self.logger.handlers:
            # File Handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter(
                "[%(asctime)s] %(levelname)s - %(message)s"
            ))

            # Console Handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(
                "%(levelname)s: %(message)s"
            ))

            self.logger.setLevel(logging.INFO)
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

            # Optional: avoid duplicate logs from root logger
            self.logger.propagate = False

    def get_logger(self):
        """Return the configured logger."""
        return self.logger

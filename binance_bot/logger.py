import logging
import os
from logging.handlers import RotatingFileHandler

LOGGER_NAME = "binance_bot"
FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


def setup_logger(log_dir: str = "logs", verbose: bool = False) -> logging.Logger:
    """Log everything to logs/bot.log (rotating); echo to the console when verbose."""
    logger = logging.getLogger(LOGGER_NAME)
    if logger.handlers:  # already configured
        return logger
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    os.makedirs(log_dir, exist_ok=True)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "bot.log"), maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(file_handler)

    if verbose:  # errors are already shown by the CLI, so only echo logs on request
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        logger.addHandler(console)
    return logger

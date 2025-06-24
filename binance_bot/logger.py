import logging
import os

def setup_logger():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # Ensure the logs/ directory exists

    logging.basicConfig(
        filename=os.path.join(log_dir, 'bot.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger()

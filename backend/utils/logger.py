# backend/app/utils/logger.py

import logging
from config import get_settings
def setup_logger() -> logging.Logger:
    settings = get_settings()

    logger = logging.getLogger(settings.app_name)
    logger.setLevel(settings.log_level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

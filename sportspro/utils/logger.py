import logging
import os

LOG_LEVELS = {
    "development": logging.DEBUG,
    "staging": logging.INFO,
    "production": logging.WARNING
}

def setup_logger(name, level="development"):
    """
    Sets up a logger with the specified name and log level.
    
    Parameters:
    - name: Name of the logger.
    - level: Log level. Should be one of 'development', 'staging', or 'production'.
    
    Returns:
    - logger: Configured logger instance.
    """
    if level not in LOG_LEVELS:
        raise ValueError(f"Invalid log level: {level}. Valid levels are 'development', 'staging', 'production'.")

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVELS[level])

    # Create a console handler
    ch = logging.StreamHandler()
    ch.setLevel(LOG_LEVELS[level])

    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add the handler to the logger
    if not logger.hasHandlers():
        logger.addHandler(ch)

    # Optional: Create a file handler if you want to log to a file
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    fh = logging.FileHandler(f'{log_dir}/{name}.log')
    fh.setLevel(LOG_LEVELS[level])
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
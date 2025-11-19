import logging


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evita adicionar handlers duplicados
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger

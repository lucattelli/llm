import logging
import sys


def configure_logger():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "(%(filename)s:%(lineno)d) [%(levelname)s] %(message)s"
    )
    handler.setFormatter(formatter)
    root.addHandler(handler)

    logger = logging.getLogger(__name__)
    logger.debug("Loggers configured...")

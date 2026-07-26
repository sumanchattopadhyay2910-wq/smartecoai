import logging
from pathlib import Path


def setup_logger(app):
    log_dir = Path(app.root_path) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("smarteco")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(log_dir / "app.log")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(handler)
    return logger

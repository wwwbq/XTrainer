import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor

from .constants import RUNNING_LOG
        

class LoggerHandler(logging.Handler):
    r"""
    Logger handler used in Web UI.
    """

    def __init__(self, output_dir: str) -> None:
        super().__init__()
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s", datefmt="%m/%d/%Y %H:%M:%S"
        )
        self.setLevel(logging.INFO)
        self.setFormatter(formatter)

        os.makedirs(output_dir, exist_ok=True)
        self.running_log = os.path.join(output_dir, RUNNING_LOG)
        if os.path.exists(self.running_log):
            os.remove(self.running_log)

        self.thread_pool = ThreadPoolExecutor(max_workers=1)

    def _write_log(self, log_entry: str) -> None:
        with open(self.running_log, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n\n")

    def emit(self, record) -> None:
        if record.name == "httpx":
            return

        log_entry = self.format(record)
        self.thread_pool.submit(self._write_log, log_entry)

    def close(self) -> None:
        self.thread_pool.shutdown(wait=True)
        return super().close()
    
    
def get_logger(name, level=1, save_path=None):
    level_dict = {0: logging.DEBUG, 1: logging.INFO, 2: logging.WARNING}
    
    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s][%(levelname)s] %(message)s"
    )
    
    logger = logging.getLogger(name)
    
    logger.setLevel(level_dict[level])

    if save_path:
        file_handler = logging.FileHandler(save_path, "w")
        #file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    # 修改hugging face的logger formatter
    # hf_logger = logging.getLogger("transformers")
    # hf_stream_handler = logging.StreamHandler()
    # hf_logger.addHandler(hf_stream_handler)
    # hf_stream_handler.setFormatter(formatter)
    
    return logger


# def get_logger(name: str) -> logging.Logger:
#     r"""
#     Gets a standard logger with a stream hander to stdout.
#     """
#     formatter = logging.Formatter(
#         fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s", datefmt="%m/%d/%Y %H:%M:%S"
#     )
#     handler = logging.StreamHandler(sys.stdout)
#     handler.setFormatter(formatter)

#     logger = logging.getLogger(name)
#     logger.setLevel(logging.INFO)
#     logger.addHandler(handler)

#     return logger


def reset_logging() -> None:
    r"""
    Removes basic config of root logger. (unused in script)
    """
    root = logging.getLogger()
    list(map(root.removeHandler, root.handlers))
    list(map(root.removeFilter, root.filters))

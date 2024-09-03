import os
import random
import subprocess
import sys
from enum import Enum, unique

from src import entry
from llamafactory.api.app import run_api
from llamafactory.chat.chat_model import run_chat
from llamafactory.eval.evaluator import run_eval
from llamafactory.extras.env import VERSION, print_env
from llamafactory.extras.logging import get_logger
from llamafactory.extras.misc import get_device_count
from llamafactory.train.tuner import export_model, run_exp

logger = get_logger(__name__)


@unique
class Command(str, Enum):
    API = "api"
    CHAT = "chat"
    ENV = "env"
    EVAL = "eval"
    EXPORT = "export"
    TRAIN = "train"
    WEBDEMO = "webchat"
    WEBUI = "webui"
    VER = "version"
    HELP = "help"


def main():
    command = sys.argv.pop(1)
    if command == Command.API:
        run_api()
    elif command == Command.CHAT:
        run_chat()
    elif command == Command.ENV:
        print_env()
    elif command == Command.EVAL:
        run_eval()
    elif command == Command.EXPORT:
        export_model()
    elif command == Command.TRAIN:
        force_torchrun = os.environ.get("FORCE_TORCHRUN", "0").lower() in ["true", "1"]
        if force_torchrun or get_device_count() > 1:
            master_addr = os.environ.get("MASTER_ADDR", "127.0.0.1")
            master_port = os.environ.get("MASTER_PORT", str(random.randint(20001, 29999)))
            logger.info("Initializing distributed tasks at: {}:{}".format(master_addr, master_port))
            subprocess.run(
                (
                    "torchrun --nnodes {nnodes} --node_rank {node_rank} --nproc_per_node {nproc_per_node} "
                    "--master_addr {master_addr} --master_port {master_port} {file_name} {args}"
                ).format(
                    nnodes=os.environ.get("NNODES", "1"),
                    node_rank=os.environ.get("RANK", "0"),
                    nproc_per_node=os.environ.get("NPROC_PER_NODE", str(get_device_count())),
                    master_addr=master_addr,
                    master_port=master_port,
                    file_name=entry.__file__,
                    args=" ".join(sys.argv[1:]),
                ),
                shell=True,
            )
        else:
            run_exp()

    else:
        raise NotImplementedError("Unknown command: {}".format(command))


if __name__ == '__main__':
    sys.exit(main())
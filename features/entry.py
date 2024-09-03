from typing import TYPE_CHECKING, Any, Dict, List, Optional

from llamafactory.train.callbacks import CustomLogCallback
from llamafactory.hparams import get_train_args
#from llamafactory.train import TaskEngine
from llamafactory.train.dpo import run_dpo
from llamafactory.train.kto import run_kto
from llamafactory.train.ppo import run_ppo
from llamafactory.train.pt import run_pt
from llamafactory.train.rm import run_rm
from llamafactory.train.sft import run_sft

if TYPE_CHECKING:
    from transformers import TrainerCallback


def run_exp(args: Optional[Dict[str, Any]] = None, callbacks: List["TrainerCallback"] = []) -> None:
    model_args, data_args, training_args, finetuning_args, generating_args = get_train_args(args)
    
    callbacks.append(CustomLogCallback(training_args.output_dir))
    
    # engine_type = "run_" + finetuning_args.stage
    
    # TaskEngine.get(engine_type)(
    #     model_args, data_args, training_args, finetuning_args, generating_args, callbacks
    # )
    if finetuning_args.stage == "pt":
        run_pt(model_args, data_args, training_args, finetuning_args, callbacks)
    elif finetuning_args.stage == "sft":
        run_sft(model_args, data_args, training_args, finetuning_args, generating_args, callbacks)
    elif finetuning_args.stage == "rm":
        run_rm(model_args, data_args, training_args, finetuning_args, callbacks)
    elif finetuning_args.stage == "ppo":
        run_ppo(model_args, data_args, training_args, finetuning_args, generating_args, callbacks)
    elif finetuning_args.stage == "dpo":
        run_dpo(model_args, data_args, training_args, finetuning_args, callbacks)
    elif finetuning_args.stage == "kto":
        run_kto(model_args, data_args, training_args, finetuning_args, callbacks)
    else:
        raise ValueError("Unknown task: {}.".format(finetuning_args.stage))


def launch():
    run_exp()


if __name__ == "__main__":
    launch()

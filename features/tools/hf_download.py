from huggingface_hub import snapshot_download
import os


repo_type = "dataset" # dataset model
repo_id = "liuhaotian/LLaVA-Instruct-150K"
local_dir = "/root/autodl-tmp/LLaVA-Instruct-150K/"

if not os.path.exists(local_dir):
    os.makedirs(local_dir, exist_ok=True)


snapshot_download(repo_id=repo_id, local_dir=local_dir, repo_type=repo_type)
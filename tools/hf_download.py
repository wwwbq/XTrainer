from huggingface_hub import snapshot_download
import sys
# import os
# os.environ['HF_ENDPOINT'] = 'hf-mirror.com'

from datasets import load_dataset
from transformers import AutoModel, AutoModelForCausalLM, AutoModelForSequenceClassification

donwload_type = sys.argv[1]
repo_id = sys.argv[2]
if len(sys.argv) > 3:
    local_dir = sys.argv[3]
else:
    repo = repo_id.split("/")[-1]
    local_dir = f"/data/home/cookieewang/HF_HOME/{repo}"
print(f"{donwload_type}, {repo_id} ------> {local_dir}")

if donwload_type == "dataset":
    snapshot_download(repo_id, local_dir=local_dir, repo_type="dataset")
    #dataset = load_dataset(repo_id, local_dir=local_dir)
    #print(dataset)
else:
    snapshot_download(repo_id, local_dir=local_dir, resume_download=True)
    #model = AutoModelForCausalLM.from_pretrained(local_dir)
    #model = AutoModelForSequenceClassification.from_pretrained(local_dir)
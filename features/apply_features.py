import os
import shutil
import inspect


class FeatureEngine:
    def insert_code(self, code: str, line: int, file_path: str):
        with open(file_path, 'r') as file:
            # 读取文件内容
            content = file.readlines()

        insert_position = line - 1
        content.insert(insert_position, code)

        print(f"insert code to {file_path} at {line}")

        with open(file_path, 'w') as file:
            file.writelines(content)
        

    def delete_code(self):
        pass


    def copy(self, src, target):
        if os.path.isdir(src):
        # 如果 src 是一个目录，则复制整个目录
            try:
                shutil.copytree(src, target)
            except:
                pass
        else:
            shutil.copy2(src, target)


    def replace_code(self, code: str, start_line: int, end_line: int, file_path: str):
        with open(file_path, 'r') as file:
            # 读取文件内容
            content = file.readlines()

        start_index = start_line - 1
        end_index = end_line

        if end_index > len(content):
            end_index = len(content)

        # 替换代码，保持原有缩进
        indent_level = content[start_index].count(' ')
        code = code.replace('\n', '\n' + ' ' * indent_level)
        
        content[start_index: end_index] = code

        with open(file_path, 'w') as file:
            file.writelines(content)

        print(f"replace code in {file_path} from {start_line} to {end_line}")


if __name__ == "__main__":  
    engine = FeatureEngine()

    # cp .vscode -> xfactory/
    # cp configs -> xfactory/
    # cp align.py -> XFactory/src/llamafactory/data/aligner.py
    # cp callback.py -> XFactory/src/llamafactory/train/callbacks.py
    # cp config.py -> XFactory/src/llamafactory/extras/config.py
    # cp registry.py -> XFactory/src/llamafactory/extras/registry.py
    # cp data_args.py -> XFactory/src/llamafactory/hparams/data_args.py
    # cp XFactory/features/dataset_info.json -> XFactory/data/dataset_info.json
    # cp XFactory/features/entry.py -> XFactory/src/entry.py
    # cp XFactory/features/logging.py -> XFactory/src/llamafactory/extras/logging.py
    # cp XFactory/features/parser.py -> XFactory/src/llamafactory/data/parser.py
    # cp XFactory/features/run.py -> XFactory/run.py
    # cp XFactory/features/TODO -> 

    # 把XTranier/features/的所有文件夹复制到XTranier/下
    for root, dirs, files in os.walk('./features'):
        for folder in dirs:
            src = os.path.join(root, folder)
            target = src.replace('./features', './')
            engine.copy(src, target)

    ##### 开始处理文件 #####
    src_root = "./features"

    ##### 处理应该放到XTranier/src/llamafactory/下的文件 #######
    target_root = "./src/llamafactory"
    engine.copy(os.path.join(src_root, "aligner.py"), os.path.join(target_root, 'data/aligner.py'))
    engine.copy(os.path.join(src_root, "callbacks.py"), os.path.join(target_root, 'train/callbacks.py'))
    engine.copy(os.path.join(src_root, "config.py"), os.path.join(target_root, 'extras/config.py'))
    engine.copy(os.path.join(src_root, "parser.py"), os.path.join(target_root, 'hparams/parser.py'))
    engine.copy(os.path.join(src_root, "registry.py"), os.path.join(target_root, 'extras/registry.py'))
    engine.copy(os.path.join(src_root, "logging.py"), os.path.join(target_root, 'extras/logging.py'))
    engine.copy(os.path.join(src_root, "data_args.py"), os.path.join(target_root, 'hparams/data_args.py'))

    #from aligner import _convert_images
    #code = "\n".join(_convert_images.__code__.co_code)
    #code = inspect.getsource(_convert_images)
    #engine.replace_code(code, 36, 46, os.path.join(target_root, 'data/aligner.py'))

    #from callbacks import CustomLogCallback
    #code = inspect.getsource(CustomLogCallback)
    #engine.replace_code(code, 36, 46, os.path.join(target_root, 'train/callbacks.py'))
    engine.insert_code("from copy import deepcopy\n", 1, os.path.join(target_root, 'train/callbacks.py'))



    ##### 处理应该放到XTranier/src/下的文件 #######
    target_root = "./src"
    engine.copy(os.path.join(src_root, "entry.py"), os.path.join(target_root, 'entry.py'))

    ##### 处理应该放到XTranier/下的文件 #######
    target_root = "./"
    engine.copy(os.path.join(src_root, "run.py"), os.path.join(target_root, 'run.py'))
    engine.copy(os.path.join(src_root, "TODO"), os.path.join(target_root, 'TODO'))
    engine.copy(os.path.join(src_root, "requirements.txt"), os.path.join(target_root, 'requirements.txt'))

    ##### 处理应该放到dataset_info #######
    target_root = "./features"
    engine.copy(os.path.join(src_root, "dataset_info.json"), './data/dataset_info.json')


    




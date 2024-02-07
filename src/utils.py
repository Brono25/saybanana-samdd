import os
import shutil




def cleanup():
    tmp_dir = os.environ.get("WORKSPACE_VOLUME")
    for item in os.listdir(tmp_dir):
        item_path = os.path.join(tmp_dir, item)
        if os.path.isdir(item_path) and item.startswith("SAMDD_"):
            shutil.rmtree(item_path)

import os
import shutil


def copy_static_to_public(src_dir_path, dst_dir_path):
    if os.path.exists(dst_dir_path):
        print(f"Deleting directory: {dst_dir_path}")
        shutil.rmtree(dst_dir_path)
    copy_files_recursive(src_dir_path, dst_dir_path)


def copy_files_recursive(src_dir_path, dst_dir_path):
    os.mkdir(dst_dir_path)
    for item in os.listdir(src_dir_path):
        src_path = os.path.join(src_dir_path, item)
        dst_path = os.path.join(dst_dir_path, item)
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            copy_files_recursive(src_path, dst_path)

#!/usr/bin/env python3

import contextlib
import os
import subprocess
import shutil
from glob import glob
from os import path

@contextlib.contextmanager
def cd(new_path):
    """Context manager for changing the current working directory"""
    previous_path = os.getcwd()
    try:
        os.chdir(new_path)
        yield
    finally:
        os.chdir(previous_path)

# these are gross, I'd like a better solution

def clear(dir):
    # note glob will ignore . files, which is desired here
    for file in glob(path.join(dir, "*")):
        if path.isdir(file):
            shutil.rmtree(file)
        else:
            os.remove(file)

def transfer(src_dir, dest_dir):
    src_dir = path.join(src_dir, "")
    dest_dir = path.join(dest_dir, "")

    for file in glob(path.join(src_dir, "*")):
        if path.isdir(file):
            reldir = file.replace(src_dir, "")
            shutil.copytree(file, path.join(dest_dir, reldir))
        else:
            reldir = file.replace(src_dir, "")
            shutil.copy2(file, path.join(dest_dir, reldir))

sha1 = subprocess.check_output(["git", "log", "-n", "1", "--pretty=format:%H"])
sha1 = sha1.decode("ascii")
sha1 = sha1[0:12]

subprocess.check_call(["./generate.py", "public"])
clear("../github/")
transfer("public/", "../github/")

with cd("../github/"):
    subprocess.check_call(["git", "add", "--all"])
    subprocess.check_call(["git", "commit", "-e", "-m", "Update to html-examples:{}".format(sha1)])
    subprocess.check_call(["git", "push"])

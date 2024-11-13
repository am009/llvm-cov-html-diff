import re,os
from dataclasses import dataclass
from bs4 import BeautifulSoup
import argparse
from collections import defaultdict

script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)
parent_dir = os.path.dirname(script_dir)

parser = argparse.ArgumentParser(
    prog="llvm-codecov-diff",
    description="A html diff generator for llvm html coverage reports",
)
# old report folder
parser.add_argument("old")
# new report folder
parser.add_argument("new")
parser.add_argument("out", nargs="?")
args = parser.parse_args()

def diff_main_report(old, new, out):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    return os.system(f'python3 {script_dir}/diff_main_report.py {old} {new} {out}')

def diff_each_file(old, new, out):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    return os.system(f'python3 {script_dir}/diff_each_file.py {old} {new} {out}')

join_index = lambda x: os.path.join(x, "index.html")
diff_main_report(join_index(args.old), join_index(args.new), join_index(args.out))

for root, dirs, files in os.walk(args.old, topdown=False):
   for name in files:
        if name.endswith('index.html'):
           continue
        if name.endswith('.html'):
            old_file = os.path.join(root, name)
            rel_path = os.path.relpath(old_file, args.old)
            new_file = os.path.join(args.new, rel_path)
            result_file = os.path.join(args.out, rel_path)
            if os.path.exists(result_file):
                continue
            result = diff_each_file(old_file, new_file, result_file)
            if result != 0:
                print(f"python3 {script_dir}/diff_each_file.py {old_file} {new_file} {result_file}")

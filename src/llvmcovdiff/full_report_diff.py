import os,sys
from .diff_line_coverage import diff_line_coverage
from .diff_main_report import diff_main_report
import traceback

def diff_full_report(old_path, new_path, out_path):

    join_index = lambda x: os.path.join(x, "index.html")
    try:
        print(f"Processing main report.")
        diff_main_report(join_index(old_path), join_index(new_path), join_index(out_path))
    except:
        traceback.print_exc()
        print(f"Error occurred, to debug or reproduce, run:")
        print(f"python3 -m llvmcovdiff.diff_main_report {join_index(old_path)} {join_index(new_path)} {join_index(out_path)}\n")

    for root, dirs, files in os.walk(old_path, topdown=False):
        for name in files:
            if name.endswith('index.html'):
                continue
            if name.endswith('.html'):
                old_file = os.path.join(root, name)
                rel_path = os.path.relpath(old_file, old_path)
                new_file = os.path.join(new_path, rel_path)
                result_file = os.path.join(out_path, rel_path)
                if os.path.exists(result_file):
                    continue
                try:
                    print(f"Processing: {rel_path}", file=sys.stderr)
                    diff_line_coverage(old_file, new_file, result_file)
                except:
                    traceback.print_exc()
                    print(f"Error occurred, to debug or reproduce, run:")
                    print(f"python3 -m llvmcovdiff.diff_line_coverage {old_file} {new_file} {result_file}\n")

def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog="llvmcovdiff",
        description="A html diff generator for llvm html coverage reports",
    )
    # old report folder
    parser.add_argument("old")
    # new report folder
    parser.add_argument("new")
    parser.add_argument("out")
    args = parser.parse_args()
    diff_full_report(args.old, args.new, args.out)

if __name__ == '__main__':
    main()

# llvm-cov-html-diff

Thanks to https://github.com/Dentosal/llvm-codecov-diff/blob/0352d07e486f75b2dfb8bf2d7eb8a6e948e19106/app.py

## Usage

1. Clone the repo.
2. Use the tool.

```
python full_report_diff.py <old_report_folder> <new_report_folder> <output_report_folder>
```

In generated report from llvm-cov
- There are `index.html` that shows the main status of the coverage.
- There are `xxxx.c.html` or `xxx.h.html` that shows line coverage.

Given two llvm-cov report folder, We generate a new folder that shows the differences.


## FAQ

1. Why some line hit count changed but not highlighted?

For line coverage count, we only highlight those counts that goes from zero to non-zero, or from non-zero to zero.

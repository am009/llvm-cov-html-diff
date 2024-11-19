# llvm-cov-html-diff

This tool allows you to inspect and debug fuzzbench results to know why one fuzzer is better than the other.
- Enable the generation of llvm-cov coverage report.
- Use this tool to diff the report.
- Check the report: Check those lines that is not covered by one fuzzer but covered by the other.

## Usage

1. Install the tool: `pip install llvmcovdiff`
2. Use the tool.

```
python -m llvmcovdiff <old_report_folder> <new_report_folder> <output_report_folder>
```

For example, for a fuzzbench result:

```
python -m llvmcovdiff ./2024-05-13-new-cov/coverage/reports/proj4_proj_crs_to_crs_fuzzer/aflplusplus/ ./2024-05-13-new-cov/coverage/reports/proj4_proj_crs_to_crs_fuzzer/afl/ out3
```

## Develop

```
python3 -m build && python3 -m pip install ./dist/llvmcovdiff-0.0.2.tar.gz
```

<!-- python3 -m twine upload ./dist/* -->

## Details

In generated report from llvm-cov
- There are `index.html` that shows the main status of the coverage.
- There are `xxxx.c.html` or `xxx.h.html` that shows line coverage.

Given two llvm-cov report folder, We generate a new folder that shows the differences.

## FAQ

1. Why some line hit count changed but not highlighted?

For line coverage count, we only highlight those counts that goes from zero to non-zero, or from non-zero to zero.

## Others

Thanks to https://github.com/Dentosal/llvm-codecov-diff/blob/0352d07e486f75b2dfb8bf2d7eb8a6e948e19106/app.py

Tested on python 3.10 pip 24.2:

```
beautifulsoup4==4.12.2
```

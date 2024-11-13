import os
from bs4 import BeautifulSoup

def diff_line_coverage(old_path, new_path, out_path):

    def preprocess(data: str):
        return data

    with open(old_path, "r") as f:
        old_html = BeautifulSoup(preprocess(f.read()), features="html.parser")

    with open(new_path, "r") as f:
        new_html = BeautifulSoup(preprocess(f.read()), features="html.parser")

    def remove_all_expansion_view(old_html):
        for div in old_html.find_all("div", {"class": "expansion-view"}):
            div.decompose()

    remove_all_expansion_view(old_html)
    remove_all_expansion_view(new_html)

    old_lines = old_html.find_all("tr")
    new_lines = new_html.find_all("tr")

    old_headers = [td.text.strip() for td in old_lines[0].find_all("td")]
    new_headers = [td.text.strip() for td in new_lines[0].find_all("td")]
    assert old_headers == new_headers, "Headers do not match"
    headers = old_headers

    def parse_count(count: str) -> int:
        if count.endswith('M'):
            return int(float(count[:-1]) * 1_000_000)
        elif count.endswith('k'):
            return int(float(count[:-1]) * 1_000)
        return int(count)

    def to_sized(number):
        number = float(number)
        for unit in ['','K','M']:
            if abs(number) < 1000.0:
                return f"{int(number)}{unit}"
            number /= 1000.0
        return f"{int(number)}B"

    def extract(line) -> tuple[dict[str, int]]:
        cells = line.find_all("td")
        assert len(cells) == len(
            headers
        ), "Number of cells does not match number of headers"

        line_no = None
        source = None
        line_data = {}
        for i, (header, column) in enumerate(zip(headers, cells)):
            header = header.strip()
            if header == 'Line':
                line_no = int(column.text.strip())
            elif header == 'Count':
                if len(column.text.strip()) == 0:
                    line_data['Count'] = None
                else:
                    line_data['Count'] = parse_count(column.text.strip())
            elif header == 'Source (jump to first uncovered line)' or header == 'Source':
                line_data['Source'] = column.text.strip()
            else:
                assert False, f"Unknown header: {header}"
        return line_no, line_data

    old_datas = []
    new_datas = []
    for result_list, lines in zip([old_datas, new_datas], [old_lines, new_lines]):
        for line in lines[1:]:
            line_no, line_data = extract(line)
            result_list.append((int(line_no), line_data['Count'], line_data['Source']))
    assert len(old_datas) == len(new_datas), "Number of lines do not match"

    def get_color(old_count, new_count):
        old_count = 0 if old_count == 0 else 1
        new_count = 0 if new_count == 0 else 1
        if old_count == new_count:
            return "color: #ccc;"
        elif old_count < new_count:
            return "color: red;"
        else:
            return "color: blue;"

    html = """
    <html><head>
    <style>
    body {
        font-family: monospace;
    }
    table {
        border: 1px solid black;
        border-collapse: collapse;
        width: 100%;
    }
    th,td {
        border: 1px solid black;
        padding: 2px;
    }
    </style>
    </head><body>
    """
    html += "<table><thead>"
    # line no is same
    html += f"<th>{headers[0]}</th>"
    # different count
    html += f'<th>{headers[1]}</th>'
    # same source
    html += f'<th>{headers[2]}</th>'
    html += "</thead><tbody>"
    for old_data, new_data in zip(old_datas, new_datas):
        old_line_no, old_count, old_source = old_data
        new_line_no, new_count, new_source = new_data
        assert old_line_no == new_line_no, "Line numbers do not match"
        assert old_source == new_source, "Source code does not match"
        no_count = False
        if old_count is None:
            no_count = True
            assert new_count is None, "Count is not None"
        
        html += f'<td style="font-weight: bold; font: monospace;">{old_line_no}</td>'
        if no_count:
            html += f'<td style="font-weight: bold; font: monospace;"></td>'
        else:
            html += f'<td style="font-weight: bold; font: monospace; { "" if no_count else get_color(old_count, new_count) }"> {to_sized(old_count)} &rarr; {to_sized(new_count)} </td>'
        html += f'<td style="font-weight: bold; font: monospace;">{new_source}</td>'
        html += "</tr>"
    html += "</tbody></table></body></html>"

    if out_path is None:
        print(html)
    else:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w") as f:
            f.write(html)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        prog="llvm-srccov-diff",
        description="A html diff generator for llvm-cov detailed line coverage reports",
    )
    # old report html
    parser.add_argument("old")
    # new report html
    parser.add_argument("new")
    parser.add_argument("out", nargs="?")
    args = parser.parse_args()
    diff_line_coverage(args.old, args.new, args.out)

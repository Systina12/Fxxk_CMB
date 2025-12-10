import os.path
import re
import sys
from typing import List

from rich.console import Console
import pdfplumber


console = Console()
def info(msg):
    console.print(f"[green][INFO][/green] {msg}")
def warn(msg):
    console.print(f"[yellow][WARN][/yellow] {msg}")
def error(msg):
    console.print(f"[bold red][ERROR][/bold red] {msg}")


def load_pdf(path)->List[str]:
    lines=[]
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            for line in text.splitlines():
                line = line.strip()
                if line:
                    lines.append(line)
    return lines

#找出交易行索引
def find_transaction_line(lines: List[str]) -> List[int]:
    indexes = []

    TXN_LINE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}\s+[^-\s]')#行首日期+空格+非-（规避2077-07-10 -- 2077-12-10）

    for index, line in enumerate(lines):
        if not line:
            continue
        if TXN_LINE_RE.match(line):
            indexes.append(index)

    return indexes





if __name__ == "__main__":
    paths=[]
    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            paths.append(arg)
            info("检测到路径： {}".format(arg))
        else:
            error("路径无效： {}".format(arg))



    for path in paths:
        lines = load_pdf(path)
        TXN_indexes = find_transaction_line(lines)
        TXN_lines = []
        for index in TXN_indexes:
            TXN_lines.append(lines[index])
        print(TXN_lines)
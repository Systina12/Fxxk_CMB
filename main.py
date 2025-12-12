import csv
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

def parse_transaction_line(line: str) -> List[str]:

    parts = line.split()

    # 只取前 6 列，多余的丢给 counterparty
    if len(parts) > 6:
        parts = parts[:5] + [' '.join(parts[5:])]

    # 不足 6 列补空
    while len(parts) < 6:
        parts.append("")

    return parts


def write_csv(path: str, rows: List[List[str]]):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "date",
            "currency",
            "amount",
            "balance",
            "summary",
            "counterparty"
        ])
        writer.writerow([
            "记账日期",
            "货币",
            "交易金额",
            "联机余额",
            "交易摘要",
            "对手信息"
        ])
        writer.writerows(rows)






if __name__ == "__main__":
    if len(sys.argv) < 2:
        error("未检测到路径，请在参数传入路径，或者直接把文件拖放到程序图标上")
    try:
        paths=[]
        for arg in sys.argv[1:]:
            if os.path.isfile(arg):
                paths.append(arg)
                info("检测到路径： {}".format(arg))
            else:
                error("路径无效： {}".format(arg))

        for path in paths:
            csv_path = os.path.splitext(path)[0] + ".csv"
            if os.path.exists(csv_path):
                warn("检测到 {} 已存在，继续处理将覆盖此文件！".format(csv_path))
                input("按回车确认......")
            lines = load_pdf(path)
            TXN_indexes = find_transaction_line(lines)

            rows = []
            for index in TXN_indexes:
                row = parse_transaction_line(lines[index])
                rows.append(row)

            write_csv(csv_path, rows)

            info(f"已输出 CSV：{csv_path}")


    except Exception as err:
        error(err)


    input("按回车退出......")
import re
from jinja2 import Environment, FileSystemLoader
from constants import *

# Указываем папку с шаблонами
ENV = Environment(loader=FileSystemLoader('.'))


def kali(variants=None, menu=None, text=None):
    return f"{LIGHT_CYAN}┌─[{DARK_GRAY}{text}{LIGHT_CYAN}]\n" \
           f"{LIGHT_CYAN}├──({LIGHT_BLUE}{variants}{LIGHT_CYAN})-[{RESET}{BOLD}{menu}{LIGHT_CYAN}]\n" \
           f"└─{LIGHT_BLUE}${RESET} "


def line_before(blank_line=True):
    text = "\n┌" + "─" * 50 + "┐"
    if blank_line:
        print(text)
    else:
        print(text.strip())


def line_after(blank_line=True):
    text = "└" + "─" * 50 + "┘\n"
    if blank_line:
        print(text)
    else:
        print(text.strip())


def main():
    while True:
        menu = (
            f"  {LIGHT_YELLOW}1 | {YELLOW} Подсчет рыбы \n"
            f"  {LIGHT_YELLOW}0 | {YELLOW} Выход \n"
        )

        print(menu)

        # /2/3/4/5/6/7/8/9/l/g/a/f/./0
        choice = input(kali('1./0', '~/Settings', "Выбери"))
        if choice == '1':
            print(f"ℹ️  Подсчет рыбы:\n")
            fish_calc()

        elif choice == '0':
            print(f"ℹ️  Exit")
            exit(1)
        else:
            print(f"ℹ️  NO_SUCH_OPTION")


def fish_calc():
    global ENV
    print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
    messages = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        messages.append(line)

    message = "\n".join(messages) + "\n"

    pattern = r'i_\d+ .*\(\d+\)'
    results = re.findall(pattern, message)
    calc = {
        "huge": [],
        "big": [],
        "small": [],
    }
    stats = {
        "huge": {"count": 0, "total": 0},
        "big": {"count": 0, "total": 0},
        "small": {"count": 0, "total": 0},
        "all": {"count": 0, "total": 0},
    }
    for result in results:
        # print(result)
        pattern = r'(i_\d+) (.*)\((\d+)\)'
        m = re.match(pattern, result)
        # print(m[3])
        item = {"name": m[2], "count": m[3]}
        if "Огромн" in result:
            calc["huge"].append(item)
            stats["huge"]["count"] += int(item["count"])
        elif "Больш" in result:
            calc["big"].append(item)
            stats["big"]["count"] += int(item["count"])
        elif "Мелк" in result:
            calc["small"].append(item)
            stats["small"]["count"] += int(item["count"])

    stats["small"]["total"] = stats["small"]["count"] * 200
    stats["big"]["total"] = stats["big"]["count"] * 300
    stats["huge"]["total"] = stats["huge"]["count"] * 400

    stats["all"]["total"] = stats["small"]["total"] + stats["big"]["total"] + stats["huge"]["total"]
    stats["all"]["count"] = stats["small"]["count"] + stats["big"]["count"] + stats["huge"]["count"]

    template = ENV.get_template("calc.tpl")
    output = '\n' + '─' * 50 + '\n'

    output += template.render(calc=calc, stats=stats)

    output += '\n' + '─' * 50 + '\n'

    print(output)


if __name__ == '__main__':
    main()

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
            f"  {LIGHT_YELLOW}2 | {YELLOW} Подсчет рыбы (прогресс) \n"
            f"  {LIGHT_YELLOW}0 | {YELLOW} Выход \n"
        )

        print(menu)

        # /3/4/5/6/7/8/9/l/g/a/f/./0
        choice = input(kali('1/2/./0', '~/Settings', "Выбери"))
        if choice == '1':
            print(f"ℹ️  Подсчет рыбы:\n")
            fish_calc()

        elif choice == '2':
            print(f"ℹ️  Подсчет рыбы - разница:\n")
            fish_calc_two()

        elif choice == '0':
            print(f"ℹ️  Exit")
            exit(1)
        else:
            print(f"ℹ️  NO_SUCH_OPTION")


def get_message(prefix):
    print(f"{prefix}\nEnter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
    messages = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        messages.append(line)

    message = "\n".join(messages) + "\n"
    return message


def calc_stats_fish(message):
    pattern = r'i_\d+ .*\(\d+\)'
    results = re.findall(pattern, message)
    calc = {
        "huge": {},
        "big": {},
        "small": {},
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
        name = m[2]
        count = int(m[3])
        item = {"name": name, "count": count}
        if "Огромн" in result:
            calc["huge"][name] = item
            stats["huge"]["count"] += count
        elif "Больш" in result:
            calc["big"][name] = item
            stats["big"]["count"] += count
        elif "Мелк" in result:
            calc["small"][name] = item
            stats["small"]["count"] += count

    stats["small"]["total"] = stats["small"]["count"] * 200
    stats["big"]["total"] = stats["big"]["count"] * 300
    stats["huge"]["total"] = stats["huge"]["count"] * 400

    stats["all"]["total"] = stats["small"]["total"] + stats["big"]["total"] + stats["huge"]["total"]
    stats["all"]["count"] = stats["small"]["count"] + stats["big"]["count"] + stats["huge"]["count"]

    return calc, stats


def fish_calc():
    global ENV
    message = get_message("")

    calc, stats = calc_stats_fish(message)

    template = ENV.get_template("fish_calc.tpl")
    output = '\n' + '─' * 50 + '\n'

    output += template.render(calc=calc, stats=stats)

    output += '\n' + '─' * 50 + '\n'

    print(output)


def fish_calc_two():
    message = get_message("Message1:")
    calc, stats = calc_stats_fish(message)
    message1 = get_message("Message2:")
    calc1, stats1 = calc_stats_fish(message1)

    diff_stats = {}
    diff_calc = {}

    for key, item in stats1.items():
        d = {"cur": item}
        if key in stats:
            d["prev"] = stats[key]
        else:
            d["prev"] = {"count": 0, "total": 0}

        d["diff"] = {
            "count": d["cur"]["count"] - d["prev"]["count"],
            "total": d["cur"]["total"] - d["prev"]["total"]
        }
        diff_stats[key] = d
        if key in calc1:
            diff_calc[key] = {}
            for key1, item in calc1[key].items():
                d = {"name": key1, "cur": item["count"], "prev": 0}
                if key in calc:
                    if key1 in calc[key]:
                        d["prev"] = calc[key][key1]["count"]
                d["diff"] = d["cur"] - d["prev"]
                diff_calc[key][key1] = d

    for key, item in stats.items():
        if key not in diff_stats:
            d = {"prev": item}
            d["cur"] = {"count": 0, "total": 0}
            d["diff"] = {
                "count": d["cur"]["count"] - d["prev"]["count"],
                "total": d["cur"]["total"] - d["prev"]["total"]
            }
            diff_stats[key] = d
            if key in calc:
                diff_calc[key] = {}
                for key1, item in calc[key].items():
                    d = {"name": key1, "cur": 0, "prev": 0}
                    if key1 in calc[key]:
                        d["prev"] = calc[key][key1].count

                    d["diff"] = d["cur"] - d["prev"]
                    diff_calc[key][key1] = d


    template = ENV.get_template("fish_calc.tpl")

    output = '\n' + '─' * 50 + '\n'
    output += '\n' + '─' * 20 + "Message1" + '─' * 20 + '\n'

    output += template.render(calc=calc, stats=stats)

    output += '\n' + '─' * 20 + "Message2" + '─' * 20 + '\n'

    output += template.render(calc=calc1, stats=stats1)

    output += '\n' + '─' * 20 + "Diff" + '─' * 20 + '\n'

    # template = ENV.get_template("fish_calc_two.tpl")
    # output += template.render(calc=calc, calc1=calc1, stats=stats, stats1=stats1)
    template = ENV.get_template("fish_calc_diff.tpl")
    output += template.render(calc=diff_calc, stats=diff_stats)

    output += '\n' + '─' * 50 + '\n'

    print(output)

if __name__ == '__main__':
    main()

import fishing

def prepare():
    prev = ""
    checked = []

    with open('data/fish_test_raw.txt', 'r', encoding='utf-8') as file:
        for line in file:
            # Убираем символ перевода строки в конце
            cur = line.strip()

            if (cur == "Отличный улов!" or cur == "Ты достаешь пустой крючок. Рыба наелась и уплыла.") and prev != "":
                checked.append(prev)
            prev = cur

    f = open('data/fish_test_data.txt', 'w+')
    f.write("\n".join(checked))
    f.close()

class Event:
    def __init__(self, text: str):
        self.raw_text = text
        self.buttons = []

def test():
    with open('data/fish_test_data.txt', 'r', encoding='utf-8') as file:
        for line in file:
            event = Event(line.strip())
            click = fishing.check_fish(event)
            if not click:
                print(event.raw_text)


if __name__ == '__main__':
    test()
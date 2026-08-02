from telethon.sync import TelegramClient, events

import re

stats = {"fights": []}

fight_stats = {}


def init_fs(message):
    global stats, fight_stats

    pattern = r'\n(.*?) \d+/\d+💚'
    results = re.findall(pattern, message)
    for result in results:
        fight_stats[result] = {"max": 0, "total": 0}

    fight_stats["enemy"] = message.splitlines()[-1]
    # print(stats)
    print(fight_stats)


def parse_step(message):
    global fight_stats

    for player in fight_stats:
        # print(player)
        pattern = re.compile(player.replace("[", '\[') + ' бьет .* на (\d+)')
        results = pattern.findall(message)
        # print(results)
        for result in results:
            if fight_stats[player]["max"] < int(result):
                fight_stats[player]["max"] = int(result)

            fight_stats[player]["total"] += int(result)

    print(fight_stats)


def main(name="", api_id="", api_hash=""):
    client = TelegramClient(name, api_id, api_hash)

    @client.on(events.NewMessage(chats='@ForestSpirits_bot', incoming=True))
    async def my_new_message(event):
        global stats, fight_stats
        if event.raw_text.startswith("Поздравляем с успешным завершением"):
            # TODO шаблон для рендера как в dl/calc.py
            print(stats)
            stats = {"fights": []}
        if event.raw_text == "Группа вступает в бой!":
            # print(fight_stats)
            if len(fight_stats) > 0:
                stats["fights"].append(fight_stats)
                fight_stats = {}

        if event.raw_text.startswith("Начинается сражение!"):
            print("Начинается сражение! ⚔️Против: " + event.raw_text.splitlines()[-1])
            init_fs(event.raw_text)

        if event.raw_text.startswith("Ход "):
            print(event.raw_text.splitlines()[0])
            parse_step(event.raw_text)

    @client.on(events.MessageEdited(chats='@ForestSpirits_bot'))
    async def my_message_edited(event):
        pass

    with client:
        client.run_until_disconnected()


if __name__ == '__main__':
    init_fs("")
    parse_step("")

from telethon.sync import TelegramClient, events

import utils
import random
import asyncio
import sqlite3
import re

sqlite_create_swarms_table_query = '''CREATE TABLE IF NOT EXISTS  swarms(
    id         INTEGER
        primary key,
    created_at TEXT default CURRENT_TIMESTAMP,
    init_data  TEXT,
    tag        TEXT,
    title      TEXT,
    count      INTEGER,
    total      INTEGER
);'''

sqlite_create_swarm_reports_table_query = '''CREATE TABLE IF NOT EXISTS swarm_reports (
    swarm_id INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    data TEXT
);'''

sqlite_insert_swarm_into_swarms_table_query = '''INSERT INTO swarms(id, init_data) 
SELECT {}, '{}' 
WHERE NOT EXISTS(SELECT 1 FROM swarms WHERE id = {});'''

sqlite_insert_into_swarm_reports_table_query = '''INSERT INTO swarm_reports(user_id, current, data) 
SELECT {}, datetime('now'), '{}';'''

sqlite_connection = sqlite3.connect('sqlite_dl.db')
cursor = sqlite_connection.cursor()
cursor.execute(sqlite_create_swarms_table_query)
cursor.execute(sqlite_create_swarm_reports_table_query)

messages = [
    # "Пoплавок cкрылся пoд водoй. Tяни быcтреe.",
]

first_words = [
    "Kлюeт",
    "Клюeт",
    "Kлюёт",
    "Клюет",
    "Клюёт",
    "Kлюет",
]

last_words = [
    "Tяни",
    "Тяни",
    "Подсeкaй",
    "Подсекай",
    "Tащи",
    "Тащи",
    "Тaщи",
    "Taщи",
    "Подcекай",
    "Подсекaй",
    "Пoдсeкай",
    "Пoдсекай",
    "Подсекай быстрeе",
    "Нe cпи",
    "Не cпи",
    "Не спи",
    "He спи",
    "Hе cпи",
    "Не зeвай",
    "Тяни быcтpее",
    "Tяни быcтреe",
    "Тяни быстрее",
    "Tяни быстpеe",
    "Не зевай",
]

messages = list(set(messages))


def check_fish(event):
    click = False

    text = event.raw_text
    text = text.replace("Ты закидываешь удочку и наслаждаешься видом.\n", "").strip()
    print(text)
    for m in messages:
        if text == m:
            click = True
            break

    # endswith = text[:-1]
    # endswith = endswith[-6:]
    # # print(endswith)
    # if endswith == "Не cпи" or endswith == "Не спи" or endswith == "He спи":
    #     click = True

    # last_word = text.rsplit(None, 1)[-1]
    # last_word = last_word[:-1]
    # print(last_word)
    for mm in last_words:
        l = -1 * (len(mm) + 1)
        last_word = text[l:]
        last_word = last_word[:-1]
        if last_word == mm:
            click = True

    first_word = text.split()[0]
    first_word = first_word[:-1]
    # print(first_word)
    for mm in first_words:
        if first_word == mm:
            click = True

    if event.buttons:
        for row in event.reply_markup.rows:
            for btn in row.buttons:
                if btn.text == "🐠 Закинуть удочку":
                    click = True
    return click

init = False

async def worker(name, client):
    if init:
        for i in range(1, 10001):
            message = f"/x_{i}"
            print(f'{name} send message:"{message}"')

            await client.send_message('@ForestSpirits_bot', message)
            random_number = random.randint(50000, 100000)
            await asyncio.sleep(0.001 * random_number)


def main(name="", api_id="", api_hash=""):
    client = TelegramClient(name, api_id, api_hash)

    @client.on(events.NewMessage(chats='@ForestSpirits_bot', incoming=True))
    async def my_new_message(event):
        print(f"New bot message: {event.raw_text}")
        if event.buttons:
            click = False
            for row in event.reply_markup.rows:
                for btn in row.buttons:
                    print(f"Button text: {btn.text}")
                    if btn.text == "🐠Начать":
                        click = True

            if click:
                utils.sleep()
                await event.click(0)

        if "/x_" in event.raw_text:
            result = re.match(r'.*/x_(\d+)\n', event.raw_text)
            if result:
                i = result.group(1)
                print(f"Save swarm info: {i}")
                sql = sqlite_insert_swarm_into_swarms_table_query.format(i, event.raw_text, i)
                sqlite_connection.cursor().execute(sql)

                sqlite_connection.commit()

    @client.on(events.MessageEdited(chats='@ForestSpirits_bot'))
    async def my_message_edited(event):
        # print(f"Edited message: {event.raw_text}")

        click = check_fish(event)

        if click:
            utils.sleep()
            await event.click(0)

    with client:
        utils.sleep()
        worker_task = client.loop.create_task(worker('worker-1', client))
        client.send_message('@ForestSpirits_bot', 'Рыбалка')
        client.run_until_disconnected()


if __name__ == '__main__':
    main("", "", "")

from telethon.sync import TelegramClient, events

import re
import sqlite3
import random
import asyncio


def parse_list(aa, role):
    aaa = aa.split('\n')
    aaa = [x for x in aaa if x]
    list = []
    for x in aaa:
        i = re.match("(.*?)( \[.*\] )?(/p_(\d+))", x)
        if i:
            list.append({"name": i.group(1), "link": i.group(3), "id": i.group(4), "role": role})
    return list


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

sqlite_create_members_table_query = '''CREATE TABLE IF NOT EXISTS swarm_members (
    id INTEGER PRIMARY KEY,
    swarm_id INTEGER,
    name TEXT,
    link TEXT,
    role TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);'''

sqlite_create_members_reports_table_query = '''CREATE TABLE IF NOT EXISTS swarm_members_reports(
    members_id        INTEGER,
    created_at        TEXT default CURRENT_TIMESTAMP,
    experience        INTEGER,
    combat_experience INTEGER,
    data              TEXT,
    head              TEXT,
    body              TEXT,
    right_paw         TEXT,
    left_paw          TEXT,
    acc_1             TEXT,
    acc_2             TEXT,
    acc_3             TEXT,
    pet               TEXT,
    house             TEXT,
    class             TEXT,
    covenant          TEXT,
    place             TEXT
);'''

sqlite_insert_into_members_table_query = '''INSERT INTO swarm_members(id, swarm_id, name, link, role) 
SELECT {}, {}, '{}', '{}', '{}' 
WHERE NOT EXISTS(SELECT 1 FROM swarm_members WHERE id = {});'''

sqlite_insert_into_members_reports_table_query = '''INSERT INTO swarm_members_reports
(members_id, experience, combat_experience, data) 
SELECT {}, {}, {}, '{}';'''

sqlite_update_swarms_table_query = '''UPDATE swarms SET 
    tag = '{}', title = '{}', count = {}, total = {} 
WHERE id = {};'''

sqlite_update_members_reports_table_query = '''UPDATE swarm_members_reports SET 
    head = '{}', body = '{}', 
    right_paw = '{}', left_paw = '{}', 
    acc_1 = '{}', acc_2 = '{}', 
    acc_3 = '{}', pet = '{}', 
    house = '{}', class = '{}', 
    covenant = '{}', place = '{}' 
WHERE members_id = {} and created_at = '{}';'''

sqlite_connection = sqlite3.connect('sqlite_dl.db')
cursor = sqlite_connection.cursor()
cursor.execute(sqlite_create_swarms_table_query)
cursor.execute(sqlite_create_members_table_query)
cursor.execute(sqlite_create_members_reports_table_query)


def init():
    sqlite_select_query = """
        SELECT id, created_at, init_data from swarms"""
    cursor.execute(sqlite_select_query)
    for item in cursor.fetchall():
        raw = item[2]
        parsed = {"tag": "", "title": "", "members": [], "count": 0, "total": 0}

        tag = re.match("^\[(.*)\] (.*) /x", raw)
        if tag:
            parsed["tag"] = tag.group(1)
            parsed["title"] = tag.group(2)

        comp = re.match(".*🐾Состав: (\d+)/(\d+)", raw, re.DOTALL)
        if comp:
            parsed["count"] = comp.group(1)
            parsed["total"] = comp.group(2)

        if "☘️Советники" in raw:
            rr = r'.*🍀Вожак:(.+)☘️Советники:'
        elif "🌱Бойцы" in raw:
            rr = r'️.*🍀Вожак:(.+)🌱Бойцы:'
        else:
            rr = r'️.*🍀Вожак:(.+)🏰Замок'
        a = re.search(rr, raw, re.DOTALL)
        if a:
            arr = parse_list(a.group(1), "leader")
            parsed["members"] = parsed["members"] + arr

        if "🌱Бойцы" in raw:
            rr = r'️.*☘️Советники:(.+)🌱Бойцы:'
        else:
            rr = r'️.*☘️Советники:(.+)🏰Замок'
        a = re.search(rr, raw, re.DOTALL)
        if a:
            parsed["members"] = parsed["members"] + parse_list(a.group(1), "advisor")

        f = re.search(r'️.*🌱Бойцы:(.+)🏰Замок:', raw, re.DOTALL)
        if f:
            parsed["members"] = parsed["members"] + parse_list(f.group(1), "fighter")

        # if int(parsed["count"]) != len(parsed["members"]):
        # if parsed["tag"] == "ЕГС":
        # raw,
        print(raw, "\n", parsed["count"], len(parsed["members"]), parsed)
        # break

        sql = sqlite_update_swarms_table_query.format(parsed["tag"], parsed["title"], parsed["count"], parsed["total"],
                                                      item[0])
        cursor.execute(sql)

        init = False
        if init:
            for m in parsed["members"]:
                sql = sqlite_insert_into_members_table_query.format(m["id"], item[0], m["name"], m["link"], m["role"],
                                                                    m["id"])
                print(sql)
                cursor.execute(sql)

        sqlite_connection.commit()


async def worker(name, client):
    sqlite_select_query = """
            SELECT id, link from swarm_members"""
    cursor.execute(sqlite_select_query)
    for m in cursor.fetchall():
        print(f"Send message to bot: {m[1]}")
        await client.send_message('@ForestSpirits_bot', m[1])
        random_number = random.randint(5000, 10000)
        await asyncio.sleep(0.001 * random_number)


def report(name="", api_id="", api_hash=""):
    client = TelegramClient(name, api_id, api_hash)

    @client.on(events.NewMessage(chats='@ForestSpirits_bot', incoming=True))
    async def my_new_message(event):
        content = event.raw_text
        if "/p_" in content:
            print(f"New bot message: {event.raw_text}")
            members_id, experience, combat_experience = 0, 0, 0
            r = re.match(r'.*/p_(\d+)', content)
            if r:
                members_id = r.group(1)
            r = re.match(r'.*⚜️Суммарный опыт: (\d+)', content, re.DOTALL)
            if r:
                experience = int(r.group(1))
            r = re.match(r'.*🏆Боевой рейтинг: (\d+)', content, re.DOTALL)
            if r:
                combat_experience = int(r.group(1))

            print(members_id, experience, combat_experience)
            if members_id != 0:
                sql = sqlite_insert_into_members_reports_table_query.format(members_id, experience, combat_experience,
                                                                            content)
                cursor.execute(sql)

                sqlite_connection.commit()

    with client:
        client.loop.create_task(worker('worker-1', client))
        client.run_until_disconnected()


def test():
    with open('dl/data/tmp.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)
        members_id, experience, combat_experience = 0, 0, 0
        r = re.match(r'.*/p_(\d+)', content)
        if r:
            members_id = r.group(1)
        r = re.match(r'.*⚜️Суммарный опыт: (\d+)', content, re.DOTALL)
        if r:
            experience = int(r.group(1))
        r = re.match(r'.*🏆Боевой рейтинг: (\d+)', content, re.DOTALL)
        if r:
            combat_experience = int(r.group(1))

        print(members_id, experience, combat_experience)

def parse_attr(content, name):
    pattern = f".*{name}(.*?)\n"
    r = re.match(pattern, content, re.DOTALL)
    if r:
        return r.group(1)
    return ""

def parse_report():
    sqlite_select_query = """
            SELECT members_id, created_at, data from swarm_members_reports"""
    cursor.execute(sqlite_select_query)
    for rr in cursor.fetchall():
        content = rr[2] + "\n"
        experience, combat_experience = 0, 0
        r = re.match(r'.*⚜️Суммарный опыт: (\d+)', content, re.DOTALL)
        if r:
            experience = int(r.group(1))
        r = re.match(r'.*🏆Боевой рейтинг: (\d+)', content, re.DOTALL)
        if r:
            combat_experience = int(r.group(1))

        parsed = {
            "head": parse_attr(content, "Голова: "),
            "body": parse_attr(content, "Тело: "),
            "right_paw": parse_attr(content, "Правая лапа: "),
            "left_paw": parse_attr(content, "Левая лапа: "),
            "acc_1": parse_attr(content, "Аксессуар 1: "),
            "acc_2": parse_attr(content, "Аксессуар 2: "),
            "acc_3": parse_attr(content, "Аксессуар 3: "),
            "pet": parse_attr(content, "Питомец: "),
            "house": parse_attr(content, "🛖Дом: "),
            "class": parse_attr(content, "Класс: "),
            "covenant": parse_attr(content, "Ковенант: "),
            "place": parse_attr(content, "🏆Место: "),
        }

        params = list(parsed.values()) + [rr[0], rr[1]]
        sql = sqlite_update_members_reports_table_query.format(*params)
        # print(sql)
        cursor.execute(sql)
    sqlite_connection.commit()


if __name__ == '__main__':
    parse_report()
    # init()
    # test()
    # report("***", "***", "***")

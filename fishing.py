from telethon.sync import TelegramClient, events
import utils

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
    "Не зевай",
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


def main(name, api_id, api_hash):
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

    @client.on(events.MessageEdited(chats='@ForestSpirits_bot'))
    async def my_message_edited(event):
        # print(f"Edited message: {event.raw_text}")

        click = check_fish(event)

        if click:
            utils.sleep()
            await event.click(0)

    with client:
        utils.sleep()
        client.send_message('@ForestSpirits_bot', 'Рыбалка')
        client.run_until_disconnected()


if __name__ == '__main__':
    main("", "", "")

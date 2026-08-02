from telethon.sync import TelegramClient, events

import re
import utils


def main(name="", api_id="", api_hash="", options=[]):
    client = TelegramClient(name, api_id, api_hash)
    print(options)

    @client.on(events.NewMessage(chats='@ForestSpirits_bot', incoming=True))
    async def my_new_message(event):
        message = event.message.text
        if "дом" in message:
            pattern = r'(/f_\d+)(.*)\((\d+/\d+)\)'
            results = re.findall(pattern, message)
            # await client.send_message('@ForestSpirits_bot', "/f_3")
            for result in results:
                print(result)
                utils.sleep()
                await client.send_message('@ForestSpirits_bot', result[0])

        if "Кормушка" in message:
            if "stroke" in options:
                utils.sleep()
                pattern = r'(/t\d+_\d+) (.*)\d+'
                results = re.findall(pattern, message)
                for result in results:
                    print(result)
                    utils.sleep(1000, 3000)
                    await client.send_message('@ForestSpirits_bot', result[0])
            if "stroll" in options:
                click = False
                idx = 0
                clkIdx = 0
                for row in event.reply_markup.rows:
                    for btn in row.buttons:
                        if btn.text == "🐾Прогулка":
                            print(f"Button text: {btn.text}")
                            click = True
                            clkIdx = idx
                        idx += 1

                if click:
                    utils.sleep(2000, 4000)
                    await event.click(clkIdx)
                else:
                    print(message)
                    print("!!! НЕТ питомцев !!!")

        if "Имя" in message:
            utils.sleep(1000, 3000)
            if event.buttons:
                click = False
                idx = 0
                clkIdx = 0
                for row in event.reply_markup.rows:
                    for btn in row.buttons:
                        if btn.text == "😸Погладить" and "stroke" in options:
                            print(f"Button text: {btn.text}")
                            click = True
                            clkIdx = idx
                        idx += 1

                if click:
                    utils.sleep()
                    await event.click(clkIdx)

    @client.on(events.MessageEdited(chats='@ForestSpirits_bot'))
    async def my_message_edited(event):
        pass

    with client:
        utils.sleep()
        client.send_message('@ForestSpirits_bot', 'Дом')
        client.run_until_disconnected()


if __name__ == '__main__':
    main("", "", "")

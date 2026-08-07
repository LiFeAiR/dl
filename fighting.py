from telethon.sync import TelegramClient, events

import utils
import re

NPP = 1
class BreakLoop(Exception):
    pass


def main(name="", api_id="", api_hash=""):
    client = TelegramClient(name, api_id, api_hash)

    @client.on(events.NewMessage(chats='@ForestSpirits_bot', incoming=True))
    async def my_new_message(event):
        # print(f"{event.raw_text}")
        if event.raw_text == "Начинается бой!":
            global NPP
            print(f"Начинается {NPP} бой!")
            NPP += 1

        pattern = r'💚: (\d+)/(\d+)'
        results = re.findall(pattern, event.raw_text)
        needPower = False
        for result in results:
            # print(result)
            if float(result[0])/float(result[1]) < 0.6:
                print(f"{float(result[0])/float(result[1]):.2f} - похилься!")
                needPower = True

        if event.buttons:
            # utils.sleep()
            # await event.click(0)
            click = False
            idx = -1
            clkIdx = []
            try:
                for row in event.reply_markup.rows:
                    for btn in row.buttons:
                        idx += 1
                        # print(f"Button text: {btn.text}")
                        if btn.text == '⚔️Вылазка':
                            clkIdx.append(idx)
                        if btn.text == '💀 Голем ветвей':
                            continue
                        if "[" in btn.text and "]" in btn.text:
                            clkIdx.append(idx)
                            raise BreakLoop
                        if btn.text == "🧪Полное лечение" and needPower:
                            clkIdx.append(idx)
            except BreakLoop:
                pass
            if len(clkIdx) > 0:
                idx = 0
                for row in event.reply_markup.rows:
                    for btn in row.buttons:
                        if idx in clkIdx:
                            print(f"{btn.text}")
                        idx += 1
                for idx in clkIdx:
                    utils.sleep()
                    await event.click(idx)
            else:
                print("АА три голема")

    @client.on(events.MessageEdited(chats='@ForestSpirits_bot'))
    async def my_message_edited(event):
        # print(f"{event.raw_text}")
        pass

    with client:
        client.run_until_disconnected()


if __name__ == '__main__':
    main("", "", "")

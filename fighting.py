from telethon.sync import TelegramClient, events
import utils

NPP = 1


def main(name, api_id, api_hash):
    client = TelegramClient(name, api_id, api_hash)

    @client.on(events.NewMessage(chats='@ForestSpirits_bot', incoming=True))
    async def my_new_message(event):
        # print(f"{event.raw_text}")
        if event.raw_text == "Начинается бой!":
            global NPP
            print(f"Начинается {NPP} бой!")
            NPP += 1

        if event.buttons:
            utils.sleep()
            await event.click(0)

    @client.on(events.MessageEdited(chats='@ForestSpirits_bot'))
    async def my_message_edited(event):
        # print(f"{event.raw_text}")
        pass

    with client:
        client.run_until_disconnected()


if __name__ == '__main__':
    main("", "", "")

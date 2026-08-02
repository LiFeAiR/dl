from telethon.sync import TelegramClient, events

import re
import asyncio
import random


async def worker(name, client, queue):
    while True:
        job = await queue.get()
        random_number = random.randint(2000, 4000)
        await asyncio.sleep(0.001 * random_number)

        if job["type"] == "click":
            event = job["event"]
            clkIdx = job["clkIdx"]
            message = " ".join(event.message.text.splitlines()[:5])
            print(f'{name} has evalt with message"{message}" and ')

            idx = 0
            for row in event.reply_markup.rows:
                for btn in row.buttons:
                    if idx == clkIdx:
                        print(f"click on button with text: {btn.text}")
                    idx += 1
            await event.click(clkIdx)

        if job["type"] == "message":
            message = job["message"]
            # Send message
            await client.send_message('@ForestSpirits_bot', message)

            print(f'{name} has message "{message}" and send it')

        # Notify the queue that the "work item" has been processed.
        queue.task_done()


def main(name="", api_id="", api_hash="", options=[]):
    client = TelegramClient(name, api_id, api_hash)
    queue = asyncio.Queue()

    @client.on(events.NewMessage(chats='@ForestSpirits_bot', incoming=True))
    async def my_new_message(event):
        message = event.message.text
        if "дом" in message:
            pattern = r'(/f_\d+)(.*)\((\d+/\d+)\)'
            results = re.findall(pattern, message)
            # await client.send_message('@ForestSpirits_bot', "/f_3")
            for result in results:
                print(result)
                job = {"type": "message", "message": result[0]}
                queue.put_nowait(job)

        if "Кормушка" in message:
            if "stroke" in options:
                pattern = r'(/t\d+_\d+) (.*)\d+'
                results = re.findall(pattern, message)
                for result in results:
                    print(result)
                    job = {"type": "message", "message": result[0]}
                    queue.put_nowait(job)
            if "stroll" in options:
                click = False
                idx = 0
                clkIdx = 0
                for row in event.reply_markup.rows:
                    for btn in row.buttons:
                        if btn.text == "🐾Прогулка":
                            # print(f"Button text: {btn.text}")
                            click = True
                            clkIdx = idx
                        idx += 1

                if click:
                    job = {"type": "click", "event": event, "clkIdx": clkIdx}
                    queue.put_nowait(job)
                else:
                    print(message)
                    print("!!! НЕТ питомцев !!!")

        if "Имя" in message:
            if event.buttons:
                click = False
                idx = 0
                clkIdx = 0
                for row in event.reply_markup.rows:
                    for btn in row.buttons:
                        if btn.text == "😸Погладить" and "stroke" in options:
                            # print(f"Button text: {btn.text}")
                            click = True
                            clkIdx = idx
                        idx += 1

                if click:
                    job = {"type": "click", "event": event, "clkIdx": clkIdx}
                    queue.put_nowait(job)

    @client.on(events.MessageEdited(chats='@ForestSpirits_bot'))
    async def my_message_edited(event):
        pass

    with client:
        worker_task = client.loop.create_task(worker('worker-1', client, queue))
        client.send_message('@ForestSpirits_bot', 'Дом')

        client.run_until_disconnected()
        worker_task.cancel()


if __name__ == '__main__':
    main("", "", "", [])

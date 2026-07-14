import random, time


def sleep():
    random_number = random.randint(50, 1000)
    time.sleep(0.001 * random_number)

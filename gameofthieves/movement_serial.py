import logging
import time


class Thief:
    def __init__(self, origin):
        self.position = origin

    def move(self):
        time.sleep(0.001)

        self.position += 1


class ThiefManager:
    @staticmethod
    def move(thieves, i):
        thieves[i].move()


def main(n, num_thiefs, num_epochs):
    thieves = []

    # Create the thieves
    for i in range(n):
        for j in range(num_thiefs):
            thieves.append(Thief(i))

    # Run algorithm
    for k in range(num_epochs):
        for i in range(len(thieves)):
            ThiefManager.move(thieves, i)

    # Simple check if the movements are persisted
    logging.info('Valid: %s' % (thieves[0].position == num_epochs))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    main(n=100, num_thiefs=3, num_epochs=1000)

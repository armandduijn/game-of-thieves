from multiprocessing import Pool, Manager, cpu_count

import logging
import time


class Thief:
    def __init__(self, origin):
        self.position = origin

    def move(self):
        time.sleep(0.0001)

        self.position += 1


class ThiefManager:
    @staticmethod
    def move(thieves, i):
        thief = thieves[i]

        thief.move()

        thieves[i] = thief  # Re-assign to trigger synchronization


def main(n, num_thiefs, num_epochs, processors):
    manager = Manager()
    thieves = manager.list()

    # Create the thieves
    for i in range(n):
        for j in range(num_thiefs):
            thieves.append(Thief(i))

    pool = Pool(processes=processors)

    # Run algorithm
    for k in range(num_epochs):
        pool.starmap(ThiefManager.move, [(thieves, i) for i in range(len(thieves))])

    # Simple check if the movements are persisted
    logging.info('Valid: %s' % (thieves[0].position == num_epochs))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    main(n=100, num_thiefs=3, num_epochs=1000, processors=cpu_count())

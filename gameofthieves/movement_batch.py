from multiprocessing import Process, Queue, cpu_count

import logging
import time
import math


class Thief:
    def __init__(self, origin):
        self.origin = origin
        self.position = origin

    def move(self):
        time.sleep(0.0001)

        self.position += 1


class ThiefManager:
    @staticmethod
    def move(queue, i, n):
        result = []

        for k in range(i, i + n):
            thief = thieves[k]
            thief.move()

            result.append(thief)

        queue.put(result)


def main(n, num_thiefs, num_epochs, processors):
    global thieves
    thieves = []

    # Create the thieves
    for i in range(n):
        for j in range(num_thiefs):
            thieves.append(Thief(i))

    last_thief_index = (len(thieves) - 1)
    batch_size = math.ceil(len(thieves) / processors)  # Calculate the batch size

    # Run algorithm
    for k in range(num_epochs):
        queue = Queue()  # Queue to store processes' results

        i = 0
        processes = []
        for _ in range(processors):
            n = batch_size  # Amount of thieves to move

            if (i + n) > last_thief_index:  # If an index out of bounds occurs
                n = last_thief_index - i  # Only move the remaining thieves

            if n < 0:  # If there are no more thieves to move
                break

            process = Process(target=ThiefManager.move, args=(queue, i, n))
            process.start()

            processes.append(process)  # Store reference for join

            i += batch_size  # Increment the counter

        results = []
        for p in processes:
            p.join()  # Wait for process to finish

            results.append(queue.get())  # Store result

        thieves = [val for sublist in results for val in sublist]  # Flatten list of lists

    # Simple check if the movements are persisted
    for t in thieves:
        if t.origin == 0:  # The thief at node 0 is not necessarily at index 0
            logging.info('Valid: %s' % (t.position == num_epochs))

            break  # There num_thieves per node so prevent multiple log messages


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    main(n=100, num_thiefs=3, num_epochs=1000, processors=cpu_count())

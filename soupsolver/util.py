from time import time

class Timer:
    def __init__(self):
        self.running = False

    def start(self):
        self.time_s = time()
        self.running = True

    def stop(self):
        self.running = False
        self.time_e = time()
        self.runtime = (self.time_e - self.time_s)
        return self.runtime

    def elapsed_time(self):
        if self.running:
            return (time() - self.time_s)
        else:
            return self.runtime
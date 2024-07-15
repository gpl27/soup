from time import time_ns

class Timer:
    def __init__(self):
        self.running = False

    def start(self):
        self.time_s = time_ns()
        self.running = True

    def stop(self):
        self.running = False
        self.time_e = time_ns()
        self.runtime = (self.time_e - self.time_s)/10**9
        return self.runtime

    def elapsed_time(self):
        if self.running:
            return (time_ns() - self.time_s)/10**9
        else:
            return self.runtime
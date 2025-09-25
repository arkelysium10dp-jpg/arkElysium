from time import time



class Timer:
    def __init__(self, seconds, minutes = 0):
        self.time = time()
        self.until = seconds+minutes*60

    def is_late(self):
        print(self.time - time())
        return self.time - time() < 0 - self.until
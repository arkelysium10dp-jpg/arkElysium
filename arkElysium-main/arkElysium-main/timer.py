from time import time



class Timer:
    def __init__(self, seconds, minutes = 0):
        self.time = time()
        self.until = seconds+minutes*60

    def is_late(self):
        return (time() - self.time) >= self.until


if __name__ == "__main__":
    t = Timer(10)
    while not t.is_late():
        input("Time came? Enter")
    cur_time = time()
    print(f"Time came and it's like: {cur_time - (t.time + t.until)}")
    print(f"Init time: {t.time + t.until}"
          f"\n Now Time: {cur_time}")
    print(t.is_late())
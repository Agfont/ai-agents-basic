# tee_logger.py
import sys
import atexit

class Tee:
    def __init__(self, *writers):
        self.writers = writers
    def write(self, data):
        for w in self.writers:
            w.write(data)
    def flush(self):
        for w in self.writers:
            try:
                w.flush()
            except Exception:
                pass

def setup_log(log_path):
    f = open(log_path, "w", encoding="utf-8")
    sys.stdout = Tee(sys.stdout, f)
    atexit.register(lambda: f.close())
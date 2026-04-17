import time

def get_time(start):

    seconds = round(time.time() - start)
    m, s = divmod(seconds, 60)

    return m, s
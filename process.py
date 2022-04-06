from multiprocessing import Queue

output = Queue()

def start_and_wait(processes):

    result = []

    for p in processes:
        p.start()

    for p in processes:
        result.extend(output.get())

    for p in processes:
        p.join()

    return result

def index_div(l, i, n_proc):
    return round(l * i/ n_proc)
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=3)

def get_input():
    return input()

def activation(future):
    result = future.result()
    print('USER SAID ' + str(result))

while True:
    executor.submit(get_input).add_done_callback(activation)
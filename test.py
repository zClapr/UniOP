# import threading
# import time

# def wait_for_event(ev):
#     while True:
#         print('\tTHREAD: This is the thread speaking, we are Waiting for event to start..')
#         ev.wait()
#         print('\tTHREAD:  WHOOOOOO HOOOO WE GOT A SIGNAL  : %s')
#         ev.set()

# e = threading.Event()
# threading.Thread(target=wait_for_event, args=(e,)).start()

# time.sleep(5)
# e.set()

# # while True:
# #     print('MAIN LOOP: still in the main loop..')
# #     time.sleep(10)
# #     print('MAIN LOOP: I just set the flag..')
# #     e.set()
# #     time.sleep(10)
# #     print('MAIN LOOP: ok ready, soon we will repeat the loop..')
# #     time.sleep(2)

###################################

d = {1:2,4:2,3:5}

print(list(d.keys()))
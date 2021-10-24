# from multiprocessing import Process
# import time

# def one():
#     while True:
#         print('USER SAID ' + input())

# def two():
#     while True:
#         print('yreakldsjf')
#         time.sleep(1)

# if __name__ == '__main__':
#     Process(target=one).start()
#     Process(target=two).start()

# # # # # # # # # # # # # # # # # # # # 

# from threading import Thread
# import time

# def loop_console_worker():
#     global user_input
#     while True:
#         user_input = input()

# if __name__ == "__main__":
#     user_input = "original value"
#     Thread(target=loop_console_worker).start()
#     while True:
#         time.sleep(1)
#         print(f"{user_input = }", end='\r')

# # # # # # # # # # # # # # # # # # # # 

# x = 101

# exec('print(x)')
from pyglet import app

user_input = None

def process_cmd(cmd):
    pass

def inputLoop():
    global user_input
    while app.event_loop.is_running:
        user_input = input()
        exec(user_input)
if __name__ == '__main__':
    from threading import Thread
    import pyglet
    from framework.window import mainWindow, screenWidth, screenHeight
    from engine.physics import celestrial_body, cosmos
    from framework.console_handler import inputLoop

    # # # # # # # # # # # # # # # # #
    # # SIMULATION CONFIGURATIONS # #
    # # # # # # # # # # # # # # # # #

    cosmos.play_speed = 1
    window = mainWindow(
        width=int(screenWidth*0.8), height=int(screenHeight*0.8), 
        caption=(__file__.split('/')[-1]), resizable=True, vsync=False
    )

    # # # # # # # # # # # # # # # # #
    # # # # SIMULATION  SETUP # # # #
    # # # # # # # # # # # # # # # # #

    b1 = celestrial_body(150, [110,10,10], [255,0,0], 0, radius=10)
    b2 = celestrial_body(300, [10,110,10], [0,255,0], 1, radius=20)
    b3 = celestrial_body(500, [10,10,110], [0,0,255], 2, radius=30)

    print(r"""
 _   _       _  ___  ____
| | | |_ __ (_)/ _ \|  _ \
| | | | '_ \| | | | | |_) |
| |_| | | | | | |_| |  __/
 \___/|_| |_|_|\___/|_|
        """)
    print('--------------- \n' + 'ACTIVE OBJECTS:')
    for body in cosmos.objects:
        print(
            str(cosmos.objects.index(body)) + ' | '
            + str(body) + ' with a mass of ' + str(body.mass) + ' at ' + str(body.position)
        )
    Thread(target=inputLoop).start()
    
    pyglet.app.run()
else:
    raise(Exception('Illegal action! Unimportable file is only to be executed as main script'))
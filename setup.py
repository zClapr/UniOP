from engine.physics import celestrial_body

baseStarter = 750
b1 = celestrial_body(50, [20,20,0])
b2 = celestrial_body(50, [-20,20,0])
b3 = celestrial_body(50, [0,-20,0])

active = [b1, b2, b3]
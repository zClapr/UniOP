import pyglet

point_list = [18, 61, 59, 149, 328, 204, 305, 284, 3, 197, 25, 107]
ec = int(len(point_list)/2)
batch.add(ec, pyglet.gl.GL_POLYGON, None, ("v2i", point_list), ("c3B", [random.randrange(255)]*(3*ec)))
for i in range(int(len(point_list)/2)):
    p1 = point_list[i*2:2+i*2]
    p2 = point_list[2+i*2:4+i*2]

    if not len(p2):
        p2 = point_list[:2]

    batch.add(ec, pyglet.gl.GL_POINTS, None, ("v2i", point_list), ("c3B", [255]*(3*ec)))

@window.event
def on_draw():
    window.clear()
    batch.draw()
pyglet.app.run()
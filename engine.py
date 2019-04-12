from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

snail = None
points = None
links = None 

def add_snail(sn):
    global snail
    snail = sn

def links_gen(nodes):
    links = []
    for i in range(len(nodes)):
        r, a = nodes[i]
        if r:
            r_ = r + 1
            a_ = a + a // r
            node = r, (a + 1) % (r * 6)
            if node in nodes:
                links.append((i, nodes.index(node)))
            node = r_, a_
            if node in nodes:
                links.append((i, nodes.index(node)))
            node = r_, a_ + 1
            if node in nodes:
                links.append((i, nodes.index(node)))
            if a % r == 0:
                node = r_, (a_ - 1) % (r_ * 6)
                if node in nodes:
                    links.append((i, nodes.index(node)))
        else:
            for a in range(6):
                node = 1, a
                if node in nodes:
                    links.append((i, nodes.index(node)))

    return links

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_POINT_SMOOTH)

    global points, links
    nodes = snail.get_data()[0]
    links = links_gen(nodes)

    max_r = max(map(lambda n: n[0], nodes))
    points = [ortogonal(r, a, max_r) for r, a in nodes]

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0.0, 0.0, 0.0)

    draw_nodes()
    draw_links()

    glutSwapBuffers()

def ortogonal(r, a, max_r):
    if r:
        ang0 = a // r
        ang1 = (ang0 + 2) % 6
        a = (a % r) / (max_r + 1)
        r = r / (max_r + 1)
        x = r * cos(pi / 3 * ang0) + a * cos(pi / 3 * ang1)
        y = r * sin(pi / 3 * ang0) + a * sin(pi / 3 * ang1)
        return (x, y)
    else:
        return (0.0, 0.0)
    

def draw_nodes():
    glPointSize(8)
    glBegin(GL_POINTS)

    glColor3f(1.0, 1.0, 1.0)
    for x, y in points:
        glVertex2d(x, y)

    glEnd()

def draw_links():
    glBegin(GL_LINES)
    
    glColor(1.0, 1.0, 1.0)
    for i, j in links:
        x, y = points[i]
        glVertex2d(x, y)
        x, y = points[j]
        glVertex2d(x, y)

    glEnd()

def simulation_run(argv):
    glutInit(argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(512, 512)
    glutInitWindowPosition(16, 16)
    glutCreateWindow('Snail')
    glutDisplayFunc(display)
    init()
    glutMainLoop()


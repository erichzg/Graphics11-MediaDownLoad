import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 20
    p = mdl.parseFile(filename)
    if p:
        (commands, symbols) = p
        for command in p[0]:
            commandList = command
            if commandList[0] == 'push':
                stack.append( [x[:] for x in stack[-1]] )
            elif commandList[0] == 'pop':
                stack.pop()
            elif commandList[0] == 'move':
                tmp = make_translate(float(commandList[1]), float(commandList[2]), float(commandList[3]))
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
            elif commandList[0] == 'rotate':
                theta = float(commandList[2]) * (math.pi / 180)
                if commandList[1] == 'x':
                    tmp = make_rotX(theta)
                elif commandList[1] == 'y':
                    tmp = make_rotY(theta)
                else:
                    tmp = make_rotZ(theta)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
            elif commandList[0] == 'scale':
                tmp = make_scale(float(commandList[1]), float(commandList[2]), float(commandList[3]))
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
            elif commandList[0] == 'box':
                polygons = []
                add_box(polygons, float(commandList[1]), float(commandList[2]), float(commandList[3]), float(commandList[4]), float(commandList[5]), float(commandList[6]))
                matrix_mult(stack[-1], polygons)
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            elif commandList[0] == 'sphere':
                polygons = []
                add_sphere(polygons, float(commandList[1]), float(commandList[2]), float(commandList[3]), float(commandList[4]), step_3d)
                matrix_mult(stack[-1], polygons)
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            elif commandList[0] == 'torus':
                polygons = []
                add_torus(polygons, float(commandList[1]), float(commandList[2]), float(commandList[3]), float(commandList[4]), float(commandList[5]), step_3d)
                matrix_mult(stack[-1], polygons)
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
            elif commandList[0] == 'line':
                edges = []
                add_edge(edges, float(commandList[1]), float(commandList[2]), float(commandList[3]), float(commandList[4]), float(commandList[5]), float(commandList[6]))
                matrix_mult(stack[-1], edges)
                draw_lines(edges, screen, zbuffer, color)
            elif commandList[0] == 'save' or commandList[0] == 'display':
                if commandList[0] == 'display':
                    display(screen)
                else:
                    save_extension(screen, commandList[1])
    else:
        print "Parsing failed."
        return

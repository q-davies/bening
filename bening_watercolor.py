# made possible through: https://www.youtube.com/watch?v=5bBkBVnrg2g&ab_channel=TheBuffED
# values tweaked a bit, for the most part exactly the same
# might add more later

import cairo, sys, argparse, copy, math, random

float_gen = lambda a, b: random.uniform(a, b)

colors = []
for i in range(7):
    colors.append((float_gen(.5, 1), float_gen(.5, 1), float_gen(.5, 1)))

def octagon(x_orig, y_orig, side):
    x = x_orig
    y = y_orig
    diag = side / math.sqrt(2)

    oct = []

    oct.append((x, y))

    x += side
    oct.append((x, y))

    x += diag
    y += diag
    oct.append((x, y))

    y += side
    oct.append((x, y))

    x -= diag
    y += diag
    oct.append((x, y))

    x -= side
    oct.append((x, y))

    x -= diag
    y -= diag
    oct.append((x, y))

    y -= side
    oct.append((x, y))

    x += diag
    y -= diag
    oct.append((x, y))

    return oct

def deform(shape, iter, vari):
    for i in range(iter):
        for j in range(len(shape)-1, 0, -1):
            midpoint = ((shape[j-1][0] + shape[j][0]) / 2 + float_gen(-vari, vari), (shape[j-1][1] + shape[j][1]) / 2 + float_gen(-vari, vari))
            shape.insert(j, midpoint)
    return shape

def create_picture():
    initial_rand = random.randint(500,5000)

    # args don't serve much of a purpose right now, maybe later
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", default=1000, type=int)
    parser.add_argument("--height", default=1500, type=int)
    parser.add_argument("-i", "--initial", default=initial_rand, type=int)
    parser.add_argument("-d", "--deviation", default=100, type=int)
    parser.add_argument("-bd", "--basedeforms", default=1, type=int)
    parser.add_argument("-fd", "--finaldeforms", default=3, type=int)
    parser.add_argument("-mins", "--minshapes", default=3, type=int)
    parser.add_argument("-maxs", "--maxshapes", default=20, type=int)
    parser.add_argument("-sa", "--shapealpha", default=.01, type=float)
    args = parser.parse_args()

    width, height = args.width, args.height
    initial = args.initial
    deviation = args.deviation

    basedeforms = args.basedeforms
    finaldeforms = args.finaldeforms

    minshapes = args.minshapes
    maxshapes = args.maxshapes

    shapealpha = args.shapealpha

    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    source_r = random.uniform(.1, .7)
    source_g = random.uniform(.1, .7)
    source_b = random.uniform(.1, .7)
    cr.set_source_rgb(source_r, source_g, source_b)
    cr.rectangle(0, 0, width, height)
    cr.fill()

    cr.set_line_width(1)

    for p in range(-int(height*.2), int(height*1.2), 60):
        cr.set_source_rgba(random.choice(colors)[0], random.choice(colors)[1], random.choice(colors)[2], shapealpha)

        shape = octagon(random.randint(-100, width + 100), p, random.randint(100, 300))
        baseshape = deform(shape, basedeforms, initial)

        for j in range(random.randint(minshapes, maxshapes)):
            tempshape = copy.deepcopy(baseshape)
            layer = deform(tempshape, finaldeforms, deviation)

            for i in range(len(layer)):
                cr.line_to(layer[i][0], layer[i][1])
            cr.fill()
    
    ims.write_to_png('pictures/watercolor.png')

#if __name__ == "__main__":
#    main()
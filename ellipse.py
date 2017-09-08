#!/usr/bin/env python3

# Extending the classical rope-and-pencil ellipse drawing technique to more than 2 foci.
# The generic problem is, given a set of 2D points, make a rope loop around them and the tip of a pencil
# and draw a convex smooth curve around the points with this pencil while keeping the loop taught.
#
# For 3 non-collinear foci the resulting curve is a smooth combination of 6 ellipse fragments.


import math
import svgwrite

def distance(F1, F2):
    "Find the distance between two 2D points"
    return math.sqrt( math.pow(F2[0]-F1[0], 2)+ math.pow(F2[1]-F1[1], 2) )

def midpoint(F1, F2):
    "Find the midpoint of two 2D points"
    return ((F1[0]+F2[0])/2, (F1[1]+F2[1])/2)

def draw_ellipse(dwg, F1, F2, d, colour='grey'):
    "Draw a tilted ellipse given two foci and the length of slack part of the rope attached to them"
    C               = midpoint(F1, F2)
    cf              = distance(F1, F2)/2
    tilt_deg        = math.degrees( math.atan2(F2[1]-F1[1], F2[0]-F1[0]) )
    a               = d/2
    b               = math.sqrt( a*a - cf*cf )
        # Here we rotate the coordinates so that inside the SVG group element the major axis of the ellipse is horizontal
    target_group    = dwg.g( stroke=colour, stroke_width='2', fill='none', transform='rotate(%f,%f,%f)' % (tilt_deg, C[0], C[1]) )
    target_group.add( dwg.ellipse( center=C, r=(a,b) ) )
    target_group.add( dwg.circle( center=(C[0]-cf,C[1]), r=5, stroke=F1[2] ) )
    target_group.add( dwg.circle( center=(C[0]+cf,C[1]), r=5, stroke=F2[2] ) )
    dwg.add( target_group )

def draw_ellipsystem(P1, P2, P3, slack=200, filename="hexaellipse.svg", canvas_size=(1000,1000)):
    "Draw a system of 6 ellipses that make up the sought-for smooth convex shape"
    d12             = distance(P1, P2)
    d23             = distance(P2, P3)
    d31             = distance(P3, P1)
    tight_loop      = d12 + d23 + d31
    loop_length     = tight_loop+slack
    dwg             = svgwrite.Drawing(filename=filename, debug=True, size=canvas_size)
    draw_ellipse(dwg, P1, P2, loop_length-d12,      colour=P3[2])
    draw_ellipse(dwg, P1, P2, loop_length-d23-d31,  colour=P3[2])
    draw_ellipse(dwg, P2, P3, loop_length-d23,      colour=P1[2])
    draw_ellipse(dwg, P2, P3, loop_length-d12-d31,  colour=P1[2])
    draw_ellipse(dwg, P3, P1, loop_length-d31,      colour=P2[2])
    draw_ellipse(dwg, P3, P1, loop_length-d12-d23,  colour=P2[2])
    dwg.save()

if __name__ == '__main__':
    P1              = (400, 500, 'red')
    P2              = (600, 400, 'orange')
    P3              = (500, 700, 'green')
    draw_ellipsystem(P1, P2, P3, slack=250)
from turtle import *

class Line:
    def __init__(self):
        self.x = []
        self.y = []

    def start(self):
        return self.x[0], self.y[0]


print 'Loading file'
lines = []
with open('img_test/table_me_small.traj', 'r') as f:
    line = Line()
    for l in f:
        if l.strip() == '-':
            # start new line
            lines.append(line)
            line = Line()
        else:
            # append to curent_line
            x, y = map(int, l.strip().split(','))
            line.x.append(x)
            line.y.append(y)

print "Done loading file. {} lines found".format(len(lines))
print 'Starting to draw'
offset_x, offset_y = 500, 250
speed(0)

for line in lines:
    up()
    start = line.start()
    goto(start[0]-offset_x, start[1]-offset_y)
    down()
    for x, y in zip(line.x, line.y):
        goto(x-offset_x, y-offset_y)

raw_input()

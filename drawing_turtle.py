

# Read the file for coordinates
with open('traj', 'r') as f:
    lines = []
    line = []
    for l in f:
        if l.strip() == '--':
            lines.append(line)
            line = []
        else:
            x, y = map(int, l.strip().split('\t'))
            line.append([x, y])
    lines.append(line)

def plot_main():
    import matplotlib.pyplot as plt
    import numpy as np

    print lines
    plt.figure()
    for line in lines:
        if line != []:
            print line
            a = np.array(line).T
            plt.plot(a[0], a[1])

    plt.show()

def turtle_main():
    from turtle import *

    screensize(1300, 900)
    speed(0)
    offx, offy = -300, -300
    for line in lines:
        if line != []:
            up()
            goto(offx+line[0][0], offy+line[0][1])
            down()
            for x, y in line:
                goto(offx+x, offy+y)


if __name__ == '__main__':
    # plot_main()
    turtle_main()

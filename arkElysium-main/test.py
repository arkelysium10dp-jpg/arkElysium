x, y = 0, 0
width, height = 2, 2
trigger_xy = xt, yt = -1, 0
d = (x-width/2 <= trigger_xy[0] <= x + width/2) & \
        (y-height/2 <= trigger_xy[1] <= y + height/2)
print(d)
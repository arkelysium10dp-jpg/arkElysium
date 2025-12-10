from Object import Object


class Path:
    """
    Used for scripts to determine path for usually EnemyObject

    """

    def __init__(self, subject: Object, destination_points: list[list[int]]):
        self.subject = subject
        self.destination_points = destination_points
        self.dest_ind = 0

    def move(self, speed):
        x, y = self.subject.xy
        dx, dy = self.destination_points[self.dest_ind]
        if [x, y] == [dx, dy]:
            if len(self.destination_points) < self.dest_ind:
                self.dest_ind += 1
            return
        if x > dx:
            x -= speed
        elif x > dx:
            x+= speed
        if y > dy:
            y -= speed
        elif y < dy:
            y += speed
        self.subject.xy = x, y


# path: (494, 204)
# Path( Object(), [[0,0], [2,2]])

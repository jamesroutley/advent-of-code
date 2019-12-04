#!/usr/bin/python3

"""
--- Part Two ---

It turns out that this circuit is very timing-sensitive; you actually need to
minimize the signal delay.

To do this, calculate the number of steps each wire takes to reach each
intersection; choose the intersection where the sum of both wires' steps is
lowest. If a wire visits a position on the grid multiple times, use the steps
value from the first time it visits that position when calculating the total
value of a specific intersection.

The number of steps a wire takes is the total number of grid squares the wire
has entered to get to that location, including the intersection being
considered. Again consider the example from above:

...........
.+-----+...
.|.....|...
.|..+--X-+.
.|..|..|.|.
.|.-X--+.|.
.|..|....|.
.|.......|.
.o-------+.
...........

In the above example, the intersection closest to the central port is reached
after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by the second
wire for a total of 20+20 = 40 steps.

However, the top-right intersection is better: the first wire takes only 8+5+2
= 15 and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30 steps.

Here are the best steps for the extra examples from above:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps

What is the fewest combined steps the wires must take to reach an intersection?
"""

import dataclasses
import fileinput
import typing


@dataclasses.dataclass
class Vector:
    x: int
    y: int

    def add(self, v):
        return Vector(self.x + v.x, self.y + v.y)

    def __eq__(self, other):
        """Define what equality means for this class. Lets us =="""
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        """Define how to hash this class. Lets us put it in a set"""
        return hash((self.x, self.y))


def tupleToVector(t: typing.Tuple[int, int]) -> Vector:
    return Vector(t[0], t[1])


def run():
    lines = []
    for line in fileinput.input():
        lines.append(line)
    intersections = calculate_intersections(lines[0], lines[1])
    return min(
        [
            manhattan_distance(Vector(0, 0), intersection)
            for intersection in intersections
        ]
    )


def calculate_intersections(
    movements_a: str, movements_b: str
) -> typing.List[typing.Tuple[Vector, int, int]]:
    points_a = get_path_points(movements_a)
    points_b = get_path_points(movements_b)

    points_b_set = set(points_b)

    intersections = []
    for point in points_a:
        if point == Vector(0, 0):
            continue
        if point in points_b_set:
            intersections.append(point)
    return intersections


def get_path_points(movements: str) -> typing.List[Vector]:
    path_points: typing.List[Vector] = []
    # All sets of movements start at the central port, which we arbitrarily
    # mark as (0, 0)
    current_position = Vector(0, 0)
    path_points.append(current_position)

    for movement in movements.split(","):
        direction = movement[0]
        distance = int(movement[1:])

        if direction == "R":
            incremental_movement = Vector(1, 0)
        if direction == "L":
            incremental_movement = Vector(-1, 0)
        if direction == "U":
            incremental_movement = Vector(0, 1)
        if direction == "D":
            incremental_movement = Vector(0, -1)

        for _ in range(distance):
            current_position = current_position.add(incremental_movement)
            path_points.append(current_position)

    return path_points


def manhattan_distance(a: Vector, b: Vector) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def _test_get_path_points():
    cases = [
        ("R1", [tupleToVector(v) for v in [(0, 0), (1, 0)]]),
        ("L3", [tupleToVector(v) for v in [(0, 0), (-1, 0), (-2, 0), (-3, 0)]]),
        ("U1,D1", [tupleToVector(v) for v in [(0, 0), (0, 1), (0, 0)]]),
        ("U100", [tupleToVector(v) for v in [(0, i) for i in range(101)]]),
    ]

    for case in cases:
        input = case[0]
        expected = case[1]
        assert get_path_points(input) == expected


def _test_calculate_intersections():
    assert calculate_intersections("R8,U5,L5,D3", "U7,R6,D4,L4") == [
        Vector(6, 5),
        Vector(3, 3),
    ]


def _test_manhattan_distance():
    assert manhattan_distance(Vector(0, 0), Vector(3, 3)) == 6
    assert manhattan_distance(Vector(0, 0), Vector(-3, 3)) == 6
    assert manhattan_distance(Vector(0, 0), Vector(3, -3)) == 6
    assert manhattan_distance(Vector(0, 0), Vector(-3, -3)) == 6


if __name__ == "__main__":
    # _test_get_path_points()
    # _test_calculate_intersections()
    # _test_manhattan_distance()
    print(run())

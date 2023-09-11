# GOAL = 452
# NUMBERS = [3, 7, 8, 9, 25, 75]

# TEST: (8 * 7 - 3) * 9 - 25 = 452
#
# 1: {"total": 8, "operator": None, "tuple": None, "used": [8]}
# 2: {"total": 7, "operator": None, "tuple": None, "used": [7]}
# 3: {"total": 3, "operator": None, "tuple": None, "used": [3]}
# 4: {"total": 56, "operator": *, "tuple": (7, 8), "used": [7, 8]}
# 5: {"total": 53, "operator": -, "tuple": (56, 3), "used": [3, 7, 8]}
# 6: {"total": 477, "operator": *, "tuple": (53, 9), "used": [3, 7, 8, 9]}
# 7: {"total": 452, "operator": -, "tuple": (477, 25), "used": [3, 7, 8, 9, 25]}
#
# 56: ((8, 7), *),
# 53: ((56, 3), -)
# 477: ((53, 9), *)
# 452: ((477, 25), -)
#
numbers_found = set()
solutions = {}


class Node:
    pair: tuple

    def __init__(self, total=0, operator=None, pair=None, numbers_left=(), parent=None, substitute="left"):
        self.total = total
        self.operator = operator
        self.pair = pair
        self.numbers_left = numbers_left
        self.substitute = substitute
        self.parent = parent

    def _get_numbers_left(self, number_to_remove):
        numbers_left = list(self.numbers_left)
        numbers_left.remove(number_to_remove)
        return tuple(numbers_left)

    def _make_neighbour(self, total, operator, pair, number):
        return Node(
            total=total,
            operator=operator,
            pair=pair,
            numbers_left=self._get_numbers_left(number)
        )

    def get_neighbours(self):
        neighbours = []
        for number in self.numbers_left:

            if self.total != 0 and (self.total % number == 0):
                neighbours.append(self._make_neighbour(self.total / number, "/", (self.total, number), number))
            if self.total != 0:
                neighbours.append(self._make_neighbour(self.total * number, "*", (self.total, number), number))

                new_neighbour = self._make_neighbour(number - self.total, "-", (number, self.total), number)
                new_neighbour.substitute = "right"
                neighbours.append(new_neighbour)

            neighbours.append(self._make_neighbour(self.total + number, "+", (self.total, number), number))
            neighbours.append(self._make_neighbour(self.total - number, "-", (self.total, number), number))
        return neighbours

    def __eq__(self, other):
        if not isinstance(other, Node):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return (self.total == other.total and self.operator == other.operator and
                self.pair == other.pair and self.numbers_left == other.numbers_left and
                self.substitute == other.substitute)

    def __hash__(self):
        # necessary for instances to behave sanely in dicts and sets.
        return hash((self.total, self.operator, self.pair, self.numbers_left))

    def __repr__(self):
        return f"[ total: {self.total}, operator: {self.operator}, " \
               f"pair: {self.pair}, numbers left: {self.numbers_left}, " \
               f"substitute: {self.substitute}]"


def bfs(goal, root):
    queue = [root]
    explored = [root]
    while queue:
        v = queue.pop()
        if v.total == goal:
            return v
        for w in v.get_neighbours():
            if w not in explored:
                explored.append(w)

                w.parent = v
                queue.append(w)


def make_expression(found_node):
    expression = ""
    node = found_node
    nodes = []
    while node:
        nodes.append(node)
        node = node.parent

    nodes.reverse()
    for node in nodes:
        if node.total != 0:
            if node.pair[0] == 0 or node.pair[1] == 0:
                expression += f"{node.total}"
            else:
                if node.substitute == "left":
                    expression += f" {node.operator} {node.pair[1]}"
                    expression = f"({expression})"
                else:
                    expression = f"{node.pair[0]} {node.operator} {expression})"
                    expression = f"({expression})"
    expression = expression[0:len(expression) - 1]
    return expression


# # 8 * 4
# number_to_find = 32
# start = Node(numbers_left=(2, 4, 8))

# # (75 / 25) * 3
# number_to_find = 9
# start = Node(numbers_left=(3, 25, 75))

# # 3 - ((((-75 + 25) * 9) + 8) - 7))
# number_to_find = 452
# start = Node(numbers_left=(3, 7, 8, 9, 25, 75))

# # ((3 - ((-100 - 75) + 7))) * 50) / 25
# number_to_find = 342
# start = Node(numbers_left=(3, 7, 25, 50, 75, 100))

# #  8 - ((((-100 + 9) * 50) / 25) * 2))
# number_to_find = 372
# start = Node(numbers_left=(2, 8, 9, 25, 50, 100))

#  2 - ( ( ( - 10 * 9 ) * 8 ) + 7 ) = 715
number_to_find = 951
start = Node(numbers_left=(6, 9, 25, 50, 75, 100))

goal_found = bfs(number_to_find, start)
if goal_found:
    print(f"goal found: {make_expression(goal_found)}")
else:
    print("No goal found!")

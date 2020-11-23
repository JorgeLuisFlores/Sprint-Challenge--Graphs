from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
reverse_direction = {"n": "s", "s": "n", "e": "w", "w": "e"}


def dft_recursive(graph, cur_room, prev=None, direction=None, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []
    exits = {}

    if cur_room in visited:
        return

    for exit_direction in cur_room.get_exits():
        exits[exit_direction] = "?"

    graph[cur_room.id] = exits
    visited.add(cur_room)

    if prev is not None:
        path.append(direction)
        graph[prev.id][direction] = cur_room.id
        graph[cur_room.id][reverse_direction[direction]] = prev.id

    for exit_ in cur_room.get_exits():
        if graph[cur_room.id][exit_] == "?":
            if cur_room.get_room_in_direction(exit_) not in visited:
                _prev = cur_room
                _dir = exit_
                _cur_room = cur_room.get_room_in_direction(exit_)
                dft_recursive(graph, _cur_room, _prev, _dir, visited, path)
                path.append(reverse_direction[exit_])

    return path


traversal_path = dft_recursive({}, player.current_room)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

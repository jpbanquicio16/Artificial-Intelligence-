STUDENT_ID = 'a1884969'
DEGREE = 'UG'

from collections import deque
import heapq
import sys
from itertools import count


def parse_map_from_string(map_str):
    lines = [line.strip() for line in map_str.strip().split('\n') if line.strip()]

    rows, cols = map(int, lines[0].split())

    start_i, start_j = map(int, lines[1].split())
    end_i, end_j = map(int, lines[2].split())
    start = (start_i - 1, start_j - 1)  
    end = (end_i - 1, end_j - 1)

    grid = []
    for line in lines[3:]:
        row = []
        for val in line.split():
            if val == 'X':
                row.append('X')  
            else:
                row.append(int(val))  
        grid.append(row)

    return rows, cols, start, end, grid


def parse_map_from_file(filename):
    with open(filename, 'r') as file:
        map_str = file.read()
    return parse_map_from_string(map_str)


def get_adj(i, j, grid):
    adj_nodes = []
    rows = len(grid)
    cols = len(grid[0])
    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    for p1, p2 in directions: 
        n1 = i + p1 
        n2 = j + p2
        if 0 <= n1 < rows and 0 <= n2 < cols: 
            if (grid[n1][n2] != 'X'): 
                adj_nodes.append((n1, n2))

    return adj_nodes

def reconstruct_path(parent, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent[current] 
    path.append(start)  
    return path[::-1]  

def BFS(start, end, grid): 
    rows = len(grid)
    cols = len(grid[0])

    visited = set()
    parent = dict()
    queue = deque([start])

    visit_count = [[0 for _ in range(cols)] for _ in range(rows)]
    first_visit = [[None for _ in range(cols)] for _ in range(rows)]
    last_visit = [[None for _ in range(cols)] for _ in range(rows)]
    counter = 1

    queue.append(start)
    first_visit[start[0]][start[1]] = counter
    visit_count[start[0]][start[1]] = 1

    while queue: 
        curr = queue.popleft()
        c1, c2 = curr 
        last_visit[c1][c2] = counter 
        counter += 1

        if curr == end: 
            return reconstruct_path(parent, start, end), visit_count, first_visit, last_visit
        
        for n1, n2 in get_adj(c1, c2, grid): 
                if (n1,n2) not in visited: 
                    visited.add((n1,n2))
                    parent[(n1,n2)] = (c1,c2)
                    queue.append((n1, n2))

                    visit_count[n1][n2] = 1

                if first_visit[n1][n2] is None: 
                    first_visit[n1][n2] = counter
                    counter += 1

    return None, visit_count, first_visit, last_visit

def overlay_path(map_matrix, path):
    path_set = set(path)
    output = []

    for i, row in enumerate(map_matrix):
        line = []
        for j, cell in enumerate(row):
            if (i, j) in path_set:
                line.append('*')
            else:
                line.append(str(cell))  
        output.append(' '.join(line))  

    return '\n'.join(output)





def print_matrix(matrix, obstacles):
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[0])):
            if obstacles[i][j] == 'X':
                row.append('X')
            elif matrix[i][j] is None:
                row.append('.')
            else:
                row.append(str(matrix[i][j]))
        print(' '.join(row))


def cost_function(curr, neighbour, grid):
    i, j = curr
    ni, nj = neighbour

    curr_state = int(grid[i][j])
    n_state = int(grid[ni][nj])

    return 1 + max(0, (n_state - curr_state))

def UCS(start, end, grid):
    counter_gen = count()  

    rows = len(grid)
    cols = len(grid[0])

    visited = set()
    parent = dict()

    heap = []
    cost_check = {start: 0}

    tie = next(counter_gen)
    heapq.heappush(heap, (0, tie, start))  

    visit_count = [[0 for _ in range(cols)] for _ in range(rows)]
    first_visit = [[None for _ in range(cols)] for _ in range(rows)]
    last_visit = [[None for _ in range(cols)] for _ in range(rows)]
    counter = 1

    first_visit[start[0]][start[1]] = counter
    visit_count[start[0]][start[1]] += 1

    while heap:
        curr_cost, _, curr = heapq.heappop(heap)
        i, j = curr

        if curr == end:
            return reconstruct_path(parent, start, end), visit_count, first_visit, last_visit

        if curr in visited:
            continue
        visited.add(curr)
        last_visit[i][j] = counter
        counter += 1

        for n1, n2 in get_adj(i, j, grid):  # UDLR enforced by get_adj
            neighbor = (n1, n2)
            new_cost = curr_cost + cost_function(curr, neighbor, grid)

            if neighbor not in cost_check or new_cost < cost_check[neighbor]:
                cost_check[neighbor] = new_cost
                parent[neighbor] = curr

                tie = next(counter_gen)
                heapq.heappush(heap, (new_cost, tie, neighbor))

                if first_visit[n1][n2] is None:
                    first_visit[n1][n2] = counter
                    visit_count[n1][n2] += 1

    return None, visit_count, first_visit, last_visit


def manhattan_dist(a,b): 
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def euclidean_dist(a,b):
    return((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def a_star(start, end, grid, heuristic_function):
    from itertools import count
    counter_gen = count()  

    rows = len(grid)
    cols = len(grid[0])

    visited = set()
    parent = {}

    heap = []
    cost_check = {start: 0}

    visit_count = [[0 for _ in range(cols)] for _ in range(rows)]
    first_visit = [[None for _ in range(cols)] for _ in range(rows)]
    last_visit = [[None for _ in range(cols)] for _ in range(rows)]
    counter = 1

    f_cost = heuristic_function(start, end)
    tie = next(counter_gen)
    heapq.heappush(heap, (f_cost, tie, 0, start)) 

    first_visit[start[0]][start[1]] = counter
    visit_count[start[0]][start[1]] += 1

    while heap:
        _, _, curr_cost, curr = heapq.heappop(heap)
        i, j = curr

        if curr == end:
            return reconstruct_path(parent, start, end), visit_count, first_visit, last_visit

        if curr in visited:
            continue
        visited.add(curr)
        last_visit[i][j] = counter
        counter += 1

        for n1, n2 in get_adj(i, j, grid):
            neighbor = (n1, n2)
            new_cost = curr_cost + cost_function(curr, neighbor, grid)

            if neighbor not in cost_check or new_cost < cost_check[neighbor]:
                cost_check[neighbor] = new_cost
                parent[neighbor] = curr
                f = new_cost + heuristic_function(neighbor, end)
                tie = next(counter_gen)
                heapq.heappush(heap, (f, tie, new_cost, neighbor))

                if first_visit[n1][n2] is None:
                    first_visit[n1][n2] = counter
                    visit_count[n1][n2] += 1

    return None, visit_count, first_visit, last_visit


def main():
    mode = sys.argv[1]
    map_path = sys.argv[2]
    algorithm = sys.argv[3].lower()  # normalize to lowercase
    heuristic = sys.argv[4].lower() if algorithm == 'astar' else None

    rows, cols, start, goal, grid = parse_map_from_file(map_path)

    if algorithm == 'bfs':
        path, visits, first_visit, last_visit = BFS(start, goal, grid)
    elif algorithm == 'ucs':
        path, visits, first_visit, last_visit = UCS(start, goal, grid)
    elif algorithm == 'astar':
        if heuristic == 'manhattan':
            heuristic_function = manhattan_dist
        elif heuristic == 'euclidean':
            heuristic_function = euclidean_dist
        else:
            print("Invalid heuristic.")
            return

        path, visits, first_visit, last_visit = a_star(start, goal, grid, heuristic_function)
    else:
        print("Invalid algorithm.")
        return

    if mode == 'release':
        print("null" if path is None else overlay_path(grid, path))
    elif mode == 'debug':
        print("path:")
        print("null" if path is None else overlay_path(grid, path))

        print("\n#visits:")
        print_matrix(visits, grid)

        print("\nfirst visit:")
        print_matrix(first_visit, grid)

        print("\nlast visit:")
        print_matrix(last_visit, grid)


if __name__ == "__main__":
    main()

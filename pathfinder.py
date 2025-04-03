from collections import deque

STUDENT_ID = 'a1884969'
DEGREE = 'UG'

def parse_map_from_string(map_str): 
    return [line.strip().split() for line in map_str.strip().split('\n')]

def get_adj(i, j, map_matrix):
    adj_nodes = []
    rows = len(map_matrix)
    cols = len(map_matrix[0])
    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    for p1, p2 in directions: 
        n1 = i + p1 
        n2 = j + p2
        if 0 <= n1 < rows and 0 <= n2 < cols: 
            if (map_matrix[n1][n2] != 'X'): 
                adj_nodes.append((n1, n2))

    return adj_nodes

def reconstruct_path(parent, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent[current]  # move one step back
    path.append(start)  # add the start at the end
    return path[::-1]  # reverse the path to go start → goal

def BFS(start, end, map): 
    rows = len(map)
    cols = len(map[0])

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
        
        for n1, n2 in get_adj(c1, c2, map): 
                if (n1,n2) not in visited: 
                    visited.add((n1,n2))
                    parent[(n1,n2)] = (c1,c2)
                    queue.append((n1, n2))

                if first_visit[n1][n2] is None: 
                    first_visit[n1][n2] = counter
                    counter += 1

    return None, visit_count, first_visit, last_visit

def overlay_path(map_matrix, path):
    path_set = set(path)  # for faster lookup
    output = []

    for i, row in enumerate(map_matrix):
        line = []
        for j, cell in enumerate(row):
            if (i, j) in path_set:
                line.append('*')
            else:
                line.append(cell)
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

def test_bfs_with_string_map():
    map_str = '''
    1 1 1 1 1
    1 X 1 X 1
    1 X 1 X 1
    1 1 1 X 1
    X X 1 1 1
    '''
    grid = parse_map_from_string(map_str)
    start = (0, 0)
    goal = (4, 4)
    path, visits, first_visit, last_visit = BFS(start, goal, grid)

    if path is None:
        print("path:\nnull")
    else:
        print("path:")
        print(overlay_path(grid, path))

    print("\n#visits:")
    print_matrix(visits, grid)

    print("\nfirst visit:")
    print_matrix(first_visit, grid)

    print("\nlast visit:")
    print_matrix(last_visit, grid)

test_bfs_with_string_map()

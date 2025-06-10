import sys
import numpy as np
import pandas as pd


STUDENT_ID = 'a1884969' # Nice :)  
DEGREE = 'UG'

class Node:
    def __init__(self, point, label, axis, split_val):
        self.point = point
        self.label = label
        self.axis = axis
        self.split_val = split_val
        self.left = None
        self.right = None

def build_tree(X, y, depth):
        if X.shape[0] == 0:
            return None
        k = X.shape[1]
        axis = depth % k

        # when there's exactly one point, make a leaf
        if X.shape[0] == 1:
            return Node(X[0], y[0], axis, X[0][axis])

        # sort on the current axis and pick the median
        sorted_idx = np.argsort(X[:, axis])
        X_sorted = X[sorted_idx]
        y_sorted = y[sorted_idx]
        mid = X_sorted.shape[0] // 2

        # this is the median point/node
        median_point = X_sorted[mid]
        median_label = y_sorted[mid]
        node = Node(median_point, median_label, axis, median_point[axis])

        # **IMPORTANT** – split the sorted arrays *around* the median,
        # excluding index mid itself
        left_X  = X_sorted[:mid]
        left_y  = y_sorted[:mid]
        right_X = X_sorted[mid+1:]
        right_y = y_sorted[mid+1:]

        node.left  = build_tree(left_X,  left_y,  depth + 1)
        node.right = build_tree(right_X, right_y, depth + 1)
        return node



def search_nn(node, query, best_dist, best_label):
    if node is None:
        return best_dist, best_label
    # Check this node
    dist = np.linalg.norm(query - node.point)
    if dist < best_dist:
        best_dist = dist
        best_label = node.label

    axis = node.axis
    # Choose branch to explore first
    if query[axis] <= node.split_val:
        near, away = node.left, node.right
    else:
        near, away = node.right, node.left

    best_dist, best_label = search_nn(near, query, best_dist, best_label)
    # Check if we need to explore the away branch
    if abs(query[axis] - node.split_val) < best_dist:
        best_dist, best_label = search_nn(away, query, best_dist, best_label)
    return best_dist, best_label


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 nn_kdtree.py [train] [test] [dimension]")
        sys.exit(1)

    train_path = sys.argv[1]
    test_path = sys.argv[2]
    init_pos = int(sys.argv[3])

    # Read data (auto-detect delimiter)
    df_train = pd.read_csv(train_path,
                       delim_whitespace=True,
                       header=None,
                       skiprows=1)
    df_test  = pd.read_csv(test_path,
                       delim_whitespace=True,
                       header=None,
                       skiprows=1)

    X_train = df_train.iloc[:, :-1].values
    y_train = df_train.iloc[:, -1].values
    X_test = df_test.values

    k = X_train.shape[1]
    axis = init_pos % k

    # Looking at nodes left due to odd id (Keshi song god im turning performative) number
    sorted_idx = np.argsort(X_train[:, axis])
    X_sorted = X_train[sorted_idx]
    y_sorted = y_train[sorted_idx]
    mid = X_sorted.shape[0] // 2
    median_val = X_sorted[mid][axis]

    left_count = np.sum(X_train[:, axis] <= median_val)
    right_count = np.sum(X_train[:, axis] > median_val)

    # Print split info
    print('.' * init_pos + 'l' + str(left_count))
    print('.' * init_pos + 'r' + str(right_count))

    # Build K-d tree
    root = build_tree(X_train, y_train, init_pos)

    # Predict (Read da future) on test set
    for point in X_test:
        _, label = search_nn(root, point, float('inf'), None)
        print(int(label))


if __name__ == '__main__':
    main()

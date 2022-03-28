import numpy as np
import sys

arguments = sys.argv  # get arguments
map_file = open(arguments[1])

list_of_node = [[]]


class Node:
    # constructer of a node
    def __init__(self, x, y, altitude, parent=None, cost_so_far=0, distance_to_end=0):
        self.x = x
        self.y = y
        self.altitude = altitude
        self.cost_so_far = cost_so_far
        self.distance_to_end = distance_to_end
        self.parent = parent
        self.up = None
        self.down = None
        self.left = None
        self.right = None

    def get_cost(self, parent):  # calculate cost of two adjacent nodes
        if int(parent.altitude) - int(self.altitude) > 0:
            return 1
            #return 1 + int(self.altitude) - int(parent.altitude)
        else:
            return 1 + int(self.altitude) - int(parent.altitude)
            #return 1
    def get_euclidean(self, end):
        # use square root and pythagorean theorem
        X_square = np.power(self.x - end.x, 2)
        Y_square = np.power(self.y - end.y, 2)
        self.distance_to_end = np.sqrt(X_square + Y_square)

    def get_manhattan(self, end):
        # manhattan distance is the absolute value of the difference between x and y
        self.distance_to_end = np.abs(self.y - end.y) + np.abs(self.x - end.x)


def read_map(file, node_list, order=''):  #
    n = 1  # the first line, because the coordinate or the map isn't start from 0, so set it as 1 at start
    for row in file:
        if n == 1:  # the first line of the file indicates the size of the map
            row_num = int(row.split()[0])
            col_num = int(row.split()[1])

        elif n == 2:  # the second line of the file indicates the start point
            start_row = int(row.split()[0]) - 1  # in our program the index and coordinates are 0 based
            start_col = int(row.split()[1]) - 1

        elif n == 3:  # the third line indicates the destination
            end_row = int(row.split()[0]) - 1
            end_col = int(row.split()[1]) - 1

        else:  # from the third line,is the map itself
            c = 0  # colum number
            row = row.replace('\n', '')
            #print(row)
            row = row.split()
            for i in row:  # input the points as node object one by one
                node_list[n - 4].append(Node(altitude=i, x=n - 4, y=c, parent=None, cost_so_far=0, distance_to_end=0))
                c += 1

        if n > 3 and n < row_num + 3:  # if the current line belongs to map area, append a new line into the list
            node_list.append([])
        n = n + 1
    #
    for p in range(row_num):  # connect the nodes
        for q in range(col_num):  # set distance if appliable
            if order == "euclidean":
                node_list[p][q].get_euclidean(node_list[end_row][end_col])
            elif order == "manhattan":
                node_list[p][q].get_manhattan(node_list[end_row][end_col])

            if p > 0 and node_list[p - 1][q].altitude != 'X':  # If it's not in the firs row and the above node isn't X#
                node_list[p][q].up = node_list[p - 1][q]

            if p < row_num - 1 and node_list[p + 1][q].altitude != 'X':
                node_list[p][q].down = node_list[p + 1][q]

            if q > 0 and node_list[p][q - 1].altitude != 'X':
                node_list[p][q].left = node_list[p][q - 1]

            if q < col_num-1 and node_list[p][q + 1].altitude != 'X':
                node_list[p][q].right = node_list[p][q + 1]

    return start_row, start_col, end_row, end_col


def test_destination(node, end_node):  # test whether the current node is the end node
    if node.x == end_node.x and node.y == end_node.y:
        return True
    else:
        return False

def insert_node(node, fringe):  # function to insert node
    fringe.append(node)


def expand(node, fringe, closed):  # show all reachable nodes of current node
    son = []
    # Check if the reachable node can be put into the fringe
    if node.up != None and node.up not in fringe and node.up not in closed:
        son.append(node.up)
    if node.down != None and node.down not in fringe and node.down not in closed:
        son.append(node.down)
    if node.left != None and node.left not in fringe and node.left not in closed:
        son.append(node.left)
    if node.right != None and node.right not in fringe and node.right not in closed:
        son.append(node.right)

    for s in son:  # record the total cost of the parent node
        #print(s.x, s.y, "'s parent node is: ", node.x, node.y)
        s.parent = node
        s.cost_so_far = s.get_cost(s.parent) + s.parent.cost_so_far  # The cost from the start point to the current point
    return son

def get_g(node):
    if node.parent != None:
        return node.get_cost(node.parent)
    else:
        return 0

def get_g_h(node):
    if node.parent != None:
        #return node.get_cost(node.parent)
        return node.cost_so_far + node.distance_to_end
    else:
        return node.distance_to_end

def bfs(end_point, start_point, node_list):
    closed = []
    fringe = []
    insert_node(start_point, fringe)

    while True:
        if len(fringe) == 0:  # visited all available nodes
            print("null")
            return

        temp = fringe[0]
        if test_destination(temp, end_point):  # if reaches the destination
            #print("finished")
            asterisk(temp)
            print_answer(node_list)
            return
        if temp not in closed:
            closed.append(temp)
            for i in expand(temp, fringe, closed):
                insert_node(i, fringe)
        fringe.remove(fringe[0])

def ucs(end_point, start_point, node_list):
    closed = []
    fringe = []
    insert_node(start_point, fringe)

    while True:
        if len(fringe) == 0:
            print("null")
            return

        fringe.sort(key=get_g)  # sort the fringe according to g()
        temp = fringe[0]
        if test_destination(temp, end_point):
            #print("finished")
            asterisk(temp)
            print_answer(node_list)
            return
        if temp not in closed:
            #print("visit: ", temp.x, temp.y)
            closed.append(temp)
            for i in expand(temp, fringe, closed):
                insert_node(i, fringe)
        fringe.remove(fringe[0])


def astar(end_point, start_point, node_list):
    closed = []
    fringe = []
    insert_node(start_point, fringe)

    while True:
        if len(fringe) == 0:
            print("null")
            return
        fringe.sort(key=get_g_h)  # sort to ascending order

        temp = fringe[0]
        #print("temp 是 fringe[0]： ",temp)
        #print(get_g_h(temp))
        if test_destination(temp, end_point):
            #print("finished")
            asterisk(temp)
            print_answer(node_list)
            return
        if temp not in closed:
            #print("visit: ", temp.x, temp.y)
            closed.append(temp)
            for i in expand(temp, fringe, closed):
                insert_node(i, fringe)
        fringe.remove(fringe[0])


def asterisk(node):  # trace back the path from the end to start
    node.altitude = '*'
    if node.parent == None:
        return
    else:
        asterisk(node.parent)


def print_answer(node_list):
    for line in node_list:  # reset the path for each new line
        path = ''

        for k in line:
            path += k.altitude + ' '
        path = path[:len(path)-1]
            #print("实际输出的字符串的长度",len(path))
        #for k in range(len(line)):
         #   if(k ==len(node_list)-1 ):
          #      path += line[k].altitude
           # else:
                #path += line[k].altitude + ' '
        print(path)


if len(arguments) > 3:
    start_x, start_y, end_x, end_y = read_map(map_file, list_of_node, arguments[3]) # load the map and calculate the distance if necessary
    astar(list_of_node[end_x][end_y], list_of_node[start_x][start_y], list_of_node)

elif arguments[2] == "bfs":
    start_x, start_y, end_x, end_y = read_map(map_file, list_of_node)
    bfs(list_of_node[end_x][end_y], list_of_node[start_x][start_y], list_of_node)

elif arguments[2] == "ucs":
    start_x, start_y, end_x, end_y = read_map(map_file, list_of_node)
    ucs(list_of_node[end_x][end_y], list_of_node[start_x][start_y], list_of_node)

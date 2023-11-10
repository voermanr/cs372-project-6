import heapq
import sys
import json
import math  # If you want to use math.inf for infinity

# TODO refactor this code based on specific problem

# This class is taken from an implementation I used in Algorithms in 2023.
# I believe the original source was either provided by the instructor, or
# based on slides.
class Graph:

    # construct the graph
    def __init__(self, vertices):
        self.V = vertices
        # adjacency matrix
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]
        # list of edges
        self.edges = []

    # set the adjacency matrix
    def set_adj_matrix(self, adjmat):

        # function to add an edge to edge list
        def addEdge(self, u, v, w):
            if w > 0:
                self.edges.append([u, v, w])

                # function to add edges for an adj matrix

        def setEdges(self, m):
            for i in range(len(m)):
                for j in range(len(m[i])):
                    addEdge(self, i, j, m[i][j])
            return

        self.graph = adjmat
        setEdges(self, adjmat)

    # pretty print the path
    def printPath(self, dist):
        print("vertex\tdistance")
        for node in range(self.V):
            print(node, "\t", dist[node])


    # Dijkstra's single source shortest path algorithm
    def dijkstra(self, src):
        # Do some setup for our datastructures
        dist = [sys.maxsize] * self.V
        pred = [None] * self.V

        # InitSSSP(s)
        dist[src] = 0

        # Insert(s, 0)
        src_vertex = (dist[src], src)
        priority_queue = [src_vertex]

        # while the priority queue is not empty
        while priority_queue:

            # u←ExtractMin()
            u = heapq.heappop(priority_queue)[1]

            # for all edges u→v
            for u_v in self.edges:
                if u_v[0] == u:
                    v = u_v[1]
                    w = u_v[2]

                    # if u→v is tense
                    if dist[u] + w < dist[v]:

                        # Relax u→v
                        dist[v] = dist[u] + w
                        pred[v] = u
                        target_vertex = (dist[v], v)

                        # if v is in the priority queue DecreaseKey(v, dist(v)) else Insert(v, dist(v))
                        #
                        #   Python doesn't have a clean way to do the DecreaseKey() method on
                        #   a Priority Queue implemented from heapq, so we just rely on the heap
                        #   invariant of the PQ to take care of the difference between DecreaseKey()
                        #   and Insert().
                        heapq.heappush(priority_queue, target_vertex)

        # print path and return it
        self.printPath(dist)
        return dist

def dijkstras_shortest_path(routers, src_ip, dest_ip):
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    to search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.31.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3,
            "if_prefix": "en"
        },
        ...

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.
    """

    # TODO Write me!
    # need to get number of vertices and make and
    # adjacency matrix for that

    # parse routers

    pass


# ------------------------------
# DO NOT MODIFY BELOW THIS LINE
# ------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)


def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")


def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)


def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)


if __name__ == "__main__":
    sys.exit(main(sys.argv))


def router_dict_to_adj_m(routers) -> [[int]]:
    """
    parses a json router dictionary and returns an adjacency list
    """
    _adj_m = [[int]]

    return _adj_m


def sort_router_ip_addresses(routers) -> list:
    return sorted(routers.keys())
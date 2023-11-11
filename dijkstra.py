import heapq
import sys
import json
import math  # If you want to use math.inf for infinity
import netfuncs as nf


DEBUG = 0


def vprint(*values):
    if DEBUG:
        print(*values)


# This class is taken from an implementation I used in Algorithms in 2023.
# I believe the original source was either provided by the instructor, or
# based on slides.
class Graph:

    # construct the graph
    def __init__(self, adjacency_matrix):
        self.V = len(adjacency_matrix)
        # adjacency matrix
        self.graph = [[0 for _ in range(self.V)]
                      for _ in range(self.V)]
        # list of edges
        self.edges = []

        self.set_adj_matrix(adjacency_matrix=adjacency_matrix)

    # set the adjacency matrix
    def set_adj_matrix(self, adjacency_matrix):

        # function to add an edge to edge list
        def add_edge(self, u, v, w):
            if w > 0:
                self.edges.append([u, v, w])

        # function to add edges for an adj matrix
        def set_edges(self, m):
            for i in range(len(m)):
                for j in range(len(m[i])):
                    add_edge(self, i, j, m[i][j])
            return

        self.graph = adjacency_matrix
        set_edges(self, adjacency_matrix)

    # pretty print the path
    def print_path(self, dist):
        vprint("vertex\tdistance")
        for node in range(self.V):
            vprint(node, "\t", dist[node])

    # Dijkstra's single source shortest path algorithm
    def dijkstra(self, src: int):
        # Do some setup for our datastructures
        dist = [math.inf] * self.V
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
        # self.print_path(dist)
        return pred

    @staticmethod
    def shortest_path(dest, prev):
        current_node = dest
        src = prev.index(None)
        path = []

        while current_node != src:
            path.append(current_node)
            current_node = prev[current_node]

        path.append(src)

        return path[::-1]


class RouterGraph(Graph):
    """
    A bad class that contains routerish functions and extends Graph.
    """
    @staticmethod
    def router_dict_to_adj_m(routers) -> [[int]]:
        """
        parses a json router dictionary and returns an adjacency list
        :param routers: JSON routers
        :return: adjacency_matrix, router_keys_sorted
        """

        length = len(routers)

        adjacency_matrix = [
            [0 for _ in range(length)] for _ in range(length)
        ]

        routers_keys_sorted = RouterGraph.sort_router_ip_addresses(routers)

        for i, router_ip in enumerate(routers_keys_sorted):
            router_connections = routers[router_ip]['connections'].items()

            for connection_ip, connection_attributes in router_connections:
                j = routers_keys_sorted.index(connection_ip)
                adjacency_matrix[i][j] = connection_attributes['ad']

        return adjacency_matrix, routers_keys_sorted

    @staticmethod
    def sort_router_ip_addresses(routers) -> list:
        return sorted(routers.keys())

    @staticmethod
    def find_routers_for_ip_pair(routers, src_ip, dest_ip) -> tuple:
        return (nf.find_router_for_ip(routers=routers, ip=src_ip),
                nf.find_router_for_ip(routers=routers, ip=dest_ip))


def dijkstras_shortest_path(routers, src_ip, dest_ip) -> list:
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

    src_router, dest_router = RouterGraph.find_routers_for_ip_pair(routers, src_ip, dest_ip)

    adj_mat, router_keys_sorted = RouterGraph.router_dict_to_adj_m(routers=routers)
    graph = Graph(adj_mat)

    src, dest = router_keys_sorted.index(src_router), router_keys_sorted.index(dest_router)

    prev = graph.dijkstra(src=src)

    ip_path = [router_keys_sorted[i] for i in Graph.shortest_path(dest=dest, prev=prev)]

    return ip_path if len(ip_path) > 1 else []


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

import unittest
import dijkstra as di
import netfuncs as nf
import json


def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)


class TestNetFunctions(unittest.TestCase):

    def test_ipv4_to_value(self):
        self.assertEqual(nf.ipv4_to_value('255.255.0.0'), 4294901760)
        self.assertEqual(nf.ipv4_to_value('1.2.3.4'), 16909060)

    def test_value_to_ipv4(self):
        self.assertEqual(nf.value_to_ipv4(4294901760), '255.255.0.0')
        self.assertEqual(nf.value_to_ipv4(16909060), '1.2.3.4')

    def test_subnet_mask_value(self):
        self.assertEqual(nf.get_subnet_mask_value('/16'), 4294901760)
        self.assertEqual(nf.get_subnet_mask_value('10.20.30.40/23'), 4294966784)

    def test_ips_same_subnet(self):
        self.assertTrue(nf.ips_same_subnet(
            ip1="10.23.121.17",
            ip2="10.23.121.225",
            slash="/23"
        ))

        self.assertFalse(nf.ips_same_subnet(
            ip1="10.23.230.22",
            ip2="10.24.121.225",
            slash="/16"
        ))

    def test_get_network(self):
        self.assertEqual(nf.get_network(0x01020305, 0xffffff00), 0x01020300)

    def test_find_router_for_ip(self):
        routers = json.loads('{ "1.2.3.1": { "netmask": "/24"},"1.2.4.1": {"netmask": "/24"}}')

        self.assertEqual(nf.find_router_for_ip(routers=routers, ip="1.2.3.5"), "1.2.3.1")
        self.assertEqual(nf.find_router_for_ip(routers=routers, ip="1.2.5.6"), None)


class TestDSP(unittest.TestCase):
    def test_dijkstras_shortest_path(self):
        router_file_name = 'example1.json'

        json_data = read_routers(router_file_name)

        routers = json_data["routers"]

        self.assertEqual( ['10.34.52.1', '10.34.250.1', '10.34.166.1'], di.dijkstras_shortest_path(routers, src_ip="10.34.52.158", dest_ip="10.34.166.1"))

    def test_find_routes(self):
        di.find_routes(routers=read_routers('example1.json')['routers'],
                       src_dest_pairs=read_routers('example1.json')['src-dest'])


class TestDijkstras(unittest.TestCase):
    def test_dijkstras(self):

        test_adj_m = [[0, 1, 4, 4],
                      [8, 0, 4, 6],
                      [3, 5, 0, 7],
                      [9, 9, 2, 0]]

        test_graph = di.Graph(test_adj_m)

        test_graph.set_adj_matrix(test_adj_m)

    def test_shortest_path(self):
        test_adj_m = [[0, 0, 4, 0],
                      [8, 0, 4, 6],
                      [3, 5, 0, 0],
                      [9, 0, 2, 0]]
        test_graph = di.Graph(test_adj_m)

        s = 0
        d = 3

        test_prev = test_graph.dijkstra(src=s)

        self.assertEqual([0, 2, 1, 3],
                         di.Graph.shortest_path(dest=d, prev=test_prev))

    def test_router_dict_to_adj_m(self):
        routers = {
            "10.0.0.1": {
                "connections": {
                    "10.0.0.2": {
                        "ad": 5
                    },
                    "10.0.0.3": {
                        "ad": 10
                    }
                }
            },
            "10.0.0.2": {
                "connections": {
                    "10.0.0.1": {
                        "ad": 3
                    }
                }
            },
            "10.0.0.3": {
                "connections": {
                    "10.0.0.2": {
                        "ad": 1
                    }
                }
            }
        }

        expected_return = ([[0, 5, 10],
                            [3, 0, 0],
                            [0, 1, 0]],
                           ['10.0.0.1',
                            '10.0.0.2',
                            '10.0.0.3'])

        self.assertEqual(expected_return, di.RouterGraph.router_dict_to_adj_m(routers=routers))

    def test_sort_router_ip_addresses(self):
        expected_return = ['10.34.166.1', '10.34.194.1',
                           '10.34.209.1', '10.34.250.1',
                           '10.34.46.1', '10.34.52.1',
                           '10.34.53.1', '10.34.79.1',
                           '10.34.91.1', '10.34.98.1']

        json_data = read_routers('example1.json')

        routers = json_data["routers"]

        self.assertEqual(expected_return, di.RouterGraph.sort_router_ip_addresses(routers=routers))


if __name__ == '__main__':
    unittest.main()

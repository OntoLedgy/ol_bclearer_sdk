from collections import namedtuple
import networkx


Edge = \
    namedtuple('Edge',
                'righthandside lefthandside')                     #create a named tuple to store the edge data


class Edges(object):
    edge = "pass"
'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple
from ways import load_map_from_csv
import collections
import random



def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])

    # collects data from roads:
    num_of_links = []
    link_distances = []
    type_counter = collections.Counter()
    # iterate:
    for junc in roads.junctions():
        num_of_links.append(len(junc.links))
    for link in roads.iterlinks():
        link_distances.append(link.distance)
        type_counter[link.highway_type] += 1

    return {
        'Number of junctions' : len(roads),
        'Number of links' : sum(num_of_links),
        'Outgoing branching factor' : Stat(max=max(num_of_links), min=min(num_of_links),
                                           avg=sum(num_of_links) / len(num_of_links)),
        'Link distance' : Stat(max=max(link_distances), min=min(link_distances),
                               avg=sum(link_distances) / len(link_distances)),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram' : sorted(type_counter.items()) # tip: use collections.Counter
    }


def print_stats():
    r = load_map_from_csv()
    for k, v in map_statistics(r).items():
        print('{}: {}'.format(k, v))
    return r
        
if __name__ == '__main__':
    from sys import argv
    #assert len(argv) == 1
    r = print_stats()

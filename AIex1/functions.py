"""
functions file:
implemetation of pricing and heuristic functions.
"""
import ways.graph as graph
from ways import compute_distance
import ways.info as info

maxspeeds = [speedrange[1] for speedrange in info.SPEED_RANGES]
avgspeed = sum(maxspeeds)/len(maxspeeds)
def price_by_estimated_time(roads:graph.Roads, link:graph.Link):
    """
    :return: the price by the air distance on the link devided by the average time in the roads.
    """
    distance = link.distance
    speed = maxspeeds[link.highway_type]
    estimated_time = distance / speed
    return estimated_time


def calculate_total_time(roads, path):
    """
    :return: the total time of path in graph roads.
    """
    time_of_path = 0
    for i in range(len(path) - 1):
        link = [x for x in roads[path[i]].links if x.target == path[i + 1]][0]
        time_of_path += price_by_estimated_time(roads, link)
    return time_of_path

def astar_heuristic(roads:graph.Roads, src, trg):
    src_junc = roads[src]
    trg_junc = roads[trg]
    air_distance = compute_distance(src_junc.lat, src_junc.lon, trg_junc.lat, trg_junc.lon)
    # return the air distance / max speed in all graph.
    return 1000 * (air_distance / avgspeed)
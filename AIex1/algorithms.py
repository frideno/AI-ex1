"""
algorithms file:
implementation of all search algorithms.
"""

import heapq
import functions
import stats


def find_ucs_route(roads, s, t, price_func=functions.price_by_estimated_time):
    # init priority queue:
    pq = []
    visited = [False] *len(roads)

    # insert root.
    heapq.heappush(pq, (0, [s]))

    # while priority queue is not empty:
    try:
        while True:
            # pop from priority queue.
            current_price, current_junc_path = heapq.heappop(pq)
            current_junc_index = current_junc_path[-1]
            current_junc = roads[current_junc_index]
            # mark current junction visited.
            visited[current_junc_index] = True

            # if we reached target junction, return the path to it.
            if current_junc_index == t:
                return current_junc_path

            # for each link of the junction, that its target junction is not visited yet:
            for link in current_junc.links:
                if not visited[link.target]:
                    # push into pq the junction path, with price of path + price of link:
                    heapq.heappush(pq, (current_price + price_func(roads, link), current_junc_path + [link.target]))
    except IndexError:
        # if the priority queue is empty.
        return []

    # return the calculated path.
    return current_junc_path

def find_astar_route(roads, s, t, price_func=functions.price_by_estimated_time, heuristic_func=functions.astar_heuristic):

    # the data structures
    open_pq = []
    visited = [False] * len(roads)

    # insert start junction into pq
    heapq.heappush(open_pq, (0, 0, [s]))
    # while priority queue is not empty:
    try:
        while True:
            # pop from priority queue.
            current_f, current_g, current_path = heapq.heappop(open_pq)
            current_junc_index = current_path[-1]

            # mark current junction visited.
            visited[current_junc_index] = True

            # if we reached target junction, return the path to it.
            if current_junc_index == t:
                return current_path

            # for each link of the junction, that its target junction is not visited yet:
            for link in roads[current_junc_index].links:
                succ = link.target
                if not visited[succ]:
                    # push into pq the junction path, with price of path + price of link:
                    succ_g = current_g + price_func(roads, link)
                    succ_h = heuristic_func(roads, current_junc_index, t)
                    succ_f = succ_g + succ_h
                    heapq.heappush(open_pq, (succ_f, succ_g, current_path + [succ]))

    except IndexError:
        return []

    return current_path;

def find_idastar_route(roads, s, t, price_func=functions.price_by_estimated_time, huristic_func=functions.astar_heuristic):

    def search(path, g, threshold):
        node = path[-1]

        # check end conditions:
        f = huristic_func(roads, node, t) + g
        if node == t:
            return "FOUND"
        if f > threshold:
            return f

        # calculate min bound from succesors:
        min_b = float('Inf')
        for link in roads[node].links:
            succ = link.target
            if succ not in path:
                path.append(succ)
                g_succ = g + price_func(roads, link)
                b = search(path, g_succ, threshold)
                if b == "FOUND": return "FOUND"
                if b < min_b:
                    min_b = b
                path.pop()

        return min_b

    # starting a search from s to t:
    threshold = functions.astar_heuristic(roads, s, t)
    path = [s]
    while True:
        bound = search(path, 0, threshold)
        if bound == 'FOUND':
            return path
        threshold = bound

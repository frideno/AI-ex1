import algorithms as algos
import random
from ways import load_map_from_csv, compute_distance
import functions
import ways.draw as plotter
import time
import statistics

# generate problems part:


def generate_random_problem(roads):
    """
    generate random s,t problem.
    """
    num_of_roads = len(roads)
    s = random.randint(0, num_of_roads)
    t = random.randint(0, num_of_roads)
    return (s,t)

def BFS(roads, source, max_level):
    """
    BFS over roads graph, starting at source junction.

    """
    visited = [False] * (len(roads))
    queue = []
    level = 0
    queue.append((source, level))
    visited[source] = True
    while queue and level <= max_level:
        u, level = queue.pop(0)
        succ = [link[1] for link in roads.get(u).links]
        for v in succ:
            if not visited[v]:
                queue.append((v, level+1))
                visited[v] = True
    return visited


def generate_random_problems(roads, max_jumps):

    # open problems, solutions file for writing:
    with open('db/problems.csv', 'w') as problems_file:

        for i in range(100):
            # get random junction s.
            s = random.randint(0, len(roads))
            # create s BFS tree, at level 15. choose random t from it.
            s_bfs_visited = BFS(roads, s, max_jumps)
            s_bfs_tree = [i for i in range(len(roads)) if s_bfs_visited[i] == True]
            t = s_bfs_tree[random.randint(0, len(s_bfs_tree) - 1)]

            # write s,t to file.
            problems_file.write(str(s) + ',' + str(t) + '\n')


# solve part:

def solve_problems(roads, algo_name):
    # define algorithms dictionary
    algorithms = {'UCS': (algos.find_ucs_route, None),
                  'AStar': (algos.find_astar_route, functions.astar_heuristic),
                  'IDAStar': (algos.find_idastar_route, functions.astar_heuristic)}
    algorithm, heuristic = algorithms[algo_name]

    running_time = []
    with open('db/problems.csv', 'r') as problems_file, open('results/' + algo_name + 'Runs.txt', 'w') as solutions_file:
        for line in problems_file:
            s, t = int(line.split(',')[0]), int(line.split(',')[1])

            # activate algorithm to find path, and messure it running time on input.
            time0 = time.time()
            path = algorithm(roads, s, t)
            delta_time = time.time() - time0
            running_time.append(delta_time)

            # plot the path and save it as file.
            plotter.plot_path(roads, path)
            plotter.plt.savefig('solutions_img/' + algo_name + '_' + str(s) + '_' + str(t) + '.png')
            plotter.plt.cla()

            # calculate time of path, and write it to solutions file:
            time_of_path = functions.calculate_total_time(roads, path)
            if not heuristic:
                solutions_file.write(str(time_of_path) + '\n')
            else:
                estimated_time = heuristic(roads, s, t)
                solutions_file.write(str(estimated_time) + ',' + str(time_of_path) + '\n')

    return running_time

if __name__== '__main__':
    roads = load_map_from_csv()
    generate_random_problems(roads, 20)

    algos_to_run = ['UCS', 'AStar', 'IDAStar']
    for alg in algos_to_run:
        running_times = solve_problems(roads, alg)
        print(alg + ': mean = ' + str(statistics.mean(running_times)) +
              ', std = ' + str(statistics.stdev(running_times)))


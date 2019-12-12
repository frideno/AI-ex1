'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''

#do NOT import ways. This should be done from other files
#simply import your modules and call the appropriate functions

import algorithms
from ways import load_map_from_csv
import functions


def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    roads = load_map_from_csv()

    if argv[1] == 'ucs':
        path = algorithms.find_ucs_route(roads, source, target)
    elif argv[1] == 'astar':
        path = algorithms.find_astar_route(roads, source, target)
    elif argv[1] == 'idastar':
        path = algorithms.find_idastar_route(roads, source, target)
    else:
        print("wrong arg1, must be one of: ucs, astar, idastar")
        return

    print(' '.join(str(j) for j in path))


if __name__ == '__main__':
    from sys import argv
    dispatch(argv)


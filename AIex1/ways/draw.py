'accessible using "import ways.draw"'


from . import info
from . import tools
from . import graph

try:
    import matplotlib.pyplot as plt
except ImportError:
    raise ImportError('Please install matplotlib:  http://matplotlib.org/users/installing.html#windows')

plt.axis('equal')


def plot_path(roads, path, color='g'):
    '''path is a list of junction-ids - keys in the dictionary.
    e.g. [0, 33, 54, 60]
    Don't forget plt.show()'''
    flons, tolons, flats, tolats = [] ,[] ,[] ,[]
    for s, t in zip(path[:-1], path[1:]):
        ps, pt = roads[s], roads[t]
        flons.append(ps.lon)
        tolons.append(pt.lon)
        flats.append(ps.lat)
        tolats.append(pt.lat)
    plt.plot(flons, flats, color=color)


def set_no_axis():
    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(False)


def draw_links(roads, count=1000, types=list(range(len(info.ROAD_TYPES)))):
    lons, lats = [], []
    for link in roads.iterlinks():
        if link.highway_type not in types: ## not sure why we don't just do link.highway_type < # of types...
            continue
        src = roads[link.source]
        dst = roads[link.target]
        lons.append([src.lon, dst.lon])
        lats.append([src.lat, dst.lat])
    plt.plot(lons, lats, str(1 - 1.0 / (types[0] + 1)), zorder=14 - types[0])


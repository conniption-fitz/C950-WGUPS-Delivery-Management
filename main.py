"""
Fitzgerald, Victoria
Student ID: #000559078
C950

This program is a solve for the Traveling Salesman Problem. There are 40 packages that need to be delivered, 3 trucks,
and 2 drivers. 4 packages have been delayed, and 14 have special restrictions, such as an early delivery time, or need
to be delivered with other packages at the same time.

Main handles the import of all .csv files containing package information, addresses, and the distance Matrix. Main also
creates the trucks, and holds and runs the load_truck method, nearest_neighbor delivery method, and the UI.

Complexity: O(n^2)
"""

from package import Package
from truck import Truck
from hashMap import HashMap
from graphClass import Vertex
from graphClass import Graph

import csv

'''
Load Addresses:

All addresses are stored as a Vertex object in a list. Each Vertex has a label and address.
Vertices are loaded into a Graph. A distance Matrix holds the distances between each Vertex. 
The Matrix is formatted to remove blank indices, then edge weights for each Vertex pair is added to the downtown Graph.

Complexity: O(n)

'''
# load location vertices into a list
vertices = []

with open('WGUPSvertices.csv') as csvfile:
    vertex_file = csv.reader(csvfile, delimiter=',')

    for row in vertex_file:
        if any(row):
            vertices.append(Vertex(row[0], row[1]))

# add vertices to Graph
downtown = Graph()

for i in range(len(vertices)):
    downtown.add_vertex(vertices[i])

# load distance table into unformatted Matrix
unformatted_matrix = []
matrix = []

with open('WGUPSdistancematrix.csv') as csvfile:
    matrix_file = csv.reader(csvfile, delimiter=',')

    for row in matrix_file:
        unformatted_matrix.append(row)

# format Matrix
for row in unformatted_matrix:
    temp_row = []
    for x in range(len(row)):
        if row[x] != '':
            temp_row.append(float(row[x]))
            # gets rid of blanks, but doesn't separate by row
    matrix.append(temp_row)

# add edge weights to Graph
for k in range(len(matrix)):  # rows
    for j in range(len(matrix[k])):  # columns
        downtown.add_undirected_edge(vertices[k], vertices[j], matrix[k][j])

'''
Packages are loaded into the HashMap with all attributes initialized except the Vertex and Delivery Time.
All packages are initialized with the Status "At the Hub."
Each package is then matched with a Vertex to the same address.

Complexity: O(n^2)
'''
# load packages into HashMap
packages = HashMap(40)

with open('WGUPSpackage.csv') as csvfile:
    pack_file = csv.reader(csvfile, delimiter=',')

    for row in pack_file:
        if any(row):
            # int id, street, city, state, zip, deadline, weight, notes
            packages.insert(Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], 'At the Hub',
                                    None, None))

# set vertex to match address label on each package
for i in range(len(packages.table)):
    for j in range(len(vertices)):
        next_pack = packages.lookup(i)
        if next_pack.delivery_add == vertices[j].address:
            next_pack.set_vertex(vertices[j])

'''
There are three Truck objects, which contain attributes including start location, current time (which starts at 8:00am, 
and a list of package IDs of the packages that are loaded onto the truck. Each Truck has a constant speed of 18 MPH and 
a maximum load of 16 packages. Trucks update time and location at each delivery stop. 

All packages containing special notes are loaded into Truck 2, with the exception of delayed packages, which are 
manually loaded onto Truck 3. Remaining packages are loaded through a loop.

When packages are loaded onto the Truck, their status is updated to "On Truck" or "Delayed" for Truck 3. 

Complexity: O(n)
'''
truck1 = Truck()
truck2 = Truck()
truck3 = Truck()

# manually load special packages
truck1.load(9) # package 9 has incorrect address, fixed at 10:20, truck 1 doesn't leave until 10:35

# truck 2 takes all special packages except delayed
truck2.load(1)
truck2.load(3)
truck2.load(13)
truck2.load(14)
truck2.load(15)
truck2.load(16)
truck2.load(18)
truck2.load(19)
truck2.load(20)
truck2.load(29)
truck2.load(31)
truck2.load(34)
truck2.load(36)
truck2.load(37)
truck2.load(38)
truck2.load(40)

truck3.set_time(545)  # truck 3 can't leave the Hub until 9:05
truck3.load(6)
truck3.load(25)
truck3.load(28)
truck3.load(32)

# set package statuses for special packages
for i in range(len(truck2.pack_load)):
    current = packages.lookup(truck2.pack_load[i])
    current.set_status('On Truck')

for i in range(len(truck3.pack_load)):
    current = packages.lookup(truck3.pack_load[i])
    current.set_status('Delayed')

'''
Non-special packages are loaded onto the Truck until each truck reaches its maximum load. Each package's status is 
updated to "On Truck" when it is loaded.

Complexity: O(n^2)
'''


def load_trucks(truck, package_list):
    # load remaining packages and set status
    idx = 0
    while idx <= 40 and len(truck.pack_load) < truck.MAX_LOAD:
        check_p = package_list.lookup(idx)
        if check_p.status == 'At the Hub':
            truck.load(check_p.pack_id)
            check_p.set_status('On Truck')
        else:
            idx += 1


'''
Packages are delivered through a Nearest Neighbor algorithm. 

Once the method is called, all packages on the Truck have a status update change to "Out for Delivery."

Using the Vertex assigned to each package, the algorithm starts with the first package in the list (index 0) and checks 
the distance from the Hub to that Vertex. Then the algorithm loops through each package, checking the distance between 
current_vtx and next_closest to see if the distance is shorter. 

Once the shortest distance is determined, the Truck delivers that package. The package status is updated to "Delivered" 
with a timestamp. The Truck's delivery time and location is updated to match, and the algorithm determines the next 
delivery address. This repeats until all packages have been delivered, and the Truck returns to the Hub.

Complexity: O(n^2)
'''


# Nearest Neighbor algorithm - self adjusting, delivers packages
def nearest_neighbor(truck, graph, start_vertex, hash_map):
    current_vtx = start_vertex

    # update package status to "Out for Delivery"
    for i in range(len(truck1.pack_load)):
        current_pack = hash_map.lookup(i)
        current_pack.set_status('Out for Delivery')

    # find nearest location - loops until only one package is remaining
    while len(truck.pack_load) > 0:
        # look for closest package to current
        next_closest = hash_map.lookup(truck.pack_load[0])  # start comparing with first package on truck
        distance = graph.get_edge_weight(current_vtx, next_closest.vertex)
        smallest_index = 0
        for n in range(len(truck.pack_load)):
            check_pack = hash_map.lookup(truck.pack_load[n])
            check_distance = graph.get_edge_weight(check_pack.vertex, current_vtx)
            if check_distance <= distance:
                distance = check_distance
                next_closest = check_pack
                smallest_index = n
            if len(truck.pack_load) == 1:
                smallest_index = 0
                next_closest = hash_map.lookup(truck.pack_load[n])
        # travel to nearest delivery address
        current_vtx = next_closest.vertex
        # update truck location, mileage, timestamp
        truck.location = current_vtx.get_address()
        truck.update_time(distance)
        truck.update_miles(distance)
        delivery_time = truck.current_time
        # update package status
        next_closest.deliver(delivery_time)
        # remove package id from truck load
        truck.deliver(smallest_index)
    # all packages are delivered, truck returns to Hub
    distance = graph.get_edge_weight(start_vertex, current_vtx)
    truck.location = start_vertex.get_address()
    truck.update_time(distance)
    truck.update_miles(distance)


load_trucks(truck1, packages)
load_trucks(truck2, packages)
load_trucks(truck3, packages)

nearest_neighbor(truck2, downtown, vertices[0], packages)
truck1.set_time(truck2.current_time)  # truck 1 can't leave until truck 2 gets back

nearest_neighbor(truck3, downtown, vertices[0], packages)
nearest_neighbor(truck1, downtown, vertices[0], packages)

'''
The UI is a command-line interface with four options: 
1. Package Lookup by ID
2. Total truck mileage
3. Status of all packages by timestamp
4. Quit

The UI reads in the user's request and returns the appropriate information.

1. Package Lookup
This looks up the package by the user's requested ID number, and returns all attributes, current status, and delivery
time. 

2. Truck mileage
This returns the total mileage driven by all three trucks.

3. Status by timestamp
The user inputs a time and two lists of packages are returned. The first list is all packages that have been delivered 
by the requested time. The second list is all packages that have not been delivered by that time. 

Complexity: O(n)
'''
print('\nWelcome to WGUPS!\nWhat would you like to do today?' + '\n\t1. Look up a package' +
      '\n\t2. Check truck mileage' + '\n\t3. Check status by timestamp' + '\n\t4. Quit')

user_input = input()

# check for valid input
if not user_input.isdigit():
    print('Invalid input.')
# 1. Package Lookup
elif int(user_input) == 1:
    get_id = input('\nPlease enter a package ID:')
    if not get_id.isdigit():
        print('\nInvalid input.')
    else:
        user_pack = packages.lookup(int(get_id))
        print('\n')
        user_pack.print()
# 2. Truck mileage
elif int(user_input) == 2:
    mileage = truck1.get_total_miles() + truck2.get_total_miles() + truck3.get_total_miles()
    print('Total Mileage: ' + str(round(mileage, 2)) + ' miles')
# Package status by timestamp
elif int(user_input) == 3:
    # check timestamp
    get_time = input('Please enter a time: ')
    # convert user time to minutes for comparison
    split_time = get_time.split(':')
    hour = int(split_time[0]) * 60
    minutes = int(split_time[1])
    check_time = hour + minutes
    # compare user time to delivery time of packages
    delivered = []
    undelivered = []
    # if delivery time <= user time, add packages to list of delivered
    for x in range(len(packages.table)):
        check_pack = packages.lookup(x)
        if check_pack.delivery_time <= check_time:
            delivered.append(x)
        # else add packages to list of undelivered
        else:
            undelivered.append(x)
    print('Packages delivered by ' + get_time + ':')
    # print list of delivered package IDs and delivery time for each package
    for q in range(len(delivered)):
        temp_delivered = packages.lookup(delivered[q])
        print('Package ID: ' + str(temp_delivered.pack_id) + ', delivered: ' + str(temp_delivered.time_format()))
    print('\nPackages not delivered by ' + get_time + ':')
    # print list of undelivered package IDs
    for p in range(len(undelivered)):
        temp_undelivered = packages.lookup(undelivered[p])
        print('Package ID: ' + str(temp_undelivered.pack_id))
# 4. Quit
elif int(user_input) == 4:
    print('Goodbye!')

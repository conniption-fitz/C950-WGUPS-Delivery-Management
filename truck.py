"""
The Truck class initializes a Truck object with the Hub location, an empty package load list, total miles initialized
to 0, and a timestamp initialized to 8:00am, formatted in minutes.

Trucks have a constant SPEED of 18 MPH and MAX_LOAD of 16 packages.

The load method adds a package ID to the pack_load list and the deliver method removes the ID from pack_load. There are
getters and setters for each attribute. Time and mileage are updated each time the Truck moves to a new address when
delivering. There is a method to format the Truck timestamp, and a formatted print method.
"""


class Truck:
    SPEED = 18
    MAX_LOAD = 16

    def __init__(self):
        self.location = '4001 South 700 East'
        self.pack_load = []  # list of package IDs
        self.total_miles = 0
        self.current_time = 480

    def load(self, package_id):
        # load package onto truck
        self.pack_load.append(package_id)

    def deliver(self, index):
        self.pack_load.pop(index)

    def get_location(self):
        return self.location

    def get_pack_load(self):
        return self.pack_load

    def get_total_miles(self):
        return self.total_miles

    def set_time(self, time):
        self.current_time = time

    def update_time(self, miles):
        minutes = (miles / 18) * 60
        self.current_time += + int(minutes)

    def update_miles(self, miles):
        self.total_miles += miles
        self.total_miles = round(self.total_miles, 2)

    def set_location(self, address):
        self.location = address

    def time_format(self):
        hour = "{:02d}".format(int(self.current_time / 60))
        minute = "{:02d}".format(self.current_time % 60)
        time_string = hour + ':' + minute
        return time_string

    def print(self):
        print('Location: ', self.location,
              '\nCurrent Time: ', self.time_format(),
              '\nNumber of Packages: ', len(self.pack_load),
              '\nTotal Mileage: ', self.total_miles, )

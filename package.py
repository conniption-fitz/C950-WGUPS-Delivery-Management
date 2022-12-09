"""
The Package class holds all information attached to a package, including all information imported from WGUPSpackage.csv,
and the matching Vertex, status, and delivery time. Packages are initialized with a status of "At the Hub" and a null
delivery time and Vertex. The Vertex is updated on the Package in Main. The Package class has getters and setters for
each attribute, a method for formatting the timestamp for delivery_time, and a formatted print method.
"""


class Package:
    def __init__(self, pack_id, delivery_add, city, state, zipcode, delivery_dead, weight, notes, status, vertex,
                 delivery_time):
        self.pack_id = pack_id
        self.delivery_add = delivery_add
        self.delivery_dead = delivery_dead
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.weight = weight
        self.notes = notes
        self.status = status
        self.vertex = vertex
        self.delivery_time = delivery_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.pack_id, self.delivery_add, self.city, self.zipcode,
                                                       self.delivery_dead, self.weight, self.status, self.delivery_time,
                                                       self.notes)

    # getters would be used for UI
    def get_id(self):
        return self.pack_id

    def get_address(self):
        return self.delivery_add

    def get_deadline(self):
        return self.delivery_dead

    def get_city(self):
        return self.city

    def get_zipcode(self):
        return self.zipcode

    def get_weight(self):
        return self.weight

    def get_status(self):
        return self.status

    def get_vertex(self):
        return self.vertex

    def set_status(self, new_status):
        self.status = new_status

    def set_vertex(self, vertex):
        self.vertex = vertex

    def deliver(self, time):
        self.set_status('Delivered')
        self.delivery_time = time

    def time_format(self):
        not_del = 'This package has not been delivered.'
        if self.delivery_time is not None:
            hour = "{:02d}".format(int(self.delivery_time / 60))
            minute = "{:02d}".format(self.delivery_time % 60)
            time_string = hour + ':' + minute
            return time_string
        else:
            return not_del

    def print(self):
        print('Package ID: ', self.pack_id,
              '\nDelivery Address: ', self.delivery_add,
              '\nCity: ', self.city,
              '\nState: ', self.state,
              '\nZip Code', self.zipcode,
              '\nDelivery Deadline: ', self.delivery_dead,
              '\nPackage Weight: ', self.weight, ' Kilos',
              '\nCurrent Status: ', self.status,
              '\nDelivery Time: ', self.time_format(),
              '\nSpecial Notes: ', self.notes)

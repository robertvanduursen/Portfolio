"""

Bike ride calculator for routes across park De Veluwe around Arnhem 

Fietsroute naar kilometer per uur berekening

"""

bike_network = {
    # junction - connected to
    99: [79, 8, 36],
    79: [51, 72, 99],
    51: [50, 79, 64],
    64: [48, 71, 51],
    71: [64, 72, 67],
    72: [71, 77, 79],
    77: [72, 21, 12],
    34: [67, 66, 21],
    67: [17, 34, 71],
    17: [66, 68, 67],
    66: [17, 65, 69],
    65: [73, 25, 66],
    25: [63, 65, 53],
    53: [25, 69, 12],
    69: [53, 25, 69],
    12: [77, 85, 53],
    21: [77, 69, 34],
}

dists = {
    # distance lookup table per edge in kilometers
    (99, 79): 0.2,
    (99, 8): 2.5,
    (99, 36): 2.1,
    (79, 51): 0.8,
    (79, 72): 1.5,
    (79, 99): None,
    (51, 50): 1.4,
    (51, 79): None,
    (51, 64): 2.3,
    (64, 48): 3.0,
    (64, 71): 0.2,
    (64, 51): None,
    (71, 64): None,
    (71, 72): 1.2,
    (71, 67): 2.5,
    (72, 71): 1.1,
    (72, 77): 1.1,
    (72, 79): None,
    (77, 72): None,
    (77, 21): 1.2,
    (77, 12): 3.9,
    (34, 67): 0.5,
    (34, 66): 1.3,
    (34, 21): 2.5,
    (67, 17): 1.6,
    (67, 34): None,
    (67, 71): None,
    (17, 66): 0.7,
    (17, 68): 2.4,
    (17, 67): None,
    (66, 17): 0.7,
    (66, 65): 1.3,
    (66, 69): 1.6,
    (65, 73): 2.9,
    (65, 25): 0.8,
    (65, 66): None,
    (25, 63): 2.4,
    (25, 65): None,
    (25, 53): 1.6,
    (53, 25): None,
    (53, 69): 1.0,
    (53, 12): 1.2,
    (69, 53): None,
    (69, 21): 2.8,
    (12, 77): None,
    (12, 85): 0.2,
    (12, 53): None,
    (21, 77): None,
    (21, 69): None,
    (21, 34): None,
}


def check_sum():
    """ test function to make sure all junctions in network are labelled """
    for key in dists.keys():
        if dists[key] == None:
            rev = tuple(reversed(key))
            assert dists[rev] != None
            print("{} reversed = {} & has value {}".format(key, rev, dists[rev]))


class Distance_query:
    """ interaction object and calculator """
    junctions = False

    def calculate_kilometers_an_hour(self, duration):
        """ calculate the distance based off of provided junctions """
        total_dist = 0

        try:
            # make sure all the junctions are in the bike_network 
            assert all([d in bike_network for d in self.junctions])
        except Exception as e:
            print('the list needs to be amended')
            for d in self.junctions:
                if d not in bike_network:
                    print('junction {} not found in bike_network '.format(d))

            print(e)
            print('do you want to restart - Y / N?')
            if input() == 'Y':
                # abort and restart
                self.start_query()
                return False

        # presuming all inputs are valid
        for edge in zip(self.junctions, self.junctions[1:]):
            if dists[edge] == None:
                rev = tuple(reversed(edge))
                total_dist += dists[rev]
            else:
                total_dist += dists[edge]

        print("you've done {} km in {} minutes".format(round(total_dist, 2), duration))
        result = round((total_dist / 60.0) * float(duration)), 4
        print("so you've bike at {} km per hour on average".format(result))

        return result

    def start_query(self):
        """ manual input of junction sequence and duration to calculate with """
        print("Enter the junctions that you've seen in your bike ride today")
        print("Keep on entering until you are done, followed by a hashtag (#)")

        self.junctions = []
        entering = input()
        while str(entering) != '#':
            self.junctions.append(int(entering))

            # keep asking until hashtag
            entering = input()

        print("Ok great, these are the junctions you entered")
        print(self.junctions)

        print("How long did it take you in minutes? - or in 1h20m format")
        duration = input()

        result = self.calculate_kilometers_an_hour(duration)
        print("You've travelled at {} on average".format(result))

    def follow_up(self):
        """ physical and psych examination """
        print("Do you feel tired?")
        print("Do you feel energized?")



query = Distance_query()

# on 22 sep
query.junctions = [79, 72, 71, 67, 34, 66, 17, 67, 34, 21, 77, 72, 79]
query.calculate_kilometers_an_hour(57)

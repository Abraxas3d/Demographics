from typing import List

from gender_detector.gender_detector import GenderDetector
from uszipcode import SearchEngine
import random


active_licenses = set()

try:
    with open('C:/Users/Kindl/OneDrive/Documents/Amateur-Radio-Demographics/HD.dat', 'r') as headers:
        # pass
        for active_line in headers:
            active_list: list[str] = active_line.split("|")  # bust up the line at the | symbols, makes a list

            if (active_list[5] == "A"):  # active licenses
                active_licenses.add(active_list[4])

except FileNotFoundError:
    pass


# print(active_licenses)

# we now have a set of active licenses


detector = GenderDetector('us')  # It can also be ar, uk, uy.

search = SearchEngine(simple_zipcode=False)  # zipcode demographics lookup

unknown_names = open(r"C:/Users/Kindl/OneDrive/Documents/Amateur-Radio-Demographics/unknown_names.dat", "w+")

try:
    with open('C:/Users/Kindl/OneDrive/Documents/Amateur-Radio-Demographics/EN-clean .dat', 'r') as my_file:
        # pass

        male_count = 0
        female_count = 0
        other_count = 0
        unknown_count = 0
        punch_count = 0
        white_count = 0
        black_count = 0
        american_indian_count = 0
        asian_count = 0
        hawaiian_count = 0
        other_race_count = 0
        two_or_more_count = 0
        prob_white = 0.0
        prob_black = 0.0
        prob_american_indian = 0.0
        prob_asian = 0.0
        prob_hawaiian = 0.0
        prob_other_race = 0.0
        prob_two_or_more = 0.0
        zipcode_fail = 0
        total_count = 0

        for my_line in my_file:
            my_list: list[str] = my_line.split("|")  # bust up the line at the | symbols, makes a list

            if (my_list[4] in active_licenses) and (my_list[5] == "L") and (my_list[23] == "I"):  # active valid individual license? continue



                #test zipcode here?
                # print("zip code is:", my_list[18][:5])
                # search.by_zipcode(my_list[18])
                # print(search.by_zipcode(my_list[18]))
                my_zipcode = search.by_zipcode(my_list[18][:5])

                #     [{'key': 'Data', 'values': [{'x': 'White', 'y': 10439}, {'x': 'Black Or African American', 'y': 46},
                #                                 {'x': 'American Indian Or Alaskan Native', 'y': 60},
                #                                 {'x': 'Asian', 'y': 93},
                #                                 {'x': 'Native Hawaiian & Other Pacific Islander', 'y': 2},
                #                                 {'x': 'Other Race', 'y': 46}, {'x': 'Two Or More Races', 'y': 154}]}]

                if (my_zipcode.population_by_race == None):
                    zipcode_fail += 1
                    #print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                    #print("Zipcode access failed.")
                    #print("zip code is:", my_list[18][:5])
                    #print(my_line)
                    #print(my_zipcode)
                    #print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

                else:

                    # white_count += my_zipcode.population_by_race[0]['values'][0]['y']
                    # black_count += my_zipcode.population_by_race[0]['values'][1]['y']
                    # american_indian_count +=my_zipcode.population_by_race[0]['values'][2]['y']
                    # asian_count += my_zipcode.population_by_race[0]['values'][3]['y']
                    # hawaiian_count += my_zipcode.population_by_race[0]['values'][4]['y']
                    # other_race_count += my_zipcode.population_by_race[0]['values'][5]['y']
                    # two_or_more_count += my_zipcode.population_by_race[0]['values'][6]['y']

                    # print(my_zipcode.population_by_race[0]['values'][0])
                    # print(my_zipcode.population_by_race[0]['values'][0]['y'])
                    # print(my_zipcode.population_by_race[0]['values'][1])
                    # print(my_zipcode.population_by_race[0]['values'][1]['y'])
                    # print(my_zipcode.population_by_race[0]['values'][2])
                    # print(my_zipcode.population_by_race[0]['values'][2]['y'])
                    # print(my_zipcode.population_by_race[0]['values'][3])
                    # print(my_zipcode.population_by_race[0]['values'][3]['y'])
                    # print(my_zipcode.population_by_race[0]['values'][4])
                    # print(my_zipcode.population_by_race[0]['values'][4]['y'])
                    # print(my_zipcode.population_by_race[0]['values'][5])
                    # print(my_zipcode.population_by_race[0]['values'][5]['y'])
                    # print(my_zipcode.population_by_race[0]['values'][6])
                    # print(my_zipcode.population_by_race[0]['values'][6]['y'])
                    # print(my_zipcode.population)

                    prob_white = my_zipcode.population_by_race[0]['values'][0]['y'] / my_zipcode.population
                    # print(prob_white)
                    prob_black = my_zipcode.population_by_race[0]['values'][1]['y'] / my_zipcode.population
                    # print(prob_black)
                    prob_american_indian = my_zipcode.population_by_race[0]['values'][2]['y'] / my_zipcode.population
                    # print(prob_american_indian)
                    prob_asian = my_zipcode.population_by_race[0]['values'][3]['y'] / my_zipcode.population
                    # print(prob_asian)
                    prob_hawaiian = my_zipcode.population_by_race[0]['values'][4]['y'] / my_zipcode.population
                    # print(prob_hawaiian)
                    prob_other_race = my_zipcode.population_by_race[0]['values'][5]['y'] / my_zipcode.population
                    # print(prob_other_race)
                    prob_two_or_more = my_zipcode.population_by_race[0]['values'][6]['y'] / my_zipcode.population
                    # print(prob_two_or_more)

                    random_number = random.randrange(0, 100000) / 100000
                    #print("Random number is:", random_number)
                    #print("The sum of the probabilities is:", (prob_hawaiian + prob_black + prob_american_indian + prob_asian + prob_white + prob_two_or_more + prob_other_race))

                    if (random_number < prob_white):
                        white_count += 1
                    elif (random_number < prob_white + prob_black):
                        black_count += 1
                    elif (random_number < prob_white + prob_black + prob_american_indian):
                        american_indian_count += 1
                    elif (random_number < prob_white + prob_black + prob_american_indian + prob_asian):
                        asian_count += 1
                    elif (random_number < prob_white + prob_black + prob_american_indian + prob_asian + prob_hawaiian):
                        hawaiian_count += 1
                    elif (random_number < prob_white + prob_black + prob_american_indian + prob_asian + prob_hawaiian + prob_other_race):
                        other_race_count += 1
                    elif (random_number < prob_white + prob_black + prob_american_indian + prob_asian + prob_hawaiian + prob_other_race + prob_two_or_more):
                        two_or_more_count += 1
                    else:
                        print("You have fallen through the race test crack.")
                        print("Random number is:", random_number)







                if (my_list[8] == ".") or (my_list[8] == ",") or (my_list[8] == ""):  # can't analyze these for name
                    punch_count += 1
                else:
                    # print(my_line)

                    # if (my_list[8] == "('Russ')William") ?
                    #    my_gender = male_count +=1
                    # Removed the ('Russ') from this line
                    # but really should write a test for this.

                    # wrote a test for "," and for ".", and for "".


                    my_gender = (detector.guess(my_list[8]))
                    if my_gender == "male":
                        male_count += 1
                        # print(my_list[8])
                    elif my_gender == "female":
                        female_count += 1
                        # print(my_list[8])
                    elif my_gender == "unknown":
                        unknown_count += 1
                        unknown_names.write(my_list[8])
                        unknown_names.write("\n")
                        # print(my_list[8])
                        # write these names to a file
                        # for further processing




                total_count += 1



            else:
                other_count += 1
                # print("other license type: ", my_list[8])

        print("female:", female_count,
              "male", male_count,
              "unknown", unknown_count,
              "punched out", punch_count)
        print("white:", white_count,
              "black:", black_count,
              "american indian alaskan native:", american_indian_count,
              "asian:", asian_count,
              "native american or pacific islander:", hawaiian_count,
              "other:", other_race_count,
              "two or more races:", two_or_more_count,
              "zipcode fail:", zipcode_fail,
              "total race count:", (white_count + black_count + american_indian_count + asian_count + hawaiian_count + other_race_count + two_or_more_count + zipcode_fail))
        print("total count:", total_count,
              "other license type", other_count)

    my_file.close()
    unknown_names.close()



except FileNotFoundError:
    pass

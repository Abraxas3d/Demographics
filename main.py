import os
import sys
import glob
import json
import random
import webbrowser

import folium
import pandas as pd
from gender_detector.gender_detector import GenderDetector
import uszipcode 
import sqlite3

class dattr(dict):
    """
    "dict-attr", used for when you don't want to type [""] all the time
    """
    def __getattr__(self,name):
        """
        With a dattr, you can do this:
        >>> x = dattr({"abc":True})
        >>> x.abc
        True

        """
        if type(self[name]) == type({}): 
            #make sure we wrap any nested dicts when we encounter them
            self[name] = dattr(self[name]) #has to assign to save any changes to nested dattrs
            #e.g.  x.abc.fed = "in" 
        #otherwise just make our key,value pairs accessible through . (e.g. x.name)
        return self[name]
    def __setattr__(self,name,value):
        """
        With a dattr, you can do this:

        >>> x = dattr({"abc":True})
        >>> x.abc = False
        >>> x.abc
        False
        """
        self[name] = value

class FCCTable:
    pass
class AD(FCCTable):
    applicationpurpose_codes = {
            "AA":"Assignment of Authorization",
            "AM":"Amendment",
            "AR":"DE Annual Report",
            "AU":"Administrative Update",
            "CA":"Cancellation of License",
            "CB":"C Block Election",
            "DC":"Data Correction",
            "DU":"Duplicate License",
            "EX":"Request for Extension of Time",
            "HA":"HAC Report",
            "LC":"Cancel a Lease",
            "LE":"Extend Term of a Lease",
            "LL":"'603T', no longer used",
            "LM":"Modification of a Lease",
            "LN":"New Lease",
            "LT":"Transfer of Control of a Lessee",
            "LU":"Administrative Update of a Lease",
            "MD":"Modification",
            "NE":"New",
            "NT":"Required Notification",
            "RE":"DE Reportable Event",
            "RL":"Register Link/Location",
            "RM":"Renewal/Modification",
            "RO":"Renewal Only",
            "TC":"Transfer of Control",
            "WD":"Withdrawal of Application",
            }
    applicationstatus_codes = {
            "1":"Submitted",
            "2":"Pending",
            "A":"A Granted",
            "C":"Consented To",
            "D":"Dismissed",
            "E":"Eliminate",
            "G":"Granted",
            "H":"History Only",
            "I":"Inactive",
            "J":"HAC Submitted",
            "K":"Killed",
            "M":"Consummated",
            "N":"Granted in Part",
            "P":"Pending Pack Filing",
            "Q":"Accepted",
            "R":"Returned",
            "S":"Saved",
            "T":"Terminated",
            "U":"Unprocessable",
            "W":"Withdrawn",
            "X":"NA",
            "Y":"Application has problems",
            }
class AM(FCCTable):
    operatorclass_codes = {
            "A":"Advanced",
            "E":"Amateur Extra",
            "G":"General",
            "N":"Novice",
            "P":"Technician Plus",
            "T":"Technician",
    }

class HD(FCCTable):
    licensestatus_codes = {
            "A":"Active",
            "C":"Canceled",
            "E":"Expired",
            "L":"Pending Legal Status",
            "P":"Parent Station Canceled",
            "T":"Terminated",
            "X":"Term Pending",
            }
class EN(FCCTable):
    entitytype_codes = {
            "CE":"Transferee contact",
            "CL":"Licensee Contact",
            "CR":"Assignor or Transferor Contact",
            "CS":"Lessee Contact",
            "E":"Transferee",
            "L":"Licensee or Assignee",
            "O":"Owner",
            "R":"Assignor or Transferor",
            "S":"Lessee",
            }

    applicanttypecode_codes = {
            "B":"Amateur Club",
            "C":"Corporation",
            "D":"General Partnership",
            "E":"Limited Partnership",
            "F":"Limited Liability Partnership",
            "G":"Governmental Entity",
            "H":"Other",
            "I":"Individual",
            "J":"Joint Venture",
            "L":"Limited Liability Company",
            "M":"Military Recreation",
            "O":"Consortium",
            "P":"Partnership",
            "R":"RACES",
            "T":"Trust",
            "U":"Unincorporated Association",
            }

class ULS:
    pass

class licensee:
    def __init__(self, uid):
        self.uid = uid
    def get(self):
        """
        select HD.id, HD.callsign, HD.licensestatus, where HD.radioservicecode in ('HV','HA')
        """



def create_db(dbcon): 
    db = dbcon.cursor()
    db.execute('''CREATE TABLE HD (
            id integer, 
            ulsfilenum text,
            ebfnum text,
            callsign text,
            licensestatus text,
            radioservicecode text,
            grantdate text,
            expireddate text,
            cancellationdate text,
            eligibilityrulenum text,
            reserved text,
            alien text,
            aliengov text,
            aliencorp text,
            alienofficer text,
            aliencontrol text,

            revoked text,
            convicted text,
            adjudged text,
            reserved2 text,
            commoncarrier text,
            noncommoncarrier text,
            privatecomm text,
            fixed text,
            mobile text,
            radiolocation text,
            satellite text,
            developmentalorstaordemonstration text,
            interconnectedservice text,

            certifierfirstname text,
            certifiermi text,
            certifierlastname text,
            certifiersuffix text,
            certifiertitle text,

            female text,
            black text,
            nativeamerican text,
            hawaiian text,
            asian text,
            white text,
            hispanic text,

            effectivedate text,
            lastactiondate text,

            auctionid integer,
            broadcastregstat text,
            bandmanagerregstat text,
            broadcastservicetype text,
            alienruling text,
            licenseenamechange text,
            whitespaceindicator text,
            operationperformancereqchoice text,
            operationperformancereqanswer text,
            discontinuationofservice text,
            regulatorycompliance text,

            eligibilitycert900mhz text,
            transitionplancert900mhz text,
            returnspectrumcert900mhz text,
            paymentcert900mhz text
            )''')
    db.execute('''CREATE TABLE EN 
            (
            id integer, 
            ulsfilenum text,
            ebfnum text,
            callsign text,
            entitytype text,
            licenseeid text,
            entityname text,
            firstname text,
            middleinitial text,
            lastname text,
            suffix text,
            phone text,
            fax text,
            email text,
            streetaddress text,
            city text,
            state text,
            zipcode text,
            pobox text,
            attnline text,
            SGIN text,
            FRN text,
            applicanttypecode text,
            applicanttypecodeother text,
            statuscode text,
            statusdata text,
            licensetype3g7 text,
            linkedid integer,
            linkedcallsign text
            )''')
    db.execute('''CREATE TABLE AM
            (
            id integer, 
            ulsfilenum text,
            ebfnum text,
            callsign text,
            operatorclass text,
            groupcode text,
            regioncode integer,
            trusteecallsign text,
            trusteeindicator text,
            physiciancertification text,
            vesignature text,
            systematiccallsignchange text,
            vanitycallsignchange text,
            vanityrelationship text,
            previouscallsign text,
            previousoperatorclass text,
            trusteename text
            )''')
    db.execute('''CREATE TABLE VC
            (
            id integer, 
            ulsfilenum text,
            ebfnum text,
            orderofpreference integer,
            requestedcallsign text
            )''')
    dbcon.commit()

def import_table(dbcon, table):
    db = dbcon.cursor()
    db.execute("select count(*) from %s"%(table)) #table name must be trusted
    rowcnt = db.fetchone()[0]
    if not rowcnt:
        with open('data/%s.dat'%(table), 'r') as fd:
            #not great because readlines reads the whole file at once.
            rows = [line.strip().split('|')[1:] for line in fd.readlines()]
            #strip it so the string doesn't have a newline
            #split it into a list of columns (FCC db dump uses the pipe as a field separator)
            #remove the first column value because we already know it's "AM" for AM rows, "HD" for HD rows, etc

            #table name must be trusted
            s = "INSERT INTO %s VALUES ("%(table) + ("?,"*len(rows[0]))[:-1] + ")"
            db.executemany(s, rows)

        dbcon.commit()
    else:
        print("already imported ", table)

def import_data(dbcon):

    #if you get no such table here, you need to start fresh on DB
    import_table(dbcon, "AM")
    import_table(dbcon, "HD")
    import_table(dbcon, "EN")

class LicenseeRow(sqlite3.Row):
    def __str__(self):
        s = ""
        for k in self.keys():
            s += k + ":" + str(self[k]) + ", "
        return s
    def __getattr__(self,name):
        return self[name]
    def __setattr__(self,name,value):
        self[name] = value
       
def query(dbcon, q):
    db = dbcon.cursor()
    db.execute(q)
    i = 0
    for row in db.fetchall():
        print(i)
        for column in row.keys():
            print("\t",column, row[column])
        i+=1


def main():
    mustcreatedb = not os.path.isfile("uls.db")
    dbcon = sqlite3.connect('uls.db')
    dbcon.row_factory = LicenseeRow
    if mustcreatedb:
        create_db(dbcon)
    import_data(dbcon)
    active_licenses = set()
    db = dbcon.cursor()
    # s="select HD.callsign, EN.firstname, EN.lastname, AM.operatorclass from HD inner join EN on HD.id=EN.id inner join AM on HD.id=AM.id where "+\
        # "HD.radioservicecode in ('HV','HA') and HD.licensestatus='A' and EN.entitytype='L' and EN.applicanttypecode='I' and EN.city='Chelmsford' and EN.state='MA'"
    # query(dbcon,s)
    # import pdb; pdb.set_trace()
    s="select HD.callsign, EN.firstname, EN.city, EN.state, EN.zipcode from HD inner join EN on HD.id=EN.id where "+\
        "HD.radioservicecode in ('HV','HA') and HD.licensestatus='A' and EN.entitytype='L' and EN.applicanttypecode='I'"+\
        "and EN.state in ('MA','NH')"
        # "and EN.state in ('MA','NH','ME','CT','RI','NY')"
        # "and EN.state in ('FL','AL','GA','MS','SC','LA')"
        # "and EN.state in ('FL','AL','GA','MS','SC','NC','LA','TN','AR')"
    detector = GenderDetector('us')  # It can also be ar, uk, uy.
    search = uszipcode.SearchEngine()  # zipcode demographics lookup

    heat_map_dataframe = pd.DataFrame()
    heat_map_dictionary = {}
    errors = []

    i = 0
    err=0
    with open("us-states.json","r") as fd:
        statedata=json.load(fd)
    stateabbr = {
            "new-hampshire":"NH",
            "massachusetts":"MA",
            # "maine":"ME",
            # "vermont":"VT",
            # "new-york":"NY",
            # "rhode-island":"RI",
            # "connecticut":"CT",
            # "florida":"FL",
            # "alabama":"AL",
            # "georgia":"GA",
            # "mississippi":"MS",
            # "louisiana":"LA",
            # "south-carolina":"SC",
            # "north-carolina":"NC",
            # "tennessee":"TN",
            # "arkansas":"AR",
            # "texas":"TX",
            }
    statepops2019 = {}
    for obj in statedata:
        if obj["Slug State"] in stateabbr and obj["ID Year"] == 2019:
            statepops2019[stateabbr[obj["Slug State"]]] = obj["Population"]

    for row in db.execute(s):
        # print(row)
        zc = search.by_zipcode(row.zipcode[:5])
        if not zc or zc.population is None:
            # print("no zc for row.zipcode?", row.zipcode)
            # errors.append(row)
            err+=1
            continue
        if zc.state not in stateabbr.values():
            #some of our data is bad and the zip code doesn't match the state
            #either in our zip code db or the fcc db
            continue
        if zc.state not in heat_map_dictionary:
            heat_map_dictionary[zc.state] = {}
        if zc.zipcode not in heat_map_dictionary[zc.state]:
            heat_map_dictionary[zc.state][zc.zipcode] = 0
        heat_map_dictionary[zc.state][zc.zipcode] += 1
        i+=1
        # if i > 10000:
            # break
        if i % 10000 == 0:
            print(i)
    print("errs: ",err)

    #TODO: race data where available
    #TODO: gender guessing

    m = folium.Map(location=[40, -70], zoom_start=5, tiles='Stamen Toner')
    # for state in heat_map_dictionary:
        # for zipcode in heat_map_dictionary[state]:
            # heat_map_dictionary[state][zipcode] = heat_map_dictionary[state][zipcode]/330000000
    for state in heat_map_dictionary:
        print("adding", state)
        heat_map_dataframe = pd.DataFrame.from_dict(heat_map_dictionary[state], orient='index').reset_index()
        heat_map_dataframe.columns = ['ZCTA5CE10', 'licensees'] #column headings for ca_california_zip_codes.geojson
        # stategeojson=glob.glob("State-zip-code-GeoJSON/%s*.simple.topojson"%(state.lower()))
        stategeojson=glob.glob("State-zip-code-GeoJSON/%s*.min.json"%(state.lower()))
        """
        for each in State-zip-code-GeoJSON/*.min.json; do echo $each; ./node_modules/topojson-server/bin/geo2topo $each -o $each.topojson; ./node_modules/topojson-simplify/bin/toposimplify -F $each.topojson -o $each.simple.topojson; done
State-zip-code-GeoJSON/ak_alaska
    """

        if len(stategeojson):
            zip_geo = stategeojson[0]
            print(zip_geo)
            folium.Choropleth(
                geo_data=zip_geo,
                name=state,
                data=heat_map_dataframe,
                #columns=['zip', 'licensees'],
                #key_on='feature.properties.zip',
                columns=["ZCTA5CE10", "licensees"],
                key_on="feature.properties.ZCTA5CE10",
                fill_color="YlGn",
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name="Heat Map %s"%(state),
            ).add_to(m)
        else:
            print("no zip codes outline for ", state)
    folium.LayerControl().add_to(m)
    m.save('heatmap.html')


main()
sys.exit(0)

# unknown_names = open("generated/unknown_names.dat", "w+")

def xyDatatoDict(valuearray):
    #     [{'key': 'Data', 'values': [{'x': 'White', 'y': 10439}, {'x': 'Black Or African American', 'y': 46},
    #                                 {'x': 'American Indian Or Alaskan Native', 'y': 60},
    #                                 {'x': 'Asian', 'y': 93},
    #                                 {'x': 'Native Hawaiian & Other Pacific Islander', 'y': 2},
    #                                 {'x': 'Other Race', 'y': 46}, {'x': 'Two Or More Races', 'y': 154}]}]
    return {x:y for x,y in valuearray}


"""
                # def zipToRaceProbabilities(zc): #zc = zipcode, the object (not a string)
                    # return {x:y/zc zipDataToDict(zipdata)

                if (my_zipcode.population_by_race == None):
                    zipcode_fail += 1
                    #print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
                    #print("Zipcode access failed.")
                    #print("zip code is:", my_list[18][:5])
                    #print(my_line)
                    #print(my_zipcode)
                    #print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")

                else:
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

                if (my_list[8].startswith('(')) or (my_list[8] == ".") or (my_list[8] == ",") or (my_list[8] == ""):
                    # can't analyze these for name
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
              "male:", male_count,
              "unknown:", unknown_count,
              "punched out:", punch_count)
        print("white:", white_count,
              "black:", black_count,
              "american indian alaskan native:", american_indian_count,
              "asian:", asian_count,
              "native Hawaiian or pacific islander:", hawaiian_count,
              "other:", other_race_count,
              "two or more races:", two_or_more_count,
              "zipcode fail:", zipcode_fail,
              "total race count:", (white_count + black_count + american_indian_count + asian_count + hawaiian_count + other_race_count + two_or_more_count + zipcode_fail))
        print("total count:", total_count,
              "other license type", other_count)
        #print("Zip code array: ", heat_map_array)

    my_file.close()
    unknown_names.close()





    heat_map_dataframe = pd.DataFrame.from_dict(heat_map_dictionary, orient='index').reset_index()
    heat_map_dataframe.columns = ['ZCTA5CE10', 'licensees'] #column headings for ca_california_zip_codes.geojson
    #heat_map_dataframe.columns = ['zip', 'licensees']    #column headings for SanDiego.geojson

    #print(heat_map_dataframe)  #check to see if it looks right


    #zip_geo="92130.geojson" #worked
    #zip_geo="SanDiego.geojson" #worked
    zip_geo="ca_california_zip_codes.geojson" #worked




    m = folium.Map(location=[33, -117], zoom_start=5)


    folium.Choropleth(
        geo_data=zip_geo,
        name='choropleth',
        data=heat_map_dataframe,
        #columns=['zip', 'licensees'],
        #key_on='feature.properties.zip',
        columns=["ZCTA5CE10", "licensees"],
        key_on="feature.properties.ZCTA5CE10",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Heat Map",
    ).add_to(m)

    folium.LayerControl().add_to(m)


    m.save('heatmap.html')
    webbrowser.open('heatmap.html', new=2)

except FileNotFoundError:
    pass

"""

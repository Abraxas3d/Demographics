# Demographics
US Amateur License Holders Demographics

Paper about this work:
https://github.com/Abraxas3d/Demographics/blob/master/Who-We-Are.pdf

Video presentation at [RATPAC 26 January 2022](https://youtu.be/hrGsTKFp_HU)

This is a python script that uses the publicly available FCC database as
a source of licensee name and address information, a machine learning
algorithm that assigns gender to first name, and a zipcode search that
uses census information to make a probabalistic guess about race of the
license holder based on where they live.

The information is presented as text results and as a folium choropleth
map of licensee intensity per zip code. California is used as the
example choropleth.

There are some obvious improvements, the first of which is to move from
zip code to more proper geotagging. The second of which is to create an
interactive online map of the entire United States, and not just export
a local html of California.

Feedback, comment, critique, improvements, and collaboration are welcome
and encouraged.



## Data Sources

FCC licensing database dumps: https://www.fcc.gov/uls/transactions/daily-weekly
Database dump documentation: https://www.fcc.gov/wireless/data/public-access-files-database-downloads
Further details the database dump documentation expects you to know: https://wireless2.fcc.gov/helpfiles/licenseSearch/helpLand.html



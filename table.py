from prettytable import PrettyTable, ALL
import os

def generate(artistStats, artistHeaders,trackStats,trackHeaders):

    filePath = os.path.abspath(__file__)
    fileDir = os.path.dirname(filePath)#The directory the python file is in

    statsDir = os.path.join(fileDir, 'stats')
    if not os.path.exists(statsDir):
        os.mkdir('stats') #If the stats directory does not exist, it will be created    

    #Generating table for artist data
    table = PrettyTable()
    table.field_names = artistHeaders
    for i in artistStats:
        table.add_row(i)
    table._max_width = {artistHeaders[1]:20,artistHeaders[2]:13,artistHeaders[5]:13,artistHeaders[3]:13,artistHeaders[4]:13}
    table.hrules = ALL
    table.header = False
    with open('stats/artists.txt','w') as statsfile:
        statsfile.write(table.get_string())

    #Generating table for track data
    table = PrettyTable()
    table.field_names = trackHeaders
    for i in trackStats:
        table.add_row(i)
    table._max_width = {trackHeaders[1]:20,trackHeaders[2]:20,trackHeaders[3]:13,trackHeaders[4]:13}
    table.hrules = ALL
    table.header = False
    with open('stats/tracks.txt','w') as statsfile:
        statsfile.write(table.get_string())

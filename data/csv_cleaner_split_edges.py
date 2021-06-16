#import libraries
import pandas as pd
import re

#df for DataFrame
df = pd.read_csv('Master_Filtered_Inc_Vanity.csv')

num_rows = df.shape[0] #number of rows

#things for the resulting csv
#eg. Id; release_title; "artist1,arist2";label; year; country; "label1,label2"; 

#create label edge file
edge_file_label = open("adjacencylist_label_only.csv","wb")

#create artist file
edge_file_artist = open("adjacencylist_artist_only.csv","wb")

#create style file
edge_file_style = open("adjacencylist_style_only.csv","wb")


size = 10
res_data = [None] * size
res_id   = 0
cur_id   = 0

def write(id,a):
    try:
        # write to edge files
        edge_file_label.write("{}; {}\n".format(a[9],a[2]).encode("utf-8"))
        edge_file_artist.write("{}; {}\n".format(a[9],a[1]).encode("utf-8"))
        edge_file_style.write("{}; {}\n".format(a[9],a[5]).encode("utf-8"))

    except:
        print("error: release skipped")


for i in range(num_rows):
    x = df.iloc[i,0].split('.') #split result number info

    # set id for current release
    cur_id = int(x[2]) + int(x[0])*100 #corresponds to centi / deca      
    
    # check if new release
    if(cur_id != res_id):
        #save res_data to file
        write(res_id,res_data)
        res_id = cur_id
        res_data = [None] * size

    # determine attribute (title, year etc.)
    # replace / remove symbols that breaks the .csv format
    attr = x[3]
    val  = df.iloc[i,1]
    val = val.replace("\"","")
    val = val.replace("'","")
    val = val.replace(",","/")
    val = val.replace(";","/")
    # do something depending on which attribute
    if attr == "title":
        title_val = val.split(" - ")
        # release title
        res_data[0] = "title:" + title_val[1].strip()
        # artist(s) by splitting at regex
        artist_regex = '(?i)\s+&\s+|\s+and\s+|\s*,\s*|\s+vs.?\s+|\s*/\s*|\s*\+\s*|\s+a.k.a.\s+|\s+ft.?\s+|\s+featuring\s+|\s+presents\s+|\s+with\s+|\s+w/\s+|\s+feat.?\s+|\s+x\s+|\s*:\s*'
        artists = re.split(artist_regex,title_val[0])
        res_data[1] = "artist:"+"; artist:".join(["{}"]*len(artists)).format(*artists)
    if attr == "label":
        res_data[2] = "label:" + val
    if attr == "year":
        res_data[3] = val
    if attr == "country":
        res_data[4] = val
    if attr == "style":
        if res_data[5] is not None:
            res_data[5] =  res_data[5] + "; style:" + val
        else:
            res_data[5] = "style:" + val
    if attr == "uri":
        res_data[6] = str('https://www.discogs.com'+val)
    if attr == "community":
        if x[4] == "want":
                res_data[7] = val
        else:
            res_data[8] = val
    if attr == "id":
        res_data[9] =val


edge_file_label.close()
edge_file_artist.close()
edge_file_style.close()


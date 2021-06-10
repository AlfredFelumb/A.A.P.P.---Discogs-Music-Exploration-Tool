#import libaries
import pandas as pd
import re
import hashlib

#df for DataFrame
df = pd.read_csv('Master_Filtered_Inc_Vanity.csv')

num_rows = df.shape[0] #number of rows

#create masternode file
node_file = open("masternodeslist_split_no_regex.csv","wb") 

#creates header for masternode file
node_file.write("Label; title; artists; recordlabels; year; country; styles; url; want; have\n".encode("utf-8"))

size = 10
res_data = [None] * size
res_id   = 0
cur_id   = 0

def write(id,a):
    try:
        # write to masternode file
        node_file.write("{}; {}; {}; {}; {}; {}; {}; {}; {}; {}\n".format(a[9],a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8]).encode("utf-8"))

    except:
        print("error: release skipped")


for i in range(num_rows):
    x = df.iloc[i,0].split('.') #split result number info

    # set id for current release
    cur_id = int(x[2]) + int(x[0])*100 #svarer til centi+deca koden     
    
    # check if new release
    if(cur_id != res_id):
        #save res_blob to file
        write(res_id,res_data)
        res_id = cur_id
        res_data = [None] * size

    # determine attribute (title, year etc.)
    attr = x[3]
    val  = df.iloc[i,1]
    # replace / remove symbols that breaks the .csv format
    val = val.replace("\"","")
    val = val.replace("'","")
    val = val.replace(",","/")
    val = val.replace(";","/")
    # do something depending on which attribute
    if attr == "title":
        title_val = val.split(" - ")
        # release title
        res_data[0] = title_val[1].strip()
        res_data[1] = title_val[0].strip()
    if attr == "label":
        res_data[2] = val
    if attr == "year":
        res_data[3] = val
    if attr == "country":
        res_data[4] = val
    if attr == "style":
        if res_data[5] is not None:
            res_data[5] =  res_data[5] + ", " + val
        else:
            res_data[5] = val
    if attr == "uri":
        res_data[6] = str('https://www.discogs.com'+val)
    if attr == "community":
        if x[4] == "want":
            res_data[7] = val
        else:
            res_data[8] = val
    if attr == "id":
        res_data[9] =val

node_file.close()


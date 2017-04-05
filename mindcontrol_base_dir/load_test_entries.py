#!/usr/bin/env python
from glob import glob
import numpy as np

def get_collection(port=3001):
    from pymongo import MongoClient
    client = MongoClient("localhost", port)
    db =  client.meteor
    collection = db.subjects
    return collection, client

coll, cli = get_collection()
files = glob("sub*/anat/sub*_T1w.nii.gz")

for f in files:
    entry = {"entry_type":"test", # this is what we use to filter items into different tables in the UI. Instead of test, you can give it a meaningful name, like "raw_data" or "segmentation_file"
             "metrics":{"GMV": np.random.rand()*100, #these are random numbers, but you could load whatever you want here
             "WMV": np.random.rand()*100}}
    Sid = f.split('/')[0] #getting subject ID from the filename
    entry["subject_id"] = Sid
    entry["name"] = Sid
    entry["check_masks"] = [f] #list of paths to files relative to /base/directory
    coll.insert_one(entry) #finally, insert an entry to the mongo database

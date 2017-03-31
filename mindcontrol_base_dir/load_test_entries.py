from glob import glob
import numpy as np
import os
# Run this from the mind control base directory
def get_collection(port=3001):
    from pymongo import MongoClient
    client = MongoClient("localhost", port)
    db = client.meteor
    collection = db.subjects
    return collection, client

coll, cli = get_collection()
# For each volume and subject iter and build the filename and update JSON
subjects = glob("sub*") # this globs finds the relative paths
volumes = ["brainmask.nii.gz","wm.nii.gz","aparc+aseg.nii.gz"]
for s in subjects:
    for v in volumes:
        t1=os.path.join(s,'T1.nii.gz')
        f=os.path.join(s,v)        
        entry_str=v.replace(".nii.gz",'').replace('+','')
        entry = {"entry_type":entry_str} # brainmask/aparc+aseg/wm
        if not coll.find({"subject_id":s,"entry_type":entry_str}).count():        
            print("adding", f)
            #"metrics":{"GMV": np.random.rand(), # metrics to be updated later
                #          "WMV": np.random.rand()}}
            entry["subject_id"] = s #need to be unique, subject exam id, fs id
            entry["name"] = s #needs to be uniquem, fs id
            entry["check_masks"] = [t1,f] # list of [T1, brainmask/wm/aparc+aseg]
            coll.insert_one(entry)
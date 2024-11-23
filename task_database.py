#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 10:55:49 2024

@author: pavel
"""

from datetime import datetime

columns = 'job_id', 'job_name',\
            'description',\
            'reward_amount',\
            'estimated_duration_minutes',\
            'difficulty_level','created_at'

task_database = [
    (0,'Washing Dishes', 'Clean all dishes in the sink, load/unload dishwasher, and wipe counters', 3.50, 20, 'Easy',datetime.now()),
    (1,'Mowing Lawn', 'Cut grass in front and back yard, trim edges, and clean up clippings', 10.00, 45, 'Hard',datetime.now()),
    (2,'Making Bed', 'Straighten sheets, arrange pillows, and smooth out comforter', 1.00, 5, 'Easy',datetime.now()),
    (3,'Vacuuming House', 'Vacuum all carpeted areas and rugs in the house', 5.00, 30, 'Medium',datetime.now()),
    (4,'Taking Out Trash', 'Collect trash from all bins, replace bags, and take to outdoor container', 2.00, 10, 'Easy',datetime.now())
]





import pandas as pd


df = pd.DataFrame(task_database,columns=columns)




def get_task(Id):
    
    
    s = df[df['job_id']==Id].iloc[0]
    
    s = None if len(s)==0 else s.to_dict()
    
    # dir(s['created_at'])
    
    if isinstance(s,dict):
        s['created_at'] = s['created_at'].to_pydatetime()
    # if 
    
    return s


if __name__=='__main__':
    
    resp = get_task(1)
    
    print(resp)
    
    s=resp


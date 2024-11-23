#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 10:55:49 2024

@author: pavel
"""

from datetime import datetime
import pandas as pd
import numpy as np


task_id = 2


columns = 'job_id', 'job_name',\
            'description',\
            'reward_amount',\
            'estimated_duration_minutes',\
            'difficulty_level','created_at',\
             'is_done',\
             'done_by'

task_database = [
    (0,'Washing Dishes', 'Clean all dishes in the sink, load/unload dishwasher, and wipe counters', 3.50, 20, 'Easy',datetime.now(),False,None),
    (1,'Mowing Lawn', 'Cut grass in front and back yard, trim edges, and clean up clippings', 10.00, 45, 'Hard',datetime.now(),False,None),
    (2,'Making Bed', 'Straighten sheets, arrange pillows, and smooth out comforter', 1.00, 5, 'Easy',datetime.now(),False,None),
    (3,'Vacuuming House', 'Vacuum all carpeted areas and rugs in the house', 5.00, 30, 'Medium',datetime.now(),False,None),
    (4,'Taking Out Trash', 'Collect trash from all bins, replace bags, and take to outdoor container', 2.00, 10, 'Easy',datetime.now(),False,None)
]







df = pd.DataFrame(task_database,columns=columns)#.set_index('job_id')
df
# fff


class TaskDatabase():
    
    def __init__(self):
        self.db = df
        pass

    
    
    def get_task(self,task_id : int):
        
        df = self.db
        
        s = df[df['job_id']==task_id].iloc[0]
        
        s = None if len(s)==0 else s.to_dict()
        
        # dir(s['created_at'])
        
        if isinstance(s,dict):
            s['created_at'] = s['created_at'].to_pydatetime()
        # if 
        
        return s
    
    
    def get_all_tasks(self):
        df = self.db
        return [s.to_dict for row_id,s in  df.iterrows()]
    
    
    def get_active_tasks(self):
        df = self.db
        return [s.to_dict for row_id,s in  df[df['is_done']==False].iterrows()]
    
    def mark_done(self,task_id: int):
        
        try:
            df = self.db
            
            # ix = np.where(df['job_id']==task_id)[0]
            
            ix = df.index[df['job_id']==task_id]
            
            df.at[ix,'is_done'] = True
            
            return 1
        except Exception as exc:
            print(exc)
            return 0
    
    
    
    






if __name__=='__main__':
    
    db = TaskDatabase()
    
    print(   db.get_active_tasks()   )


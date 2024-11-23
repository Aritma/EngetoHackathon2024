#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 10:55:49 2024

@author: pavel
"""

from datetime import datetime
import pandas as pd
import numpy as np





columns = 'task_id', 'job_name',\
            'description',\
            'reward_amount',\
            'estimated_duration_minutes',\
            'difficulty_level','created_at',\
             'is_done',\
             'done_by',\
             'done_at',\
             'waiting'

task_database = [
    (0,'Washing Dishes', 'Clean all dishes in the sink, load/unload dishwasher, and wipe counters', 35, 20, 'Easy',datetime.now(),False,None,None,None),
    (1,'Mowing Lawn', 'Cut grass in front and back yard, trim edges, and clean up clippings', 10, 45, 'Hard',datetime.now(),False,None,None,None),
    (2,'Making Bed', 'Straighten sheets, arrange pillows, and smooth out comforter', 10, 5, 'Easy',datetime.now(),False,None,None,None),
    (3,'Vacuuming House', 'Vacuum all carpeted areas and rugs in the house', 50, 30, 'Medium',datetime.now(),False,None,None,None),
    (4,'Taking Out Trash', 'Collect trash from all bins, replace bags, and take to outdoor container', 20, 10, 'Easy',datetime.now(),False,None,None,None)
]




len(columns)
len(task_database[0])




df = pd.DataFrame(task_database,columns=columns)#.set_index('task_id')
df


df['created_at'] = [s.to_pydatetime() for s in df['created_at']]



class TaskDatabase():
    
    def __init__(self):
        self.db = df
        pass

    
    
    def get_task(self,task_id : int) -> dict:
        '''vraci radek databaze domacich praci jako dict
        '''
        df = self.db
        
        s = df[df['task_id']==task_id].iloc[0]
        
        s = None if len(s)==0 else s.to_dict()
       
        
        return s
    
    
    def get_all_tasks(self) -> list:
        '''vraci vsechny radky (databaze domacich praci)
            jako list of dicts
        '''
        df = self.db
        return [s.to_dict() for row_id,s in  df.iterrows()]
    
    
    def get_active_tasks(self) -> list:
        '''vraci vsechny AKTIVNI radky (databaze domacich praci)
            jako list of dicts
        '''
        df = self.db
        return [s.to_dict() for row_id,s in  df[df['is_done']==False].iterrows()]
    
    def mark_done(self,task_id: int, kid_id: int = 0) -> int:
        '''oznaci task (podle task_id) jako done
            1...done
            0...failed
        '''

        df = self.db
        
        # ix = np.where(df['task_id']==task_id)[0]
        
        ix = df.index[df['task_id']==task_id]
        
        df.at[ix,'is_done'] = True
        

    
    
    def update(self, task: dict):
        '''update databaze
            vstup: task (dict)
            najde dany radek - vymaze ho - a appenduje vstup
            1...done
            0...failed
        '''
        
        print(task['task_id'])
        
        df = self.db
        print(df)
        df = df[~(df['task_id']==task['task_id'])]
        print(df)
        # task['done_at'] = datetime.now()
        
        
        df_new = pd.DataFrame([task],columns=columns)
        
        self.db = pd.concat([df,df_new])

        print(self.db)


    def waiting_rewards(self,days:int =4):
        
        df = self.db
        df

        ix = ~df['done_at'].isna()
        ix
        df.loc[ix]['done_at']
        ((pd.Timestamp('now')-df.loc[ix]['done_at']).values.astype(float))/1e9/3600
        
        
        # df = df[]
        
        df.loc[ix,'days'] = ((pd.Timestamp('now')-df.loc[ix]['done_at']).values.astype(float))/1e9/3600
        
        
        
        
        # (datetime.now()-df['done_at']).to_timedelta()
        
        
        df = df[df['days']>=4]
        
        return [s.to_dict() for ii,s in df.iterrows()]







if __name__=='__main__':
    
    db = TaskDatabase()
    self=db
    
    print(   db.get_all_tasks()   )
    
    print(   db.get_active_tasks()   )

    print(   db.get_task(1)   )


    print('-'*40)
    df=self.db
    df


    r = db.get_task(1) 
    r['is_done'] = True
    r['done_by'] = 2
    r['done_at'] = datetime.now()
    r
    task=r
    
    db.update(r)
    print('-'*40)

    df = db.db
    print(df)

    print(   db.waiting_rewards()   )
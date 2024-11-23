#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 10:55:49 2024

@author: pavel
"""

from datetime import datetime
import pandas as pd
import numpy as np

import sqlite3
import os
import re
db_file = 'kids_chores.db'




class TaskDatabase():
    
    def __init__(self):



        '''
        hardcoded database...
        '''
    
    

        self.columns = 'task_id', 'job_name',\
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
        
        
        len(self.columns)
        len(task_database[0])
        
        df = pd.DataFrame(task_database,columns=self.columns)#.set_index('task_id')
        df
        df['created_at'] = [s.to_pydatetime() for s in df['created_at']]
        
        self.db = df
    
    
    
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
        
        # print(task['task_id'])
        
        df = self.db
        # print(df)
        df = df[~(df['task_id']==task['task_id'])]
        # print(df)
        # task['done_at'] = datetime.now()
        
        
        df_new = pd.DataFrame([task],columns=self.columns)
        
        self.db = pd.concat([df,df_new])

        # print(self.db)


    def waiting_rewards(self,done_by: int, days:int =4):
        
        df = self.db
        df

        ix = ~df['done_at'].isna()
        ix
        df.loc[ix]['done_at']
        ((pd.Timestamp('now')-df.loc[ix]['done_at']).values.astype(float))/1e9/3600
        
        
        # df = df[]
        
        df.loc[ix,'days'] = ((pd.Timestamp('now')-df.loc[ix]['done_at']).values.astype(float))/1e9/3600
        
        
        
        
        # (datetime.now()-df['done_at']).to_timedelta()
        
        
        df = df[  (df['done_by']==done_by)  &  (df['days']>=days)  &  (df['waiting']==True)   ]
        
        return [s.to_dict() for ii,s in df.iterrows()]

#%%



class TaskDatabaseSQL():
    
    def __init__(self):
        self.db_file = db_file#'kids_chores.db'
        

        # if True:
            # os.remove(self.db_file)
            
        if not os.path.exists(self.db_file):
            
            conn = sqlite3.connect(self.db_file)
    
            '''
            hardcoded database...
            '''
            
            sql_query = """
            CREATE TABLE IF NOT EXISTS home_jobs (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_name TEXT NOT NULL,
                description TEXT,
                reward_amount INTEGER NOT NULL,
                estimated_duration_minutes INTEGER,
                difficulty_level TEXT CHECK(difficulty_level IN ('Easy', 'Medium', 'Hard')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_done BOOL DEFAULT FALSE,
                done_by INTEGER DEFAULT NULL,
                done_at TIMESTAMP DEFAULT NULL,
                waiting BOOL DEFAULT NULL
            );
            """
            
            
            # Read and execute the SQL file
            conn.executescript(sql_query)
            # conn.close()
            
            
            
            # -- Insert sample jobs
            sql_query = """INSERT INTO home_jobs (job_name, description, reward_amount, estimated_duration_minutes, difficulty_level)
            VALUES 
            """
            task_samples = [('Washing Dishes', 'Clean all dishes in the sink, load/unload dishwasher, and wipe counters', 35, 20, 'Easy'),
                            ('Mowing Lawn', 'Cut grass in front and back yard, trim edges, and clean up clippings', 10, 45, 'Hard'),
                            ('Making Bed', 'Straighten sheets, arrange pillows, and smooth out comforter', 10, 5, 'Easy'),
                            ('Vacuuming House', 'Vacuum all carpeted areas and rugs in the house', 50, 30, 'Medium'),
                            ('Taking Out Trash', 'Collect trash from all bins, replace bags, and take to outdoor container', 20, 10, 'Easy'),
                            ]
            
            # sql_query += '\n'
            for ij in range(3):
                for task in task_samples:
                    sql_query += "(" + ', '.join(["'%s'"% (str(s) if k>0 else str(s)+'%d'%ij) for k,s in enumerate(task)]) + "),\n"
            print(sql_query[-10:])
            sql_query = sql_query[:-2]+';'
            print(sql_query[-10:])
            
            # Read and execute the SQL file
            conn.executescript(sql_query)
            conn.close()

    
    def _query_to_dicts(self,query, params=()):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row  # This allows dict-like access to rows
        cursor = conn.cursor()


        query = 'SELECT * FROM home_jobs'
        params=[]
        cursor.execute(query, params)
        
        
        # sqlite3 
        # SQLite does not have a native TIMESTAMP data type. Instead, it stores TIMESTAMP values as TEXT, INTEGER, or REAL, 
        # --> 
        result=[]
        # Convert results to list of dicts
        for row in cursor.fetchall():
            d = dict(row)
            
            for d0 in d.keys():
                d
                if re.match('^\d{4}-\d{2}-\d{2}\s+\d{2}[:]\d{2}[:]\d{2}\.\d{6}$',str(d[d0])):
                    d0
                    d[d0] = datetime.strptime(d[d0],'%Y-%m-%d %H:%M:%S.%f')
                elif re.match('^\d{4}-\d{2}-\d{2}\s+\d{2}[:]\d{2}[:]\d{2}$',str(d[d0])):
                    d0
                    d[d0] = datetime.strptime(d[d0],'%Y-%m-%d %H:%M:%S')
                    
            d
                    
            result.append(d)
        
        
        
        # result = [dict(row) for row in cursor.fetchall()]
        return result

        conn.close()


    def get_all_tasks(self) -> list:

        resp = self._query_to_dicts('SELECT * FROM home_jobs')
        # print("\nAll jobs:")
        # for job in resp:
        #     print('%2d: %s' % (job['task_id'],job['job_name']))

        return resp
    
    def get_active_tasks(self) -> dict:
        resp = self._query_to_dicts('SELECT * FROM home_jobs WHERE is_done = FALSE')
        
        # print("\nActive jobs:")
        # for job in resp:
        #     print('%2d: %s' % (job['task_id'],job['job_name']))

        return resp


    def get_task(self, task_id: int) -> dict:

        resp = self._query_to_dicts('SELECT * FROM home_jobs WHERE task_id = ?', (task_id,))


        return resp[0]


    def _delete_job_by_id(self,task_id: int):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row  # This allows us to access columns by name
        cursor = conn.cursor()
        

        # Get job details
        cursor.execute('SELECT * FROM home_jobs WHERE task_id = ?', (task_id,))
        job = cursor.fetchone()
        
        
        
        if job:
        
            cursor.execute('DELETE FROM home_jobs WHERE task_id = ?', (task_id,))
            conn.commit()
            print(f"Successfully deleted job: {job['job_name']}")
            
        else:
            print(f"No job found with ID {task_id}")
            return False
                
        conn.close()



    
    def update(self,task_dict: dict):
        task_id = task_dict.get('task_id')
        # print(task_id)
        
        # task_id=1
        self._delete_job_by_id(task_id)
        

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Prepare the INSERT statement
        query = '''
            INSERT INTO home_jobs 
            (job_name, description, reward_amount, estimated_duration_minutes, difficulty_level,is_done,done_by,done_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        # Get values from dictionary
        values = (
            task_dict.get('job_name'),
            task_dict.get('description'),
            task_dict.get('reward_amount'),
            task_dict.get('estimated_duration_minutes'),
            task_dict.get('difficulty_level'),
            task_dict.get('is_done'),
            task_dict.get('done_by'),
            task_dict.get('done_at'),
            
        )
        
    
        cursor.execute(query, values)
        conn.commit()
        # print(f"Successfully added job: {job_dict['job_name']}")
        
        conn.close()
        
        # Return the id of the newly inserted row
        return cursor.lastrowid



    def waiting_rewards(self,done_by: int , days: int = 4):

        resp = self._query_to_dicts('SELECT * FROM home_jobs WHERE waiting = ?', (True,))

        # resp = self._query_to_dicts('SELECT * FROM home_jobs')
        # r=resp[-1]
        # r
        # done_by=2
        # td = (datetime.now() - datetime.strptime(r['done_at'],'%Y-%m-%d %H:%M:%S.%f'))
        # datetime.strptime('%Y-%m-%d %H:%M:%S.%f',r['done_at'])


        # (datetime.now() - r['done_at'])
        resp = [r for r in resp if (r['done_by']==done_by) and ((datetime.now() - r['done_at']).days>=days)]

        return resp





#%%



if __name__=='__main__':
    print('='*80)
    db = TaskDatabase()
    self=db
    
    print(   db.get_all_tasks()   )
    
    print(   db.get_active_tasks()   )

    print(   db.get_task(1)   )


    print('-'*40)
    df=self.db
    df

    task_ids = [r['task_id'] for r in db.get_all_tasks() ]
    task_id = task_ids[0]

    print('-'*40)
    r = db.get_task(task_id) 

    r = db.get_task(task_id) 
    r['is_done'] = True
    r['done_by'] = 2
    r['done_at'] = datetime.now()
    r['waiting'] = True
    r
    task=r
    
    db.update(r)
    print('-'*40)

    df = db.db
    print(df)

    print('-'*40)
    print(   db.waiting_rewards(2)   )




#%%============================================================================

if __name__=='__main__':
    print('='*80)
    db = TaskDatabaseSQL()
    self=db
    
    
    r = db.get_all_tasks() 
    r[0]['created_at']
    
    
    
    # wevwev
    # print(   db.get_all_tasks()   )
    
    # print(   db.get_active_tasks()   )

    # print(   db.get_task(1)   )


    task_ids = [r['task_id'] for r in db.get_all_tasks() ]
    task_id = task_ids[0]

    print('-'*40)
    r = db.get_task(task_id) 
    r['is_done'] = True
    r['done_by'] = 2
    r['done_at'] = datetime.now()
    task_dict=r
    
    db.update(r)

    print('-'*40)
    print(   db.waiting_rewards(2)   )


    # df = db.db
    # print(df)
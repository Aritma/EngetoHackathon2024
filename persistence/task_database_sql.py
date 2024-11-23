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



class TaskDatabaseSQL():
    
    def __init__(self):
        self.db_file = db_file
        if not os.path.exists(self.db_file):
            conn = sqlite3.connect(self.db_file)
            #hardcoded database...
            
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
            conn.executescript(sql_query)
            
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
            
            sql_query = sql_query[:-2]+';'
            
            conn.executescript(sql_query)
            conn.close()


    def _query_to_dicts(self,query, params=()):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row  # This allows dict-like access to rows
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        
        # SQLite does not have a native TIMESTAMP data type. Instead, it stores TIMESTAMP values as TEXT, INTEGER, or REAL, 
        result=[]
        # Convert results to list of dicts
        for row in cursor.fetchall():
            d = dict(row)
            
            for d0 in ['created_at','done_at']: #d.keys():
                d
                if re.match('^\d{4}-\d{2}-\d{2}\s+\d{2}[:]\d{2}[:]\d{2}\.\d{6}$',str(d[d0])):
                    d0
                    d[d0] = datetime.strptime(d[d0],'%Y-%m-%d %H:%M:%S.%f')
                elif re.match('^\d{4}-\d{2}-\d{2}\s+\d{2}[:]\d{2}[:]\d{2}$',str(d[d0])):
                    d0
                    d[d0] = datetime.strptime(d[d0],'%Y-%m-%d %H:%M:%S')
                    
            d
            
            result.append(d)
        
        conn.close()
        return result

        

    def get_all_tasks(self) -> list:
        resp = self._query_to_dicts('SELECT * FROM home_jobs')
        return resp
    
    def get_active_tasks(self) -> dict:
        resp = self._query_to_dicts('SELECT * FROM home_jobs WHERE is_done = FALSE')
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
            conn.close()
            print(f"Successfully deleted job: {job['job_name']}")
            
        else:
            print(f"No job found with ID {task_id}")
            conn.close()
            return False
                
        



    
    def update(self,task_dict: dict):
        task_id = task_dict.get('task_id')
        keys = ['is_done','done_at','done_by','waiting']
        set_values = ', '.join([f"{key} = ?" for key in keys])

        query = f'UPDATE home_jobs SET {set_values} WHERE task_id = ?'
        
        values = tuple([task_dict[k] for k in keys] + [task_id,])
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute(query, values)
        conn.commit()
        
        if cursor.rowcount > 0:
            print({k:task_dict[k] for k in (['task_id',]+keys)})
            print(f"Successfully updated job {task_id}")
            return True
        else:
            print(f"No job found with ID {task_id}")
            return False



    def waiting_rewards(self,done_by: int , days: int = 4):
        resp = self._query_to_dicts('SELECT * FROM home_jobs WHERE waiting = ?', (True,))
        resp = [r for r in resp if (r['done_by']==done_by) and ((datetime.now() - r['done_at']).days>=days)]
        return resp





#%%




#%%============================================================================

if __name__=='__main__':
    print('='*80)
    
    os.remove(db_file)
    
    
    db = TaskDatabaseSQL()
    self=db
    
    
    r = db.get_all_tasks() 
    r[0]['created_at']
    
    
    
    # wevwev
    # print(   db.get_all_tasks()   )
    
    # print(   db.get_active_tasks()   )

    # print(   db.get_task(1)   )



    print('-'*40)
    task_ids = [r['task_id'] for r in db.get_all_tasks() ]
    task_id = task_ids[1]
    print(task_id)

    print('-'*40)
    
    
    
    r = db.get_task(task_id) 
    
    print( {k:r[k] for k in ['task_id']})
    
    
    r['is_done'] = True
    r['done_by'] = 2
    r['done_at'] = datetime.now()
    task_dict=r
    
    
    
    
    
    db.update(r)

    print('-'*40)
    print(   db.waiting_rewards(2)   )


    # df = db.db
    # print(df)
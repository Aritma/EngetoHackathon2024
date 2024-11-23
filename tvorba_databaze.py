#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 10:18:22 2024

@author: pavel
"""

from datetime import datetime
import sqlite3
import os

db_file = 'kids_chores.db'
os.remove(db_file)





#%%
class TaskDatabase():
    
    def __init__(self):
        self.db_file = db_file#'kids_chores.db'
        
        
        conn = sqlite3.connect(self.db_file)

        
        
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
            done_at TIMESTAMP DEFAULT NULL
        );
        """
        
        
        # Read and execute the SQL file
        conn.executescript(sql_query)
        # conn.close()
        
        
        
        # -- Insert sample jobs
        sql_query = """INSERT INTO home_jobs (job_name, description, reward_amount, estimated_duration_minutes, difficulty_level)
        VALUES 
            ('Washing Dishes', 'Clean all dishes in the sink, load/unload dishwasher, and wipe counters', 35, 20, 'Easy'),
            ('Mowing Lawn', 'Cut grass in front and back yard, trim edges, and clean up clippings', 10, 45, 'Hard'),
            ('Making Bed', 'Straighten sheets, arrange pillows, and smooth out comforter', 10, 5, 'Easy'),
            ('Vacuuming House', 'Vacuum all carpeted areas and rugs in the house', 50, 30, 'Medium'),
            ('Taking Out Trash', 'Collect trash from all bins, replace bags, and take to outdoor container', 20, 10, 'Easy');
        """
        
        # Read and execute the SQL file
        conn.executescript(sql_query)
        conn.close()

    
    def _query_to_dicts(self,query, params=()):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row  # This allows dict-like access to rows
        cursor = conn.cursor()

        cursor.execute(query, params)
        # Convert results to list of dicts
        result = [dict(row) for row in cursor.fetchall()]
        return result

        conn.close()


    def get_all_tasks(self) -> list:

        resp = self._query_to_dicts('SELECT * FROM home_jobs')
        print("\nAll jobs:")
        for job in resp:
            print('%2d: %s' % (job['task_id'],job['job_name']))

        return resp
    
    def get_active_tasks(self) -> dict:
        resp = self._query_to_dicts('SELECT * FROM home_jobs WHERE is_done = FALSE')
        
        print("\nActive jobs:")
        for job in resp:
            print('%2d: %s' % (job['task_id'],job['job_name']))

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


    

# # Example usage:
# # Delete with confirmation
# delete_job_by_id(1)

# # Delete without confirmation
# delete_job_by_id(2, confirm=False)






# # Example usage:
# job = get_exact_job_by_name("Mowing Lawn")
# if job:
#     print(f"Found: {job['job_name']} - ${job['reward_amount']}")
    

#%%============================================================================

if __name__=='__main__':
    
    db = TaskDatabase()
    self=db
    
    print(   db.get_all_tasks()   )
    
    print(   db.get_active_tasks()   )

    print(   db.get_task(1)   )

    r = db.get_task(1) 
    r['is_done'] = True
    r['done_by'] = 2
    r['done_at'] = datetime.now()
    task_dict=r
    
    db.update(r)


    # df = db.db
    # print(df)

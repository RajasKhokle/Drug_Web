# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 08:14:44 2019
Purpose: Connect to the AWS Drug Database
@author: Rajas Khokle
"""

import pandas as pd
from sqlalchemy import create_engine


# Create Connection to the database

engine = create_engine('postgres://raj_dbadmin:raj_drug_2019@drug-db.c6jct1xqezn1.ap-southeast-2.rds.amazonaws.com:5454/diabetes')

df = pd.read_csv('P:\GA Capstone\Health Forcast\Capstone Deliverables\Tableau\Capstone.csv')

df.to_sql('df',engine,if_exists = 'append',index=True)
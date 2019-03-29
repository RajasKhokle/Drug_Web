# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 08:14:44 2019
Purpose: Connect to the Postgresql Drug Database on local virtual machine on UBUNTU
@author: Rajas Khokle
"""

import pandas as pd
from sqlalchemy import create_engine


# Create Connection to the database

engine = create_engine('postgres://postgres:raj_drug_2019@10.37.17.10:5432/diabetes')

df = pd.read_csv('P:\GA Capstone\Health Forcast\Capstone Deliverables\Tableau\Capstone.csv')

df.to_sql('df',engine,if_exists = 'append',index=True)
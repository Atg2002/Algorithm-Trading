# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 19:02:06 2022

@author: Krithikavvgreat
"""

import pandas as pd

url = "https://www.xe.com/currencycharts/"
tables = pd.read_html(url)

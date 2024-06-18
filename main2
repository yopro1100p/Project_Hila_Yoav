"""
this main file is in order to print all we got untill now 
"""
import time

import h5py
import matplotlib.pyplot as plt
import McsPy
import numpy as np
import pandas as pd

import Chanels

# file_path = "C:/Users/user/Desktop/bar ilan/Forth year/project/your_file.h5" #yoav's link 
file_path = "C:/Users/dvirg/OneDrive/Desktop/toar1/year4/project/CODE/your_file.h5" #hilla's link
electrode= 13
analyzer = Chanels.ChannelAnalyzer(file_path, electrode)
print(f"for electrode num {electrode}")
# analyzer.group_spikes()
# print(f"the group of all point that over the threshhold in the time thy appeerd {analyzer.group_of_spikes}")
# analyzer.find_max_in_groups()
# print(f"the max in each group is the the spike himself, the spikes value: {analyzer.max_values}")
#print(f"the amplitude of the spikes for this electrod: {analyzer.find_Average_Spikes()}")
#print(f"the time between each spikes is: {analyzer.finding_Spikes_Samples_rate()}")
print(f"the average rate between every spikes is: {analyzer.find_the_avarage_rate_between_spikes()} miue sec")
print(f"the num of spikes in the electrode: {analyzer.find_num_of_spikes()} ")
print(f"the berst by min num of spike=2 and max dist= 5: {analyzer.find_burst(6,2)}")
print(f"the num of the berst  by min num of spike=2 and max dist= 5: {analyzer.find_num_of_berst(6,2)}")


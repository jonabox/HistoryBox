#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 22:59:23 2018

@author: jonabox
"""

import numpy as np

def unit_vector(vector):
    return vector/ np.linalg.norm(vector)

def angle_between(v1, v2):
    
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    
    return np.arccos(np.clip(np.dot(v1_u, v2_u.T), -1.0, 1.0))

def get_most_similar(userId, userBase):
    
    user = userBase[userId] 

    neighbors = np.vstack((userBase[:userId], userBase[userId + 1:]))
    
    return np.argmin([angle_between(user, neighbor) for neighbor in neighbors])
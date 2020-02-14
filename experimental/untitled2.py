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


v1 = np.array([[1,0,0]])
v2 = np.array([[-1,0,0]])

print(v1)
print(v2)
print(angle_between(v1,v2)[0][0])
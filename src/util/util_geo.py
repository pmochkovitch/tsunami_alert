# -*- coding: utf8 -*-
from __future__ import unicode_literals
__author__ = 'tsunami_team'
"""
Util geo functions
"""

import pandas as pd
from geopy.distance import vincenty


"******************************************************************************************"
csv_gsm_coord = '../../dataset/GSM_Coord.csv'
csv_nodes_locations = '../../dataset/Nodes_locations.csv'
"******************************************************************************************"


"""
Transform longitude & latitude into (longitude,latitude)
"""
def calc_coord(row):
    row['coordinates'] = (row['latitude'], row['longitude'])
    return row


"""
Calculate distance between seism and a given coordinate
"""
def get_distance_to_seism(row, impact_coordinates):
    row['dist_from_seism'] = vincenty(row['coordinates'], impact_coordinates).miles
    return row


"""
Get all the GSM codes near the epicentre
"""
def get_GSM_codes_close_to_impact(latitude, longitude, km_range):
    GSMZone_dist = pd.read_csv(csv_gsm_coord)
    impact_coord = (latitude, longitude)
    GSMZone_dist = GSMZone_dist.apply(lambda x : get_distance_to_seism(x, impact_coord), axis=1)
    GSMZone_dist = GSMZone_dist.sort(['dist_from_seism'],ascending=1)
    GSMZone_dist_500 = GSMZone_dist[GSMZone_dist['dist_from_seism'] <= km_range]
    return GSMZone_dist_500


"""
Get the id of the closest node to impact
"""
def get_node_close_to_impact_id(latitude, longitude, km_range, switch):
    Node_dist_to_impact = pd.read_csv(csv_nodes_locations, sep =";")
    impact_coord = (latitude, longitude)
    Node_dist_to_impact = Node_dist_to_impact.apply(lambda x : calc_coord(x), axis=1)
    Node_dist_to_impact = Node_dist_to_impact.apply(lambda x : get_distance_to_seism(x, impact_coord), axis=1)
    Node_dist_to_impact = Node_dist_to_impact.sort(['dist_from_seism'],ascending=1).reset_index(drop=True)
    Closest_node_id = str(Node_dist_to_impact.ix[switch]['Node_id'])
    Closest_node = str(Node_dist_to_impact.ix[switch]['Node'])
    return Closest_node_id, Closest_node
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 08:35:19 2021

@author: julio
"""

from bs4 import BeautifulSoup#biblioteca con utlidades para manipulacion y lectura de archivos xml

# Funcion para parsear archivo de seiscomp xml, devuelve una lista con las picadas de fase que se extraen del xml
# se extrae informacion importante como el codigo de estacion el tiempo de arribo de las fases sismicas
# se utilza en seicomp_to_nordic.py
def xml_station_list(xml_file_path):
    f=open(xml_file_path,'r')
    data=f.read()
    xml_data=BeautifulSoup(data,'xml')
    #origins=xml_data.find_all('origin')
    #print(origins)
    
    #origin_ID='Origin/20210504185033.563186.3844'
    
    desired_origin=xml_data.find('EventParameters')#,{'publicID':origin_ID})
    
    arrivals=desired_origin.find_all('pick')
    
    station_list=[]
    #print(arrivals[0])
    for i in range(len(arrivals)):
        #pickID=arrivals[i].find('publicID')
        pickID=arrivals[i].get('publicID')
        pickID_list=pickID.split('.')
        year   =pickID[0:4]
        month  =pickID[4:6]
        day    =pickID[6:8]
        hour   =pickID[9:11]
        minute =pickID[11:13]
        seconds=pickID[13:18]
        station=pickID_list[len(pickID_list)-3]
        channel=pickID_list[len(pickID_list)-1][2]
        instrument=pickID_list[len(pickID_list)-1][0:2]
        phase=arrivals[i].find('phaseHint').string
        #azimuth=arrivals[i].find('azimuth').string
        #time_residual=arrivals[i].find('timeResidual').string
        #distance=arrivals[i].find('distance').string
        #weight=arrivals[i].find('weight').string
        station_list.append([station,       #0
                             channel,       #1
                             instrument,    #2
                             year,          #3
                             month,         #4
                             day,           #5
                             hour,          #6
                             minute,        #7
                             seconds,       #8
                             phase])#,         #9
       #                      azimuth,       #10
       #                      time_residual, #11
       #                      distance,      #12
       #                      weight])       #13
    return station_list


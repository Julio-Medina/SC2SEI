#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 16:15:34 2021

@author: julio
"""
# Funcion para parsear archivo de seiscomp xml, devuelve una lista con las picadas de fase que se extraen del xml
# se extrae informacion importante como el codigo de estacion el tiempo de arribo de las fases sismicas
# se utilza en seicomp_to_nordic.py
# se modifico para utlizar libreria xml.etree.ElementTree ya que es mas estandar

import xml.etree.ElementTree as ET

def xml_station_list(xml_file_path):
    
    tree=ET.parse(xml_file_path)#arbol con la estructura xml
    root=tree.getroot()# se obtiene la etiqueta raiz del xml
    eventParameters=root[0]#root de xml generados por seiscomp
    name_space={'seiscomp':root.tag[1:len(root.tag)-9]}#namespace definido por seiscomp {http://geofon.gfz-potsdam.de/ns/seiscomp3-schema/0.11} 
    arrivals=eventParameters.findall('seiscomp:pick',name_space)#tags con las picadas de fase 
    station_list=[]#se inicializa la lista de estaciones que se dara de resultado
   
    for i in arrivals:
        time=i.find('seiscomp:time',name_space).find('seiscomp:value',name_space).text
        year   =time[0:4]#año del evento
        month  =time[5:7]#mes del evento
        day    =time[8:10]#dia del evento
        hour   =time[11:13]#hora del evento
        minute =time[14:16]# minuto de llegada de fase
        seconds=time[17:22]# segundo de llegada de fase
        if seconds[len(seconds)-1]=='Z':
            seconds=seconds[:len(seconds)-1]+'0'
        station=i.find('seiscomp:waveformID',name_space).get('stationCode')
        channel=i.find('seiscomp:waveformID',name_space).get('channelCode')[2]
        instrument=i.find('seiscomp:waveformID',name_space).get('channelCode')[:2]
        phase=i.find('seiscomp:phaseHint',name_space).text#fase detectada
        station_list.append([station,       #0
                             channel,       #1
                             instrument,    #2
                             year,          #3
                             month,         #4
                             day,           #5
                             hour,          #6
                             minute,        #7
                             seconds,       #8
                             phase])        #9
    return station_list


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 12:42:53 2021

@author: julio
"""
# Script that takes a wav file i.e a .mseed and generates data to feed  a neural network called SeismicNet
# it is based on the data acquisition scripts used for the development of SeismicNet https://github.com/Julio-Medina/SeismicNet
# The predictions of SesimicNet are going to be used to expand the SC2SEI project https://github.com/Julio-Medina/SC2SEI
# currently working on a branch called Phase_S

from obspy import read as readStream#objeto para leer formas de onda, WAV files
from obspy import read_events#objeto para leer Eventos
import os #  objeto para crear lista de archivos en una carpeta
import math #biblioteca con funciones matematicas
import numpy as np #biblioteca para computacion cientifica
import pickle#objeyo para guardar archivos de objetos en txt


def RAW_data_acquisition(wave_file_path, outputX_file, sample_dimension, pick_channel):
    
    
    wave_form_list=[]
    station_list=[]
    channel_list=[]
    wave_stream=readStream(wave_file_path)
    #print(len(wave_stream))
    #print(wave_stream.__str__(extended=True))
    wave_stream.merge(method=1)
    #print(wave_stream.__str__(extended=True))
    print(len(wave_stream))
    for wave_form in wave_stream:
        if  (((wave_form.stats.endtime-wave_form.stats.starttime)!=0) and 
            (wave_form.stats.channel[2]==pick_channel)):#and
            #(wave_form.stats.station not in station_list)):
            #print(wave_form.stats.channel[1:3])
            ##########################################################################################
            #REGULARIZACION Y NORMALIZACION de Datos
            
            #REGULARIZACION
            #Rutina que remuestrea las formas de onda, se asegura que todos los datos tengan 3000 puntos
            
            aux=0
            while (wave_form.stats.npts!=sample_dimension):#se asegura que el numero de datos sea 3000
                wave_form.resample(wave_form.stats.sampling_rate/(wave_form.stats.npts/(sample_dimension+aux)))
                aux+=0.1
            ###########################################################################################
            #NORMALIZACION
            #se normalizan los datos como (X-mean)/(max-min), convencion de machine learning
            normalized_data=(wave_form.data-wave_form.data.mean())/(wave_form.data.max()-wave_form.data.min())# se normalizan los datos para que el entrenamiento convega
            #datos de mseed para predecir fases S
            wave_form_list.append(normalized_data)
            station_list.append(wave_form.stats.station)
            channel_list.append(wave_form.stats.channel)
           
    return np.array(wave_form_list), station_list, channel_list

C, D, E= RAW_data_acquisition('/home/julio/Documents/SC2SEI/project1/20052021/SC2SEI/insivumeh2021joxb.mseed',
                           '', 3000, 'E')
    
    
    
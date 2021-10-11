#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 12:45:13 2021

@author: julio
"""
import tensorflow as tf
import numpy as np
#import pickle
#import os
from scipy.signal import find_peaks
from WAV_data_acquisition import RAW_data_acquisition
#import matplotlib.pyplot as plotTrace



def phase_S_picker(wave_forms, start_time_list, event_time_lapse_list, dimension_sample, SeismicNet_model_path):
    wave_form_number=len(wave_forms)
    model=tf.keras.models.load_model(SeismicNet_model_path+'SeismicNet.h5')
    wave_forms_data_set=np.expand_dims(wave_forms, axis=2)
    phase_S_arrival_time_list=[]
    for i in range(wave_form_number):
        predictions=model.predict(np.expand_dims(wave_forms_data_set[i],axis=0))
        
        predictions_distributions=np.transpose(predictions[0])
                
        #se identifican las distribuciones dadas por la red neuronal con las fases sismicas
        phase_P=predictions_distributions[0]
        phase_S=predictions_distributions[1]
        #noise=predictions_distributions[2]


        #se hallan maximos de distribuciones de probabilidad
        peaks_P, peakdic1=find_peaks(phase_P,distance=35)
        peaks_S, peakdic2=find_peaks(phase_S,distance=35)
        
        peak_P_list=phase_P[peaks_P]#lista de maximos dist. probabilidad fase P
        sorted_peak_P_list=np.sort(peak_P_list) #lista de maximos ordenada
        peak_value_P=sorted_peak_P_list[len(sorted_peak_P_list)-1] #valor maximo P
        
        peak_S_list=phase_S[peaks_S]
        sorted_peak_S_list=np.sort(peak_S_list)
        peak_value_S=sorted_peak_S_list[len(sorted_peak_S_list)-1]
        
        # posiciones de maximos fase P en serie
        peak_P_value_positions,=np.where(np.isclose(phase_P,peak_value_P))
        # posiciones de maximos fase S en serie
        peak_S_value_positions,=np.where(np.isclose(phase_S,peak_value_S))
        
        prediction_p_phase_position=peak_P_value_positions[0]
        prediction_s_phase_position=peak_S_value_positions[0]
        
        if prediction_p_phase_position>prediction_s_phase_position:
            aux=prediction_p_phase_position
            prediction_p_phase_position=prediction_s_phase_position
            prediction_s_phase_position=aux
        
        phase_S_arrival_time=start_time_list[i]+prediction_s_phase_position*event_time_lapse_list[i]/dimension_sample
        phase_S_arrival_time_list.append(phase_S_arrival_time)
        
    
    return phase_S_arrival_time_list

def station_list_phase_S(station_list, channel_list, phase_S_arrival_time_list):
    aux_list=[]
    for i in range(len(station_list)):
        aux_list.append([station_list[i],                               #0 estacion
                         channel_list[i],                               #1 tipo de instrumento y canal e.g. HHE
                         str(phase_S_arrival_time_list[i].hour),        #2 hora del arribo de fase S
                         str(phase_S_arrival_time_list[i].minute) if len(str(phase_S_arrival_time_list[i].minute))==2  else '0'+str(phase_S_arrival_time_list[i].minute),      #3 minuto del arribo de fase S
                         (str(phase_S_arrival_time_list[i].second) if len(str(phase_S_arrival_time_list[i].second))==2  else '0'+str(phase_S_arrival_time_list[i].second))+'.'+str(phase_S_arrival_time_list[i].microsecond)[0:2]])     #4 segundo del arribo de fase S
    return aux_list
        

#C, D, E, F ,G= RAW_data_acquisition('/home/julio/Documents/SC2SEI/project1/20052021/SC2SEI/insivumeh2021joxb.mseed',
                           '', 3000, 'E')

#phase_S_arrival_time_list=phase_S_picker(C,F,G,3000,'/home/julio/Documents/NeuralNetworks/2021/models/SeismicNet/')

#final_list=station_list_phase_S(D, E, phase_S_arrival_time_list)

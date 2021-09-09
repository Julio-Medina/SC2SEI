#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 12:45:13 2021

@author: julio
"""
import tensorflow as tf
import numpy as np
import pickle
import os
from scipy.signal import find_peaks
import matplotlib.pyplot as plotTrace



def phase_P_picker(wave_forms, SeismicNet_model_path):
    wave_form_number=len(wave_forms)
    model=tf.keras.models.load_model(SeismicNet_model_path+'SeismicNet.h5')
    wave_forms_data_set=np.expand_dims(wave_forms, axis=2)
    
    for i in range(wave_form_number):
        predictions=model.predict(np.expand_dims(wave_forms_data_set[i],axis=0))
        
        predictions_distributions=np.transpose(predictions[0])
       
        
       
        #se identifican las distribuciones dadas por la red neuronal con las fases sismicas
        phase_P=predictions_distributions[0]
        phase_S=predictions_distributions[1]
        noise=predictions_distributions[2]


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
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 13:04:40 2021

@author: julio
based on: seiscomp_to_nordic.py
added on git repository on  Sun Sep 05 12:10:00 2021
"""
# Programa para convertir un boletin de seiscomp acompañado del xml correspondie
# a formato nordic, este el formato utilizado por SEISAN en los S-Files
# los S-files constituyen la unidad de almacenamiento fundamental de SEISAN
# La definicion de nordic se puede hallar en el Apendice A del manual de SEISAN



#import os
from shutil import copyfile #biblioteca para manejo de archivo, especificamente copiar archivos
from seiscomp_xml_parser import xml_station_list #PARSER XML
import os # bliblioteca para utlidades de manejo de archivos


#funcion para agregar espacios en blanco a un string de una longitud determinada
#se agregan los espacios al principio del string s

def add_blank(s, length):
    aux=s
    if len(s)<length:
        aux="{:>"+str(length)+ "}"
        aux=aux.format(s)
    return aux


#funcion para agregar espacios al final de un string de una longitud determinada
def add_blank_suffix(s, length):
    aux=s
    if len(s)<length:
        aux="{:<"+str(length)+ "}"
        aux=aux.format(s)        
    return aux
    
#funcion para determinar la posicion de un elemento dentro de una lista de listas
def find_in_sublists(lst, value):
    for sub_i, sublist in enumerate(lst):
        try:
            return (sub_i, sublist.index(value))
        except ValueError:
            pass

    raise ValueError('%s is not in lists' % value)   
        


#sfile_name='/home/julio/Documents/project1/03-1925-42L.S202105'
#files_path='/home/julio/Documents/project1/'# directorio de trabajo
#seiscomp_file_name='insivumeh2021jfvi.txt'#nombre del boletin generado en seiscomp
#wav_file_name='insivumeh2021jfvi.mseed' #nombre del archivo wav al que apunta el s-file
#xml_file_name='insivumeh2021jfvi.xml' #xml generado por seiscomp, en este xml se tiene informacion de las arribos de ondas sismicas

def seiscomp_to_nordic(files_path,
                       seiscomp_file_name,
                       wav_file_name,
                       xml_file_name):
    
    seiscomp_file=open(files_path+seiscomp_file_name,'r') #se lee el archivo del boletin
    seiscomp_file_lines=seiscomp_file.readlines() # se leen las lineas del boletin de seiscomp
    station_list_start=False # flag para determinar si se empiezan a leer picadas de fase
    #station_list_header=False
    station_list=[]# lista de estacione en el evento sismico
    magnitude='Null'#valor temporal que indica que no se ha medido magnitud del evento sismico
    depth=''
    residual_RMS=''
    for line in seiscomp_file_lines:# se itera a traves de las lineas del boletin con el fin de extraer informacion del evento
        
        if line.find('Date')!=-1: #se extrae la fecha del evento sismico
            year=line[27:31] # se lee el año
            month=line[32:34]# se lee el mes
            day=line[35:37]# se lee el dia
            
        if line.find('Time')!=-1: # se lee la hora del evento sisimico
            hour=line[27:29]      # se lee la hora del evento sismico
            minute=line[30:32]    # se leen los minutos del evento sismico
            seconds=line[33:37]   # se leen los segundos del evento sismico
            
        if line.find('Latitude')!=-1: # se lee la latitud del evento sismico
            latitude=line[27:33]     
        if line.find('Longitude')!=-1: # se lee la longitud del evento sismico
            longitude=line[27:33]
            
        if line.find('Depth')!=-1: #se lee la profundidad del evento sismico
            depth=line[31:33]
            
        if line.find('Agency')!=-1:# se lee informacion de la agencia sismica
            agency=line[27:30]
        
        if line.find('Residual')!=-1: # se lee la informacion del rms
           # print('test')
            residual_RMS=line[29:33]
           # print(line[29:33])
        
        #if (line.find('ML')!=-1)and(line.find('MLv')==-1) and (magnitude=='Null'): # see lee la magnitud
        #    magnitude=line[14:18]
        
        if ((line.find('MLv')!=-1)or (line.find('Mw')!=-1)) and (line.find('Preferred')==-1) and (magnitude=='Null'): # see lee la magnitud
            magnitude=line[14:18]
            
        if line.find('Public ID')!=-1: #id que sirve para identificar el origin utlizado por seiscomp para hallar el origen del evento sismico
            public_ID=line[27:60]
        
        
        station_list_header=False     # se ha encontrado el header de las picadas de fase 
        if ((line.find('sta')!=-1)and(line.find('net')!=-1)and line.find('dist')!=-1 )and (len(station_list)==0):
            station_list_start=True
            station_list_header=True
        
        if station_list_start and not station_list_header: # se extrae de las picadas de fase
            station=line[4:9] #codigo de estacion
            pick_hour=line[33:36] # hora de la llegada de fase
            pick_minute=line[36:39] # minuto de la llegada de fase
            pick_seconds=line[39:44]# segundo de la llegada de fase
            res=line[45:49]         #residual
            pick_mode=line[50:51]   #tipo de fase(P o S)
            distance=line[16:19]    #distacia del sismo
            weight=line[53:56]      #peso para la incerteza de la picada de fase
            azimuth=line[20:23]     #angulo azimutal
            
            if (station not in station_list) and (station!=''):# no se tiene a la estacion en el listado de estaciones con picadas de fase
                station_list.append([station,           #0
                                     pick_hour,         #1
                                     pick_minute,       #2
                                     pick_seconds,      #3
                                     res,               #4
                                     distance,          #5
                                     weight,            #6
                                     pick_mode,         #7
                                     azimuth])          #8
            if station=='':
                station_list_start=False
    

    #################################################################################################################
    # se utliza funcion creada en seiscomp_xml_parser para parsear el xml para extraer informacion de las estaciones con picada de fase 
    station_list_xml=xml_station_list(files_path+xml_file_name) 

            
    station_number=str(len(station_list_xml))# numero de estaciones encontradas
    
    
    
    #depth=add_blank(depth,5)
    station_number=add_blank(station_number,3)
    residual_RMS=add_blank(residual_RMS, 4)
    #magnitude=add_blank(magnitude)
    
    
    #station_number=add_blank(station_number,3)
     
    float_magnitude=float(magnitude)
    magnitude=f"{float_magnitude:.1f}"     
    magnitude=add_blank(magnitude,4)
    #s_file=open(sfile_name,'r')
    #s_file_lines=s_file.readlines()
    
    residual_RMS_float=float(residual_RMS)
    residual_RMS=f"{residual_RMS_float:.1f}"
    
    residual_RMS=add_blank(residual_RMS, 4)
    
    ###############################################################################################################
    # se crea la primera linea del s-file, el header
    if month[0]=='0':
        month_aux=' '+month[1]
    
    s_file_header=' '+year+' '+month_aux+day+' '+hour+minute+' '+seconds+' L '+add_blank(latitude+'0',7)+add_blank(longitude+'0',8)+add_blank(depth+'.0',5)
    s_file_header=s_file_header+'  '+agency+station_number+residual_RMS+magnitude+'L'+agency
    
    
    s_file_header=add_blank_suffix(s_file_header,79)+'1'
    
    ###############################################################################################################
    # se crea la linea del s-file que contiene el nombre del wav-file(forma de onda)
    seisan_wav_name=year+'-'+month+'-'+day+'T'+hour+':'+minute+':'+seconds[0:2]+'.MSEED'
    #copyfile(files_path+wav_file_name,files_path+'/seisan_output/'+seisan_wav_name)
    
    wav_file_location_line=' '+seisan_wav_name
    wav_file_location_line=add_blank_suffix(wav_file_location_line,79)+'6'
    
    
    sfile_name=day+'-'+hour+minute+'-'+seconds[0:2]+'L.S'+year+month
    
    ###############################################################################################################
    # se crea el header que identifica al listado de picadas de fase sismicas
    
    picks_header=' STAT SP IPHASW D HRMM SECON CODA AMPLIT PERI AZIMU VELO AIN AR TRES W  DIS CAZ7'
    
   
    
    
    ###############################################################################################################
    #se crea el archivo de salida es decir el s-file resultante, tambien se le agregan las lineas creadas arriba
    try:
        os.mkdir(files_path+'/seisan_output/')
    except:
        pass
    copyfile(files_path+wav_file_name,files_path+'/seisan_output/'+seisan_wav_name)
    s_file_output=open(files_path+'/seisan_output/'+ sfile_name,'w')
    ################################################################################################################
    
    
    
    
    ################################################################################################################
    # inicia proceso de edicion de S-file
    
    s_file_output.write(s_file_header+'\n')
    s_file_output.write(wav_file_location_line+'\n')
    s_file_output.write(picks_header+'\n')
    #a=station_list_xml[0]
    
    
    #se intera a traves de las picadas de fase para agregarlas al s-file
    
    for station_pick in station_list_xml:
        station=add_blank(station_pick[0],5)
        channel=station_pick[1]
        instrument=station_pick[2][0]
        
        hour=station_pick[6]
        minute=station_pick[7]
        seconds=station_pick[8]
        phase=station_pick[9]
        
        """
        #se relaciona la lista de xml y la lista creada del boletin de seiscomp
        a,b=find_in_sublists(station_list,add_blank_suffix(station_pick[0],5))
        
        azimuth=station_list[a][8]
        
        time_residual=station_list[a][4]
        if time_residual[0]=='-':
            time_residual=add_blank(station_list[a][4],3)
        else:
            time_residual=add_blank(station_list[a][4],4)
        
        distance=add_blank(station_list[a][5],4)
       """ 
        quality_indicator='I'# revisar Apendice A del manual de SEISAN pag 541..
        
        
        station_pick_line=' '+add_blank_suffix(station_pick[0],5)+instrument+channel+' '+quality_indicator+phase
        station_pick_line=station_pick_line+'       '+hour+minute+seconds+'0 '
        station_pick_line=add_blank_suffix(station_pick_line,80)#+azimuth[:6]+' '
        #station_pick_line=add_blank_suffix(station_pick_line,63)+time_residual+'    '+distance+'     '
        s_file_output.write(station_pick_line+'\n')
        
    s_file_output.write(add_blank(' ',80)+'\n')
    s_file_output.close()    
    print(sfile_name+' '+xml_file_name)
    
    
    
    
"""
for station_pick in station_list:
    staion_pick_line=' '+add_blank(station_pick[0],5)+'HZ '+'EP '+station_pick[6][0:1]
    if station_pick[7]=='A':
        station_pick_line=staion_pick_line+'A  '
    else:
        station_pick_line=staion_pick_line+'  '
    station_pick_line=station_pick_line+hour+minute+add_blank(seconds,6)+' '
"""
    
root_path='./SC2SEI/'
seicomp_file_list=os.listdir(root_path)
i=0
for seiscomp_file in seicomp_file_list:
    i+=1
    #print(i)
    #print(seiscomp_file)
    if seiscomp_file.find('xml')!=-1:
        seiscomp_file_name=seiscomp_file.split('.')[0]
        seiscomp_to_nordic(root_path,
                           seiscomp_file_name+'.txt',
                           seiscomp_file_name+'.mseed',
                           seiscomp_file)
    
    











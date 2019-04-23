#!/bin/python
# -*- coding:utf-8 -*-
"""
@author: XueFeiLiu(201307129@gznu.edu.cn,qq 316187631@qq.com)
@file: Atom_number.py
@time: 2019/1/29 21:44

"""
import re
import sys
import os
from numpy import *
import numpy as np
import pprint
poscar_bulk="../../bulk/POSCAR"
poscar_def="POSCAR"
def defect_coord_center():
    str1=[]
    str2=[]
    str_dump=[]
    d_center3=[]
    d_center4=[]
    f_bulk=open(poscar_bulk,'r')
    f_def=open(poscar_def,'r')
    fc=open("defect_center.dat",'w+')
     
    for line in f_bulk.readlines():
        str1.append(line.replace("\n",''))
    for line in f_def.readlines():
        str2.append(line.replace("\n",''))
     
    for i in str1:
        if i in str2:
            str_dump.append(i)
     
    str_all=set(str1+str2)
     
    for i in str_dump:
        if i in str_all:
            str_all.remove(i)
    
    for i in list(str_all):
        fc.write(i+'\n')
    f_bulk.close()
    f_def.close()
    fc.close()
    f_defect_r=open("defect_center.dat",'r')
    f_defect_w=open("center_coord.dat",'w+')
    #readline=f_defect_r.readlines()
    for line in f_defect_r:
        d_center.append(line)
        #line=line.replace('\n','')
    d_center.sort()
    d_center1=d_center[0]
    d_center2=d_center1[:-2]
    d_center3=(d_center2.split())
    
    return d_center3
def lattice_write():
    lattice=[]
    poscar_tem=[]
    scale=[]
    if os.path.exists("POSCAR"):
       poscar=open("POSCAR",'r')
    elif os.path.exists("CONTCAR"):
         poscar=open("CONTCAR",'r')
    else:
        raise IOError('CONTCAR OR POSCAR does not exist！')
    for line in poscar.readlines():
                poscar_tem.append(line)
    poscar.close()
    scale=poscar_tem[1].split()
    lat=poscar_tem[2:5]
    for i in lat:
        lattice.append(i.split())
    scale_lat=[]
    scale_lat.append(scale)
    scale_lat.append(lattice)
    return scale_lat
def other_line():
    lines=[]
    poscar_tem=[]
    if os.path.exists("POSCAR"):
       poscar=open("POSCAR",'r')
    elif os.path.exists("CONTCAR"):
         poscar=open("CONTCAR",'r')
    else:
        raise IOError('CONTCAR OR POSCAR does not exist！')
    for line in poscar.readlines():
                poscar_tem.append(line)
    line1=poscar_tem[0]
    line6=poscar_tem[5]
    line7=poscar_tem[6]
    if poscar_tem[7].strip().upper().startswith("S"):
       line8=poscar_tem[7]
       line9=poscar_tem[8]
    else:
    
       line8=' '
       line9=poscar_tem[7]    
    lines.append(line1)
    lines.append(line6)
    lines.append(line7)    
    lines.append(line8)
    lines.append(line9)
    return lines    
def atom_coord_write():
    cord=[]
    poscar_tem=[]
    atom_num=[]
    if os.path.exists("POSCAR"):
       poscar=open("POSCAR",'r')
    elif os.path.exists("CONTCAR"):
         poscar=open("CONTCAR",'r')
    else:
        raise IOError('CONTCAR OR POSCAR does not exist！')
    for line in poscar.readlines():
                poscar_tem.append(line)
    poscar.close()

    atom_n=poscar_tem[6]
    atom_n=atom_n.split()
    atom_number=0
    for i in range(len(atom_n)):

        atom_number+=int(atom_n[i])
    if poscar_tem[7].strip().upper().startswith("S"):    
       coor=poscar_tem[9:9+atom_number]
    else:
       coor=poscar_tem[8:8+atom_number]
    for i in coor:
        cord.append(i.split()[0:3])
    reslut=[]
    reslut.append(atom_number)
    reslut.append(cord)
    return reslut

def write_atom_acording_layer():
    
     data=atom_coord_write()
    
     atom_number=data[0]
     cord=data[1]
     
     key=list(range(1,atom_number+1))
     value=[]
     for i in range(atom_number):
         value.append(cord[i])
     layer=dict(zip(key,value))
     layer_sort=sorted(layer.items(),key=lambda x:float(x[1][2]))
     return layer,layer_sort
def show_layers():
     layer,layer_sort=write_atom_acording_layer()
     print("**************************************************************")
     print("                Sorted atoms coordination:                    ")
     print("**************************************************************")
     pprint.pprint(layer_sort)
     data=atom_coord_write()
     atom_number=data[0]
     print("**************************************************************")
     print(" Please input a threshold value according to layer distance,\n\
 the atoms coordination has been listed above.e.g:for direct a\n\
 smaller value as 0.001,for cartesian a bigger value as 0.5 needed\n \
     ")
     print("**************************************************************")
     delt=float(input( "Input:\n "))
          
     k=1
     lay=[]
     lay_n=[]
     tmp=[]
     for i in range(1,atom_number):
         if abs(float(layer_sort[i][1][2])-float(layer_sort[i-1][1][2]))> delt:
            k+=1
            lay.append(i)
     lay.append(atom_number)
     key0=list(range(k))
     lay_num=dict(zip(key0,lay))
     print("\n")
     print("**************************************************************")
     print("           There are total %.d layers are found!"  %k)
     print("**************************************************************")
     
     return lay_num
def atom_select():
    lay_num=show_layers()
    layer,layer_sort=write_atom_acording_layer()
    data=atom_coord_write()
    atom_number=data[0]
    print("**************************************************************")
    print("      There are two  methods to fix atoms in POSCAR:\n")
    print("The first one :input a total layer number,e.g. 5 means you will \
                       fix 5 layers from bottom to top")
    print("The second one:input a layer order number,e.g. 3 4  measn you\n \
will fix the 3th and 4th layer ,used in case where you want to fix\n \
center part of the POSCAR ")
    print("**************************************************************")
    print("**************************************************************")
    fix_type=str(input("     Please input a for method 1 and b for method 2:\n"))
    print("**************************************************************")
    if fix_type=='a':
       print("**************************************************************")
       la_n=int(input("Please input the total number of layers to be fixed :"))
       print("**************************************************************")
       la_n1=la_n-1
          
       sel_up=lay_num[la_n1]
       atoms=[]
       atoms_not=[]
       for i in range(0,sel_up):
           atoms.append(layer_sort[i][0])
           
       for j in range(sel_up,atom_number):
           atoms_not.append(layer_sort[j][0])
    elif fix_type=='b':
       print("**************************************************************")
       la_n=str(input("Please input the number of layer order to be fixed :"))
       print("**************************************************************")
       la_n=la_n.strip().split()
       atoms=[]
       
       atoms_not_tmp=[]
       if '1' in la_n:
           for j in range(0,lay_num[0]):
                  atoms.append(layer_sort[j][0])
       for i in la_n:
           la_n1=int(i)-1
           if la_n1>=len(lay_num):
              la_n1=len(lay_num)-1
           la_n0=int(i)-2
           if la_n0<=0:
              la_n0=0
           sel_low=lay_num[la_n0]
           
           sel_up=lay_num[la_n1]
          
          
           for i in range(sel_low,sel_up):
               
                   atoms.append(layer_sort[i][0])
       for k in range(len(layer_sort)):
           atoms_not_tmp.append(layer_sort[k][0])
       atoms_not=list((set(atoms_not_tmp).difference(set(atoms))))
      
               
    else:
        print("**************************************************************")
        print("           You have input wrong !Please rerun this script !")
        print("**************************************************************")
        sys.exit()
            
    return atoms,atoms_not,layer,layer_sort

def atom_select_for_new_poscar():
    #layer,layer_sort=write_atom_acording_layer()
    atoms,atoms_not,layer,layer_sort=atom_select()
    tf=[]
    tf_other=['T T T']
    new_layer=[]
    print("**************************************************************")
    TF=str(input("Please input which type you will fix,e.g. F F T,F F F,T F F etc.:\n"))
    print("**************************************************************")
    tf.append(TF)
    for i in atoms:
        layer[i]=layer[i]+tf
        
    for j in atoms_not:
        layer[j]=layer[j]+tf_other
    for k in range(len(layer)):
        new_layer.append(layer[k+1]) 
    print("**************************************************************")        
    print("             Atoms number below have been fixed !\n")
    print(atoms)
    print("            New POSCAR has been written in POSCAR_NEW !")
    print("**************************************************************")    
    return new_layer
def new_POSCAR_write():
    new_POSCAR=[]
    scale_lat=lattice_write()
    other_lines=other_line()
    other_lines[3]='Selective Dynamics\n'
    
    atom_cords=atom_select_for_new_poscar()
    new_POSCAR.append(other_lines[0])
    new_POSCAR.append(" ".join(scale_lat[0])+'\n')
    for i in range(3):
        new_POSCAR.append(" ".join(scale_lat[1][i])+'\n')
    for i in range(1,5):
        new_POSCAR.append(other_lines[i])
    for i in range(len(atom_cords)):
        new_POSCAR.append("   ".join(atom_cords[i])+'\n')
    return new_POSCAR
       
        
if __name__=="__main__":
    
   new_POSCAR=new_POSCAR_write()
   poscar_new=open("POSCAR_NEW",'w+')
   for i in new_POSCAR:
       poscar_new.write(i)
   layer,layer_sort=write_atom_acording_layer()    
   poscar_new.close()
   print("**************************************************************")
   print("        You may contact 316187631@QQ.com if any questions")
   print("**************************************************************")
   #lay_num=show_layers()
import json 
import numpy as np 
import cv2
import matplotlib.pyplot as plt
import itertools
from collections import defaultdict

"""
HELPER FUNCTIONS
"""

def consecutive(x):
    """
    input:[3,4,7,9,11,12,13,14,16,17,18,20,21]
    output:[[3, 4], 7, 9, 11, [11, 12, 13, 14], [12, 13, 14], [13, 14], 16, [16, 17, 18], [17, 18], 20, [20, 21]]
    """
    qq = []    
    for i in range(len(x)-1):
        ml = int()
        if x[i+1]-x[i]==1:
            ml +=1            
            bb = []
            #print(list(itertools.takewhile(lambda h: x[h+1]-x[h]==1,range(i,len(x)-1))))
            for k in list(itertools.takewhile(lambda h: x[h+1]-x[h]==1,range(i,len(x)-1))):
                bb.append(x[k])
                #print(bb)
            try:
                bb.append(x[list(itertools.takewhile(lambda h: x[h+1]-x[h]==1,range(i,len(x)-1)))[-1]+1])            
            except IndexError:
                pass
            if bb:
                qq.append(bb)        
        else:
            if ml==0:
                if i == len(x)-2:
                    #print(x[i])
                    qq.append(x[i])
                    qq.append(x[i+1])
                else:  
                    #print(x[i])
                    qq.append(x[i])               
    return qq  
  
  
def av_len(ans):
    """
    input:[[3, 4], 7, 9, 11, [11, 12, 13, 14], [12, 13, 14], [13, 14], 16, [16, 17, 18], [17, 18], 20, [20, 21]]
    output:[[3, 4], 7, 9, [11, 12, 13, 14], [16, 17, 18], [20, 21]]
    """
    true_major = ans[:]
    for i in range(len(ans)):
        try:
            if len(ans[i]):
                for j in range(i+1,i+len(ans[i])-1):
                    try:
                        true_major.remove(ans[j])
                    except ValueError:
                        pass
        except TypeError:
            pass    
    az = true_major[:]
    for k in range(len(true_major)):
        try:
            if len(true_major[k])>1:
                try:              
                    az.remove(true_major[k+1])
                except:
                    pass
        except:
            pass    
    return az

def choose_one(foo):
    """
    input :[[3, 4], 7, 9, [11, 12, 13, 14], [16, 17, 18], [20, 21]]
    output: [0, 4, 7, 9, 13, 17, 21]
    """
    loo = foo[:]    
    for i in range(len(foo)):
        try:
            if len(foo[i]):
                if foo[i][0]==0:                    
                    loo[i]==0
                else:
                    loo[i]= foo[i][len(foo[i])//2]
            else:
                pass
        except:
            pass
    if loo:
        if loo[0]!=0:
            loo.insert(0,0)
        else:
            pass
    else:
        pass
    return loo

##########################################################################################################################################################################


def read_image(img_path):
   im = cv2.imread(img_path)
   return im
   

 
def bootstrap_annotations(im,annotations):
    the_default ={}
    for i in annotations: 
        samp  = []
        cords = i['geometry'] 
        x_init = cords[0][0]
        x_final = cords[1][0]
        x_diff = x_final-x_init
        y_init = cords[0][1]
        y_final = cords[1][1]
        slice = im[cords[0][1]:cords[1][1],cords[0][0]:cords[1][0]]
        gray = cv2.cvtColor(slice,cv2.COLOR_BGR2GRAY)
        th3=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                cv2.THRESH_BINARY,11,2)
        ret, threshold = cv2.threshold(th3,0,255,cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)    

        threshold = np.transpose(threshold,(1,0))       
        max_all = 1.5*(len(threshold)//len(list(i['value'])))    
        granular = len(list(i['value']))-1    
        co = []
        for j in range(len(threshold)):        
            if not threshold[j].any():
                co.append(j)
                
        prac = consecutive(co)    
        prac = av_len(prac)    
        prac = choose_one(prac)  
        
        try:
            if prac[-1]!=x_diff:                
                prac.append(x_diff)
        except IndexError:
            pass    
        if not prac:
            samp.append({"geometry":[[' ' ,' ' ],[' ' ,' ' ]],"value":"Unable to decipher"})

        elif len(prac)-1 > len(list(i['value'])):
            samp.append({"geometry":[[' ' ,' ' ],[' ' ,' ' ]],"value":"Possible Incorrect Bounding Box At Some Points"})


        elif len(prac)-1 == len(list(i['value'])):       
            for q in range(len(prac)-1):
                samp.append({"geometry":[[x_init+prac[q],y_init ],[x_init+prac[q+1],y_final]],"value":list(i['value'])[q]})

        else:
            try:
                skip_list=[]        
                for q in range(len(prac)-1): 

                    if prac[q+1]-prac[q]>1.5*max_all:                
                        skip_list.append([k for k in i['value'][q:q+2]])                
                    elif prac[q+1]-prac[q]>max_all:                        
                        skip_list.append([k for k in i['value'][q:q+1]])

                    else:
                         pass
                new_skip_list=[]
                skip_list = list(itertools.chain.from_iterable(skip_list))        
                if skip_list:
                    for jj in i['value']:
                        if jj in skip_list:

                            skip_list.remove(jj)
                        else:
                            new_skip_list.append(jj)
                for q in range(len(new_skip_list)-1):
                    if q ==len(new_skip_list)-2:
                        try:
                            samp.append({"geometry":[[x_init+prac[q],y_init ],[x_init+prac[q+1],y_final]],"value":new_skip_list[q]})
                        except:
                            pass
                        try:
                            samp.append({"geometry":[[x_init+prac[q+1],y_init ],[x_init+prac[q+2],y_final]],"value":new_skip_list[q+1]})
                        except IndexError:
                            pass                    
                    else:
                        samp.append({"geometry":[[x_init+prac[q],y_init ],[x_init+prac[q+1],y_final]],"value":new_skip_list[q]})
            except TypeError:
                samp.append({"geometry":[[' ' ,' ' ],[' ' ,' ' ]],"value":"unable to decipher"})
                
        the_default.update({i['value']:samp})    
    return the_default
  ######################################################################################################################################################################

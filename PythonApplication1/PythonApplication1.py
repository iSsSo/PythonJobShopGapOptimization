# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 17:15:38 2021

@author: ismail
"""
# from asyncio.windows_events import NULL
import copy
import os
import matplotlib.pyplot as plt
import numpy as np
import colorsys
from datetime import datetime
import hashlib


class FileOperations:
    def __init__(self, filename_):
        print(filename_ + ".txt")
        self.filesonuc = open(filename_ + ".txt", 'w').close()
        self.lines_Order = []       # Ýþler Satýr Makineler Sütun Orj dosyalar Þu iþin þu Op þu makinede
        self.lines_p = []       # Ýþler Satýr Makineler Sütun Orj dosyalar Þu iþin þu Op þu makinede
        self.lines_r = []       # Ýþler Satýr Makineler Sütun Orj dosyalar Þu iþin þu Op þu makinede
        # self.lines_p = op_p           # Ýþler Satýr Makineler Sütun Orj dosyalar
        self.lines_rf = []           # Ýþler Satýr Makineler Sütun Orj dosyalar
        self.s2x = []  # Makineler Satýr Ýþler Sütun Orjinal Listeler  Her iþin makinelere göre dizilimi
        self.s2o = []  # Makineler Satýr Ýþler Sütun Orjinal Listeler  Her iþin makinelere göre dizilimi
        self.s2r = []      # Makineler Satýr Ýþler Sütun Orjinal Listeler
        self.s2p = []
        self.l2r = []      # Ýþler Satýr Makineler Sütun Orjinal Listeler
        self.file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'instances\\_abz_instances\\abz5.txt')
        self.machine_Count = 0
        self.job_Count = 0
        
        
    def open_files(self, filename_):
        self.filesonuc = open(filename_ + ".txt","a")
        
    def list_files(self, folder_):
        if folder_:
            for file1 in os.listdir(folder_):
                if file1.endswith(".txt"):
                    # self.write_files(os.path.join("\nDosya Adi: ", file1))
                    print(os.path.join("Dosya Adi: ", file1))
         
    def CalculateIfThereIsFile(self, folder_):
        sayac_ = 0
        with open(self.file_path) as file_in:                       
            inner_list = [splits for splits in file_in.readline().strip().split("\t") if splits != ""]
            self.job_Count = int(inner_list[0])
            self.machine_Count = int(inner_list[1])
            self.lines_Order = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.lines_p = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.lines_r = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.JM_Map = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)]
            self.l2r = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.s2x = [[-1 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.s2o = [[0 for i in range(self.job_Count)] for i in range(self.machine_Count)]
            self.s2r = [[0 for i in range(self.job_Count)] for i in range(self.machine_Count)]
            self.s2p = [[0 for i in range(self.job_Count)] for i in range(self.machine_Count)]
            self.s2d = [[0 for i in range(self.job_Count)] for i in range(self.machine_Count)]
            
            gecici_r = 0 
            for x in range(self.job_Count):
                inner_list = [splits for splits in file_in.readline().strip().split("\t") if splits != ""]
                gecici_r = 0 
                for sayac in range(0,len(inner_list)-1,2):                  
                    self.lines_Order[x][sayac//2] = int(inner_list[sayac]) 
                    sayac += 1
                    self.lines_p[x][sayac//2] = int(inner_list[sayac])
                    self.lines_r[x][sayac//2] = gecici_r
                    #self.lines_d[x][sayac//2] = gecici_r + int(inner_list[sayac])
                    gecici_r += int(inner_list[sayac])
                             
            for ww in range(self.machine_Count):
                for zz in range(self.job_Count): 
                    self.JM_Map[self.lines_Order[zz][ww]][zz] = ww 

        # word = ""
        # self.write_files("\n Lines_p: ")
        # for a1 in range(self.job_Count):
        #     for a2 in range(self.machine_Count):
        #         word = word + str(self.lines_p[a1][a2]) + "\t"# fileHandler.write_files(word)
        #     word = word + "\n"
        # self.write_files(word)
                            

        if folder_:
            file_list = os.listdir(folder_)
            for file1 in file_list:
                if file1.__contains__("start.txt"):
                    for file2 in file_list:
                        if file2 == file1.replace("start", "order"):
                            # self.write_files("\n" + file1)
                            with open(folder_ + "\\" + file2) as file_inOrder:     
                                for m_index in range(self.machine_Count): 
                                    inner_list = [splits for splits in file_inOrder.readline().strip().split("\t") if splits != ""]
                                    for sayac in range(len(inner_list)): 
                                        self.s2o[m_index][sayac] = int(inner_list[sayac]) - 1
                            # word = ""
                            # self.write_files("\n s2Order: ")
                            # for a1 in range(self.machine_Count):                               
                            #     for a2 in range(self.job_Count):
                            #         word = word + str(self.s2o[a1][a2]) + "\t" 
                            #     word = word + "\n"
                            # self.write_files(word)
                            
                            with open(folder_ + "\\" + file1) as file_inr:   
                                for j_index in range(self.job_Count): 
                                    inner_list = [splits for splits in file_inr.readline().strip().split("\t") if splits != ""]
                                    for sayac in range(len(inner_list)): 
                                       self.l2r[j_index][sayac] = int(inner_list[sayac])
                                       
                            for a1 in range(self.machine_Count):
                                for a2 in range(self.job_Count):
                                    self.s2r[a1][a2] = self.l2r[self.s2o[a1][a2]][a1]
                                              
                            # word = ""
                            # self.write_files("s2r: ")
                            # for a1 in range(self.machine_Count):
                            #     for a2 in range(self.job_Count):
                            #         word = word + str(self.s2r[a1][a2]) + "\t" 
                            #     word = word + "\n"
                            # self.write_files(word)
                            
                            for a1 in range(self.machine_Count):
                                for a2 in range(self.job_Count):
                                    self.s2p[a1][a2] = self.lines_p[self.s2o[a1][a2]][self.JM_Map[a1][self.s2o[a1][a2]]]
                            
                            # word = ""
                            # self.write_files("s2p: ")
                            # for a1 in range(self.machine_Count):
                            #     for a2 in range(self.job_Count):
                            #         word = word + str(self.s2p[a1][a2]) + "\t" 
                            #     word = word + "\n"
                            # self.write_files(word)
                            
                            ortaNokta = 0
                            puan = 0
                            for a1 in range(self.machine_Count):
                                for a2 in range(self.job_Count): 
                                    ortaNokta = self.s2r[a1][a2] + (self.s2p[a1][a2] / 2)
                                    puan += self.s2p[a1][a2] * ortaNokta
                            self.write_files(str(puan))
    

    def CalculatePoints(self, folder_, folderAll_, numberOfSol_):
        sayac_ = 0
        with open(self.file_path) as file_in:                       
            inner_list = [splits for splits in file_in.readline().strip().split("\t") if splits != ""]
            self.job_Count = int(inner_list[0])
            self.machine_Count = int(inner_list[1])
            self.lines_Order = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.lines_p = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.lines_r = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.JM_Map = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)]
            self.l2r = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.s2x = [[-1 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.s2o = [[[] for j in range(self.machine_Count)] for k in range(numberOfSol_)]
            self.s2r = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)]
            self.s2p = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)]
            self.s2d = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)]
            
            gecici_r = 0 
            for x in range(self.job_Count):
                inner_list = [splits for splits in file_in.readline().strip().split("\t") if splits != ""]
                gecici_r = 0 
                for sayac in range(0,len(inner_list)-1,2):                  
                    self.lines_Order[x][sayac//2] = int(inner_list[sayac]) 
                    sayac += 1
                    self.lines_p[x][sayac//2] = int(inner_list[sayac])
                    self.lines_r[x][sayac//2] = gecici_r
                    #self.lines_d[x][sayac//2] = gecici_r + int(inner_list[sayac])
                    gecici_r += int(inner_list[sayac])
                             
            for ww in range(self.machine_Count):
                for zz in range(self.job_Count): 
                    self.JM_Map[self.lines_Order[zz][ww]][zz] = ww 
                          

        if folder_:
            JobId = 0
            MachineId = 0
            with open(folderAll_ + "All.txt") as file_inOrder:     
                for m_index in range(numberOfSol_): 
                    inner_list = [splits for splits in file_inOrder.readline().strip().split("\t") if splits != ""]
                    for sayac in range(len(inner_list)): 
                        if (int(inner_list[sayac]) % 10) == 0: 
                            JobId = 9
                        else: JobId = (int(inner_list[sayac]) % 10)
                        MachineId = self.lines_Order[JobId][(int(inner_list[sayac]) - 1) // 10]
                        self.s2o[m_index][MachineId].append(JobId)
            
            
            file_list = os.listdir(folder_)
            index_ = 0
            for file1 in file_list:
                if file1.__contains__("start.txt"):
                    # self.write_files("\n" + file1)
                    with open(folder_ + "\\" + file1) as file_inr:   
                        for j_index in range(self.job_Count): 
                            inner_list2 = [splits for splits in file_inr.readline().strip().split("\t") if splits != ""]
                            for sayac in range(len(inner_list2)): 
                                self.l2r[j_index][sayac] = int(inner_list2[sayac])
                                       
                    for a1 in range(self.machine_Count):
                        for a2 in range(self.job_Count):
                            self.s2r[a1][a2] = self.l2r[self.s2o[index_][a1][a2]][a1]
                            
                    for a1 in range(self.machine_Count):
                        for a2 in range(self.job_Count):
                            self.s2p[a1][a2] = self.lines_p[self.s2o[index_][a1][a2]][self.JM_Map[a1][self.s2o[index_][a1][a2]]]
                            
                    ortaNokta = 0
                    puan = 0
                    for a1 in range(self.machine_Count):
                        for a2 in range(self.job_Count): 
                            ortaNokta = self.s2r[a1][a2] + (self.s2p[a1][a2] / 2)
                            puan += self.s2p[a1][a2] * ortaNokta
                    self.write_files(str(puan))
                index_ = index_ + 1


    def CalcAlgorithm2(self, folder_, folderAll_, numberOfSol_):
        sayac_ = 0
        makespan_ = 1234
        makepanYarisi = makespan_ // 2
        with open(self.file_path) as file_in:                       
            inner_list = [splits for splits in file_in.readline().strip().split("\t") if splits != ""]
            self.job_Count = int(inner_list[0])
            self.machine_Count = int(inner_list[1])
            self.lines_Order = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.lines_p = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.lines_r = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.JM_Map = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)]
            self.l2r = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.s2x = [[-1 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.s2o = [[[] for j in range(self.machine_Count)] for k in range(numberOfSol_)]
            self.s2r = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)]
            self.s2p = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)]
            self.s2d = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)]
            
            gecici_r = 0 
            for x in range(self.job_Count):
                inner_list = [splits for splits in file_in.readline().strip().split("\t") if splits != ""]
                gecici_r = 0 
                for sayac in range(0,len(inner_list)-1,2):                  
                    self.lines_Order[x][sayac//2] = int(inner_list[sayac]) 
                    sayac += 1
                    self.lines_p[x][sayac//2] = int(inner_list[sayac])
                    self.lines_r[x][sayac//2] = gecici_r
                    #self.lines_d[x][sayac//2] = gecici_r + int(inner_list[sayac])
                    gecici_r += int(inner_list[sayac])
                             
            for ww in range(self.machine_Count):
                for zz in range(self.job_Count): 
                    self.JM_Map[self.lines_Order[zz][ww]][zz] = ww 
                          
        stringh =""
        if folder_:
            JobId = 0
            MachineId = 0
            with open(folderAll_ + "All.txt") as file_inOrder:             
                for m_index in range(numberOfSol_): 
                    stringh =""
                    inner_list = [splits for splits in file_inOrder.readline().strip().split("\t") if splits != ""]
                    
                    for aa1 in range(len(inner_list)):
                        stringh = stringh + inner_list[aa1] 
                        if aa1 != len(inner_list) - 1:
                            stringh = stringh + "_"
                    result = hashlib.md5(stringh.encode())
                    # print(result.hexdigest())
                    strinFile = str(result.hexdigest())
                    
                    for sayac in range(len(inner_list)): 
                        if (int(inner_list[sayac]) % 10) == 0: 
                            JobId = 9
                        else: JobId = (int(inner_list[sayac]) % 10) - 1
                        MachineId = self.lines_Order[JobId][(int(inner_list[sayac]) - 1) // 10]
                        self.s2o[m_index][MachineId].append(JobId)
                        
                    with open(folder_ + "\\abz5_" + strinFile + "_solution_start.txt") as file_inr:   
                        for j_index in range(self.job_Count): 
                            inner_list2 = [splits for splits in file_inr.readline().strip().split("\t") if splits != ""]
                            for sayac in range(len(inner_list2)): 
                                self.l2r[j_index][sayac] = int(inner_list2[sayac])
                                       
                    for a1 in range(self.machine_Count):
                        for a2 in range(self.job_Count):
                            self.s2r[a1][a2] = self.l2r[self.s2o[m_index][a1][a2]][a1]
                            
                    for a1 in range(self.machine_Count):
                        # for a2 in range(self.job_Count):
                            self.s2p[a1][a2] = self.lines_p[self.s2o[m_index][a1][a2]][self.JM_Map[a1][self.s2o[m_index][a1][a2]]]
                            
                    ortaNokta = 0
                    puan = 0
                    gapBsl = 0
                    gapUzunluk = 0
                    for a1 in range(self.machine_Count):
                        for a2 in range(self.job_Count): 
                            gapUzunluk = self.s2r[a1][a2] - gapBsl
                            if self.s2r[a1][a2] < makepanYarisi:
                                if gapUzunluk > 0:
                                    ortaNokta = (self.s2r[a1][a2] - gapBsl) / 2
                                    gapUzunluk = self.s2r[a1][a2] - gapBsl
                                    puan += (makepanYarisi - ortaNokta) * gapUzunluk
                            elif gapBsl < makepanYarisi:
                                if gapUzunluk > 0:
                                    ortaNokta = ((makepanYarisi - gapBsl) / 2) + gapBsl
                                    gapUzunluk = makepanYarisi - gapBsl
                                    puan += (makepanYarisi - ortaNokta) * gapUzunluk  
                                break
                                    
                            gapBsl = self.s2r[a1][a2] + self.s2p[a1][a2]
                            self.write_files(str(makepanYarisi) + "_" + str(ortaNokta) + "_" + str(gapUzunluk))
                        gapBsl = 0
                        gapUzunluk = 0
                        self.write_files(str(puan))
                    self.write_files(str(puan))
            
            
            # file_list = os.listdir(folder_)
            # index_ = 0
            # for file1 in file_list:
            #     if file1.__contains__(strinFile):
            #         # self.write_files("\n" + file1)
            #         with open(folder_ + "\\" + file1) as file_inr:   
            #             for j_index in range(self.job_Count): 
            #                 inner_list2 = [splits for splits in file_inr.readline().strip().split("\t") if splits != ""]
            #                 for sayac in range(len(inner_list2)): 
            #                     self.l2r[j_index][sayac] = int(inner_list2[sayac])
                                       
            #         for a1 in range(self.machine_Count):
            #             for a2 in range(self.job_Count):
            #                 self.s2r[a1][a2] = self.l2r[self.s2o[index_][a1][a2]][a1]
                            
            #         for a1 in range(self.machine_Count):
            #             # for a2 in range(self.job_Count):
            #                 self.s2p[a1][a2] = self.lines_p[self.s2o[index_][a1][a2]][self.JM_Map[a1][self.s2o[index_][a1][a2]]]
                            
            #         ortaNokta = 0
            #         puan = 0
            #         gapBsl = 0
            #         gapUzunluk = 0
            #         for a1 in range(self.machine_Count):
            #             for a2 in range(self.job_Count): 
            #                 gapUzunluk = self.s2r[a1][a2] - gapBsl
            #                 if self.s2r[a1][a2] < makepanYarisi:
            #                     if gapUzunluk > 0:
            #                         ortaNokta = (self.s2r[a1][a2] - gapBsl) / 2
            #                         gapUzunluk = self.s2r[a1][a2] - gapBsl
            #                         puan += (makepanYarisi - ortaNokta) * gapUzunluk
            #                 elif gapBsl < makepanYarisi:
            #                     if gapUzunluk > 0:
            #                         ortaNokta = ((makepanYarisi - gapBsl) / 2) + gapBsl
            #                         gapUzunluk = makepanYarisi - gapBsl
            #                         puan += (makepanYarisi - ortaNokta) * gapUzunluk  
            #                     break
                                    
            #                 gapBsl = self.s2r[a1][a2] + self.s2p[a1][a2]
            #                 self.write_files(str(makepanYarisi) + "_" + str(ortaNokta) + "_" + str(gapUzunluk))
            #             gapBsl = 0
            #             gapUzunluk = 0
            #             self.write_files(str(puan))
            #         self.write_files(str(puan))
            #     index_ = index_ + 1


    def CalcAlgorithm3(self, folder_, folderAll_, numberOfSol_):
        sayac_ = 0
        makespan_ = 1234
        makepanYarisi = makespan_ // 2
        with open(self.file_path) as file_in:                       
            inner_list = [splits for splits in file_in.readline().strip().split("\t") if splits != ""]
            self.job_Count = int(inner_list[0])
            self.machine_Count = int(inner_list[1])
            self.lines_Order = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.lines_p = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.lines_r = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.JM_Map = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)]
            self.l2r = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.s2x = [[-1 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.s2o = [[[] for j in range(self.machine_Count)] for k in range(numberOfSol_)]
            self.s2r = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)]
            self.s2p = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)]
            self.s2d = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)]
            
            gecici_r = 0 
            for x in range(self.job_Count):
                inner_list = [splits for splits in file_in.readline().strip().split("\t") if splits != ""]
                gecici_r = 0 
                for sayac in range(0,len(inner_list)-1,2):                  
                    self.lines_Order[x][sayac//2] = int(inner_list[sayac]) 
                    sayac += 1
                    self.lines_p[x][sayac//2] = int(inner_list[sayac])
                    self.lines_r[x][sayac//2] = gecici_r
                    #self.lines_d[x][sayac//2] = gecici_r + int(inner_list[sayac])
                    gecici_r += int(inner_list[sayac])
                             
            for ww in range(self.machine_Count):
                for zz in range(self.job_Count): 
                    self.JM_Map[self.lines_Order[zz][ww]][zz] = ww 
                          
        stringh =""
        if folder_:
            JobId = 0
            MachineId = 0
            with open(folderAll_ + "All.txt") as file_inOrder:             
                for m_index in range(numberOfSol_): 
                    stringh =""
                    inner_list = [splits for splits in file_inOrder.readline().strip().split("\t") if splits != ""]
                    
                    for aa1 in range(len(inner_list)):
                        stringh = stringh + inner_list[aa1] 
                        if aa1 != len(inner_list) - 1:
                            stringh = stringh + "_"
                    result = hashlib.md5(stringh.encode())
                    # print(result.hexdigest())
                    strinFile = str(result.hexdigest())
                    
                    for sayac in range(len(inner_list)): 
                        if (int(inner_list[sayac]) % 10) == 0: 
                            JobId = 9
                        else: JobId = (int(inner_list[sayac]) % 10) - 1
                        MachineId = self.lines_Order[JobId][(int(inner_list[sayac]) - 1) // 10]
                        self.s2o[m_index][MachineId].append(JobId)
                        
                    with open(folder_ + "\\abz5_" + strinFile + "_solution_start.txt") as file_inr:   
                        for j_index in range(self.job_Count): 
                            inner_list2 = [splits for splits in file_inr.readline().strip().split("\t") if splits != ""]
                            for sayac in range(len(inner_list2)): 
                                self.l2r[j_index][sayac] = int(inner_list2[sayac])
                                       
                    for a1 in range(self.machine_Count):
                        for a2 in range(self.job_Count):
                            self.s2r[a1][a2] = self.l2r[self.s2o[m_index][a1][a2]][a1]
                            
                    for a1 in range(self.machine_Count):
                        for a2 in range(self.job_Count):
                            self.s2p[a1][a2] = self.lines_p[self.s2o[m_index][a1][a2]][self.JM_Map[a1][self.s2o[m_index][a1][a2]]]
                            

                    optimumPuan = 0
                    mOptPuan =[0 for i in range(self.machine_Count)]
                    mTotalDurations = [0 for i in range(self.machine_Count)]
                    for a1 in range(self.machine_Count):
                        for a2 in range(self.job_Count): 
                            mTotalDurations[a1] += self.s2p[a1][a2]
                        for a3 in range(mTotalDurations[a1], makespan_):
                            mOptPuan[a1] += makespan_ - a3
                        optimumPuan +=mOptPuan[a1]
                        

                    ortaNokta = 0
                    puan = 0
                    gapBsl = 0
                    gapUzunluk = 0
                    for a1 in range(self.machine_Count):
                        for a2 in range(self.job_Count): 
                            if self.s2r[a1][a2] > gapBsl:
                                for a3 in range(gapBsl, self.s2r[a1][a2]):
                                    puan += makespan_ - a3
                            gapBsl = self.s2r[a1][a2] + self.s2p[a1][a2]
                        if gapBsl < makespan_:
                            for a3 in range(gapBsl, makespan_):
                                    puan += makespan_ - a3
                        # self.write_files(str(puan))
                    self.write_files(str(puan))
                    # self.write_files(str(puan/optimumPuan))
                    
            

    def write_files(self, _word):
        self.filesonuc.write(str(_word) + "\n")    
        
    def close_files(self):
        self.filesonuc.close()
        
        
        
# %% Read Instance

class All_Solver:
    def __init__(self):
        self.machine_Count = 0
        self.job_Count = 0
        #self.op_Order = [][]
        #self.instance_Directory = "C:\Users\ASUS LIVE\Desktop\ismail\Flask vs\SB_Codes\instances"
        #print(type(self.machine_Count))
        self.Cmax = 0
        self.Cj = 0
        self.lines_Order = []       # Ýþler Satýr Makineler Sütun Orj dosyalar Þu iþin þu Op þu makinede
        self.lines_p = []           # Ýþler Satýr Makineler Sütun Orj dosyalar
        self.lines_r = []           # Ýþler Satýr Makineler Sütun Orj dosyalar
        self.lines_d = []           # Ýþler Satýr Makineler Sütun Orj dosyalar
        self.lines_Mp = []      # Makineler Satýr Ýþler BSütun Dinamik Listeler  r deðerlerine göre her iþin makinelere göre sýralanmýþ hali
        self.lines_Mr = []      # Makineler Satýr Ýþler Sütun Dinamik Listeler
        self.lines_Md = []      # Makineler Satýr Ýþler Sütun Dinamik Listeler
        self.linesM_Order = []  # Makineler Satýr Ýþler Sütun Dinamik Listeler 
        self.SM_Map = []     # Orjinal tablodaki iþler sýralamadan sonra kaçýncý sýradalar Map Tablosu
        self.olmayanMakineler = [] # Hiçbir iþin ilk sýrasýnda olmayan makineler
        self.olmayanMakinelerSureleri = []  # # Hiçbir iþin ilk sýrasýnda olmayan makinelerin süreleri
        self.makineToplamSureleri = [] # Makinelerdeki toplam süreler
        self.makinelerSurelereGore = [] # Makinelerin Sürelere göre sýralanmýþ hali
        self.jobToplamSureleri = [] # Makinelerdeki toplam süreler
        self.jobSurelereGore = [] # Makinelerin Sürelere göre sýralanmýþ hali
        self.OneAlinacaklar = []
        self.OneAlinacakSureler = []
        self.jobSonIndeks = []
        self.OpJob = []
        self.OpMakine = []
        self.OperasyonSureleri = []
        self.OpMakineToplamSuresi = []
        
        self.s2x = []  # Makineler Satýr Ýþler Sütun Orjinal Listeler  Her iþin makinelere göre dizilimi
        self.s2o = []  # Makineler Satýr Ýþler Sütun Orjinal Listeler  Her iþin makinelere göre dizilimi
        self.s2r = []      # Makineler Satýr Ýþler Sütun Orjinal Listeler
        self.s2p = []
        self.s2d = []
        self.l2o = []  # Ýþler Satýr Makineler Sütun Orjinal Listeler  
        self.l2r = []      # Ýþler Satýr Makineler Sütun Orjinal Listeler
        self.file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'instances\\_abz_instances\\abz5.txt')
        
        
    def Read(self):
        print(self.file_path)
        with open(self.file_path) as file_in:           
            inner_list = [splits for splits in file_in.readline().strip().split("\t") if splits != ""]
            self.job_Count = int(inner_list[0])
            self.machine_Count = int(inner_list[1])
            
            self.lines_Order = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.lines_p = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.lines_r = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.lines_d = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)]   
            self.lines_Mp = [[] for i in range(self.machine_Count)]
            self.lines_Mr = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)] 
            self.lines_Md = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)] 
            self.linesM_Order = [[] for i in range(self.machine_Count)]
            self.JM_Map = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)]
            self.SM_Map = [[0 for i in range(self.job_Count)] for j in range(self.machine_Count)]
            self.olmayanMakineler = [i for i in range(self.machine_Count)]
            self.makineToplamSureleri = [0 for i in range(self.machine_Count)]
            self.OneAlinacaklar= [[] for i in range(self.machine_Count)]
            self.OneAlinacaklar= [[] for i in range(self.machine_Count)]
            self.makinelerSurelereGore = [i for i in range(self.machine_Count)]
            self.jobSurelereGore = [i for i in range(self.job_Count)]
            self.jobToplamSureleri = [0 for i in range(self.job_Count)]
            self.jobSonIndeks = [0 for i in range(self.job_Count)]
            
            
            self.s2x = [[-1 for i in range(self.machine_Count)] for j in range(self.job_Count)] 
            self.s2o = [[] for i in range(self.machine_Count)]
            self.s2r = [[] for i in range(self.machine_Count)]
            self.s2p = [[] for i in range(self.machine_Count)]
            self.s2d = [[] for i in range(self.machine_Count)]
            self.s2q = [[] for i in range(self.machine_Count)]
            self.l2o = [[] for i in range(self.job_Count)]
            self.l2r = [[] for i in range(self.job_Count)]

            gecici_r = 0          
            for x in range(self.job_Count):
                inner_list = [splits for splits in file_in.readline().strip().split("\t") if splits != ""]
                # in alternative, if you need to use the file content as numbers
                # inner_list = [int(elt.strip()) for elt in line.split(',')]
                gecici_r = 0 
                for sayac in range(0,len(inner_list)-1,2):                  
                    self.lines_Order[x][sayac//2] = int(inner_list[sayac]) 
                    sayac += 1
                    self.lines_p[x][sayac//2] = int(inner_list[sayac])
                    self.lines_r[x][sayac//2] = gecici_r
                    #self.lines_d[x][sayac//2] = gecici_r + int(inner_list[sayac])
                    gecici_r += int(inner_list[sayac])
                    
                if gecici_r > self.Cmax:
                    self.Cmax = gecici_r
                    self.Cj = x              
                #print("Job: {}, Cmax: {}, Machine Order: {}".format(x, gecici_r, self.lines_Order[x]))                
            file_in.close()
        gecici_p = 0    
        for w in range(int(self.job_Count)):
            gecici_p = 0
            for z in range(int(self.machine_Count)-1, -1, -1):  
                # self.JM_Map[self.lines_Order[w][z]][w] = z
                self.lines_d[w][z] = gecici_p
                #self.s2q[self.lines_Order[w][z]][z] = gecici_p
                gecici_p += self.lines_p[w][z]
                self.makineToplamSureleri[self.lines_Order[w][z]] += self.lines_p[w][z]
            self.jobToplamSureleri[w] = gecici_p
            
        for i2 in range(self.machine_Count):
            for i3 in range(self.job_Count):
                self.OpJob.append(i3)
                self.OpMakine.append(self.lines_Order[i3][i2])
                self.OperasyonSureleri.append(self.lines_p[i3][i2])
                self.OpMakineToplamSuresi.append(self.makineToplamSureleri[self.lines_Order[i3][i2]] + self.jobToplamSureleri[i3])
        # print(self.OpMakineToplamSuresi)
                
        for i4 in range(self.machine_Count):
            for i5 in range(1,self.job_Count): 
                indeks = (i4 * self.job_Count) + i5
                key = self.OpMakineToplamSuresi[indeks]
                key1 = self.OpJob[indeks]
                key2 = self.OpMakine[indeks]
                key3 = self.OperasyonSureleri[indeks]
                
                j = indeks-1
                while j >=(i4 * self.job_Count) and key >= self.OpMakineToplamSuresi[j]: 
                    self.OpMakineToplamSuresi[j+1]  = self.OpMakineToplamSuresi[j] 
                    self.OpJob[j+1] = self.OpJob[j]
                    self.OpMakine[j+1] = self.OpMakine[j]
                    self.OperasyonSureleri[j+1] = self.OperasyonSureleri[j]
                    j -= 1
                self.OpMakineToplamSuresi[j+1] = key 
                self.OpJob[j+1] = key1
                self.OpMakine[j+1] = key2
                self.OperasyonSureleri[j+1] = key3
            # for i6 in range(self.job_Count): 
            #     indeks = (i4 * self.job_Count) + i6
            #     print("Op: {}, Job: {}, Machine: {}, Süre: {}, Makine Toplam Süresi: {}".format(indeks, self.OpJob[indeks], self.OpMakine[indeks], self.OperasyonSureleri[indeks], self.OpMakineToplamSuresi[indeks]))  
        print("Cmax: {}, Job: {}".format(self.Cmax, self.Cj))  
        return self.Cmax, self.Cj
    
# %% Draw Gantt Chart
    def GanttChartShow(self, M_Count, J_Count, filename_, ylim, xlim):
        J_Color_List = self.get_colors(J_Count)
        Arr_yTicks = []
        Arr_yLabels = []
        # Declaring a figure "gnt" 
        fig, gnt = plt.subplots() 
          
        # Setting Y-axis limits 
        gnt.set_ylim(0, ylim) 
          
        # Setting X-axis limits 
        gnt.set_xlim(0, xlim) 
          
        # Setting labels for x-axis and y-axis 
        gnt.set_xlabel('Jobs') 
        gnt.set_ylabel('Machines') 

        for i1 in range(M_Count):
            Arr_yTicks.append(10 + (i1 * 5))
            Arr_yLabels.append(i1)
          
        # Setting ticks on y-axis 
        # gnt.set_yticks([10 ,15 ,20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,80]) 
        gnt.set_yticks(Arr_yTicks)
        # Labelling tickes of y-axis 
        gnt.set_yticklabels(Arr_yLabels) 
        # gnt.invert_yaxis()  # labels read top-to-bottom
          
        # Setting graph attribute 
        gnt.grid(True) 
        
        for i1 in range(M_Count):
            for i2 in range(J_Count):
                gnt.broken_barh([(self.s2r[i1][i2],self.lines_p[i2][i1])], (8+(i1*5),4),facecolors = J_Color_List[self.s2o[i1][i2]])
          
        plt.savefig("gantt1.png",dpi=300) 

    def get_colors(self, num_colors):
        colors=[]
        for i in np.arange(0., 360., 360. / num_colors):
            hue = i/360.
            lightness = (50 + np.random.rand() * 10)/100.
            saturation = (90 + np.random.rand() * 10)/100.
            colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
        return colors

    
# %% Calculate Performance   
    def PerformansHesapla(self):
        word_ = "\n"
        cizelgeToplamPuan = 0
        makineToplamPuan = 0
        opPuan = 0
        bosluk = 0
        _job = 0
        maxMakineSure = self.makineToplamSureleri[0]
        boslukBaslangic = 0
        word_ += "Longest Time On Machines= {}\n". format(maxMakineSure)
        for i1 in range(self.machine_Count):
            boslukBaslangic = 0
            makineToplamPuan = 0
            for i2 in range(self.job_Count):
                _job = self.s2o[i1][i2]
                bosluk = self.s2r[i1][i2] - boslukBaslangic - self.lines_p[_job][self.lines_Order[_job].index(i1)]
                opPuan = abs(bosluk * (maxMakineSure - boslukBaslangic))
                word_ += "Op Puan= {} Gap Start= {} Gap= {}\n". format(opPuan, boslukBaslangic, bosluk)
                boslukBaslangic = self.s2r[i1][i2]
                makineToplamPuan += opPuan
            word_ += "Machine Total Puan= {}\n". format(makineToplamPuan)
            cizelgeToplamPuan += makineToplamPuan
        word_ += "Schedule Total Puan= {}\n". format(cizelgeToplamPuan)
        return word_
    
    def PerformansHesapla2(self):
        word_ = "\n\n\n"
        cizelgeToplamPuan = 0
        makineToplamPuan = 0
        opPuan = 0
        bosluk = 0
        _job = 0
        maxMakineSure = self.makineToplamSureleri[0]
        boslukBaslangic = 0
        word_ += "Longest Time On Machines= {}\n". format(maxMakineSure)
        for i1 in range(self.machine_Count):
            boslukBaslangic = 0
            makineToplamPuan = 0
            for i2 in range(self.job_Count):
                _job = self.s2o[i1][i2]
                # bosluk = self.s2r[i1][i2] - boslukBaslangic - self.lines_p[_job][self.lines_Order[_job].index(i1)]
                opPuan = ((self.s2r[i1][i2] + (self.s2p[i1][i2] / 2) * self.s2p[i1][i2]))
                word_ += "Op Puan= {} Baslangic= {} Uzunluk= {} Gap= {}\n". format(opPuan, self.s2r[i1][i2], self.s2p[i1][i2], self.s2r[i1][i2] - boslukBaslangic)                
                boslukBaslangic = self.s2d[i1][i2]
                makineToplamPuan += opPuan
            word_ += "Machine Total Puan= \n{}\n". format(makineToplamPuan)
            cizelgeToplamPuan += makineToplamPuan
        word_ += "Schedule Total Puan= {}\n". format(cizelgeToplamPuan)

        return word_
    

# %% Sort Jobs
    def SortJobSurelereGore(self): 
        # Standart insertion Sort                  
        for i in range(1, self.job_Count): 
            key = self.jobToplamSureleri[i] 
            key1 = self.jobSurelereGore[i]
            j = i-1
            while j >=0 and key > self.jobToplamSureleri[j]:
                self.jobToplamSureleri[j+1]  = self.jobToplamSureleri[j] 
                self.jobSurelereGore[j+1] = self.jobSurelereGore[j]
                j -= 1
            self.jobToplamSureleri[j+1] = key 
            self.jobSurelereGore[j+1] = key1  
 
    
# %% Sort Jobs    
    def SortMakinelerSurelereGore(self): 
        # Standart insertion Sort                  
        for i in range(1, self.machine_Count): 
            key = self.makineToplamSureleri[i] 
            key1 = self.makinelerSurelereGore[i]
            j = i-1
            while j >=0 and key > self.makineToplamSureleri[j]   : 
                self.makineToplamSureleri[j+1]  = self.makineToplamSureleri[j] 
                self.makinelerSurelereGore[j+1] = self.makinelerSurelereGore[j]
                j -= 1
            self.makineToplamSureleri[j+1] = key 
            self.makinelerSurelereGore[j+1] = key1  
  
# %% Check Schedule      
    
    def sr2_KontrolEt(self):
        word_ = "\n"
        
        xOpBitis = 0
        xOncekiOpBitis = 0
        xOpSure = 0      
        #bir makine üzerinde ayný anda sadece bir iþ iþlenebilir
        for a1 in range(self.machine_Count):
            for a2 in range(1, self.job_Count):
                xOpBitis = self.s2d[a1][a2]
                xOncekiOpBitis = self.s2d[a1][a2-1]
                #xOpSure = self.lines_p[self.s2o[a1][a2]][self.s2x[i3][i4]]
                xOpSure = self.s2p[a1][a2]
                if xOpBitis - xOpSure < xOncekiOpBitis:
                    print("On Machine {}, {}.th Op started before previous Op finish".format(a1,a2))
                
        
        #Bir iþe ait operasyon tamamlanmadan o iþin diðer operasyonunun baþlayamamasý Kýsýtý. 
        kacinciSiradaIslenmis = 0
        buOpHangiMakinedeymis = 0
        oncekiOpBitisDegeri = 0
        buOpBitisDegeri = 0
        for i3 in range(self.job_Count):
            for i4 in range(self.machine_Count):
                buOpHangiMakinedeymis = self.lines_Order[i3][i4]
                kacinciSiradaIslenmis = self.s2x[i3][i4] 
                buOpBslDegeri = self.s2r[buOpHangiMakinedeymis][kacinciSiradaIslenmis] 
                if oncekiOpBitisDegeri > buOpBslDegeri:
                    print("lines_Order[{}][{}] started before previous Op finish".format(i3,i4))
                    
                oncekiOpBitisDegeri = buOpBslDegeri + self.lines_p[i3][i4]
            #if self.s2r[i4][]
            buOpBslDegeri = 0
            oncekiOpBitisDegeri = 0
        return word_
    
    
# %% First Option Func - Makine Toplam Sürelerine Göre Çizelgeleme
    def MakineToplamSurelerineGoreCizelgele(self):
        Cizelgelenecek_Op_Count = self.job_Count * self.machine_Count
        makine_ = 0
        job_ = 0
        level_ = 0
        print(self.OpJob)
        print(self.OpMakine)
        for i in range(Cizelgelenecek_Op_Count):
            makine_ = self.OpMakine[i]
            job_ = self.OpJob[i]
            level_ = int(i/self.job_Count)
            self.s2o[makine_].append(job_)   # makineye sýradaki iþ atanýr
            self.s2x[job_][level_] = len(self.s2o[makine_])-1 # Bir Op Bir makinede kaçýncý sýrada?
            self.s2p[makine_].append(self.lines_p[job_][level_])
            if self.s2x[job_][level_] == 0:
                if level_ > 0:
                    self.s2r[makine_].append(self.s2d[self.lines_Order[job_][level_-1]][self.s2x[job_][level_-1]] )
                    self.s2d[makine_].append(self.s2d[self.lines_Order[job_][level_-1]][self.s2x[job_][level_-1]] + self.OperasyonSureleri[i])           
                else:
                    self.s2r[makine_].append(0)
                    self.s2d[makine_].append(self.OperasyonSureleri[i])                   
            else:
                if level_ == 0:
                    self.s2r[makine_].append(self.s2d[makine_][-1])
                    self.s2d[makine_].append(self.s2d[makine_][-1] + self.OperasyonSureleri[i])              
                else:
                    if self.s2d[makine_][-1] > self.s2d[self.lines_Order[job_][level_-1]][self.s2x[job_][level_-1]]:
                        self.s2r[makine_].append(self.s2d[makine_][-1])
                        self.s2d[makine_].append(self.s2d[makine_][-1] + self.OperasyonSureleri[i])                  
                    else:
                        self.s2r[makine_].append(self.s2d[self.lines_Order[job_][level_-1]][self.s2x[job_][level_-1]]) 
                        self.s2d[makine_].append(self.s2d[self.lines_Order[job_][level_-1]][self.s2x[job_][level_-1]] + self.OperasyonSureleri[i])                         

# %% Second Option Func - Sýradan ilk Gelen Ýþe göre Çizelgeleme
    def Baslangic_r_degerleri_Hesapla(self):
        Makine = 0
        self.SortMakinelerSurelereGore()
        self.SortJobSurelereGore()
        makespan_Siradan = 0
        for i2 in range(self.machine_Count):
            for i3 in range(self.job_Count):
                Makine = self.lines_Order[i3][i2]
                self.s2o[Makine].append(i3)   # makineye sýradaki iþ atanýr
                self.l2o[i3].append(Makine)
                self.s2x[i3][i2] = len(self.s2o[Makine])-1 # Bir+ Op Bir makinede kaçýncý sýrada?
                self.s2p[Makine].append(self.lines_p[i3][i2])
                if self.s2x[i3][i2] == 0:
                    if i2 > 0:
                        self.s2r[Makine].append(self.s2d[self.lines_Order[i3][i2-1]][self.s2x[i3][i2-1]])
                        self.l2r[i3].append(self.s2d[self.lines_Order[i3][i2-1]][self.s2x[i3][i2-1]])
                        self.s2d[Makine].append(self.s2d[self.lines_Order[i3][i2-1]][self.s2x[i3][i2-1]] + self.lines_p[i3][i2])
                    else:
                        self.s2r[Makine].append(0)
                        self.l2r[i3].append(0)
                        self.s2d[Makine].append(self.lines_p[i3][i2])
                else:
                    if i2 == 0:
                        self.s2r[Makine].append(self.s2d[Makine][-1])
                        self.l2r[i3].append(self.s2d[Makine][-1])
                        self.s2d[Makine].append(self.s2d[Makine][-1] + self.lines_p[i3][i2])
                    else:
                        if self.s2d[Makine][-1] > self.s2d[self.lines_Order[i3][i2-1]][self.s2x[i3][i2-1]]:
                            self.s2r[Makine].append(self.s2d[Makine][-1]) 
                            self.l2r[i3].append(self.s2d[Makine][-1]) 
                            self.s2d[Makine].append(self.s2d[Makine][-1] + self.lines_p[i3][i2])                     
                        else:
                            self.s2r[Makine].append(self.s2d[self.lines_Order[i3][i2-1]][self.s2x[i3][i2-1]])
                            self.l2r[i3].append(self.s2d[self.lines_Order[i3][i2-1]][self.s2x[i3][i2-1]])
                            self.s2d[Makine].append(self.s2d[self.lines_Order[i3][i2-1]][self.s2x[i3][i2-1]] + self.lines_p[i3][i2])
                        if self.s2d[Makine][-1] > makespan_Siradan:
                                makespan_Siradan = self.s2d[Makine][-1]    
                
        return makespan_Siradan


# %% First Option Func - SPT Orj
    def SPT_Orj(self):
        cizelgelenecekMakineler = []
        cizelgelenecekJoblar = []
        jobKalanSureler = []
        secilenJob = []
        secilenJobSure = []
        jobKalanMakineler = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)]
        Makine_ = 0
        makespan_SPT = 0
        tMakine = []
        tJob = []
        for x1 in range(self.machine_Count):
            cizelgelenecekMakineler.append(x1)
            secilenJob.append(-1)
            secilenJobSure.append(9999)
            tMakine.append(0)
            
        for x1 in range(self.job_Count):
            cizelgelenecekJoblar.append(x1)
            jobKalanSureler.append(self.jobToplamSureleri[x1])
            for x2 in range(self.machine_Count):
                jobKalanMakineler[x1][x2] = self.lines_Order[x1][x2]   
            tJob.append(0)  
            
        while len(cizelgelenecekJoblar) > 0:
            for secilecekMakine in cizelgelenecekMakineler:
                secilenJob[secilecekMakine] = -1
                secilenJobSure[secilecekMakine] = 9999
                for secilecekJob in cizelgelenecekJoblar:
                    if jobKalanMakineler[secilecekJob][0] == secilecekMakine:
                        if jobKalanSureler[secilecekJob] < secilenJobSure[secilecekJob]:
                            secilenJob[secilecekMakine] = secilecekJob
                            secilenJobSure[secilecekMakine] = jobKalanSureler[secilecekJob]
            
            for Operation in range(self.machine_Count):
                Makine_ = jobKalanMakineler[secilecekJob][Operation]
                self.s2o[Makine_].append(secilecekJob)           
                self.s2x[secilecekJob][Makine_] = len(self.s2o[Makine_])-1 # Bir Op Bir makinede kaçýncý sýrada?
                if tMakine[Makine_] >= tJob[secilecekJob]:
                    self.s2r[Makine_].append(tMakine[Makine_])
                    tJob[secilecekJob] = tMakine[Makine_] + self.lines_p[secilecekJob][Operation]
                else:
                    self.s2r[Makine_].append(tJob[secilecekJob])
                    tJob[secilecekJob] += self.lines_p[secilecekJob][Operation]
                tMakine[Makine_] = tJob[secilecekJob] 
                self.s2p[Makine_].append(self.lines_p[secilecekJob][Operation])
                self.s2d[Makine_].append(tJob[secilecekJob])
                if tMakine[Makine_] > makespan_SPT:
                    makespan_SPT = tMakine[Makine_]  
            cizelgelenecekJoblar.remove(secilecekJob)
            jobKalanSureler[secilecekJob] = 0

        return (makespan_SPT)



# %% First Option Func - SPT Modifikasyon 1
    def SPT_v1(self):
        cizelgelenecekMakineler = []
        cizelgelenecekJoblar = []
        jobKalanSureler = []
        secilenJob = []
        secilenJobSure = []
        gecikmeliSecilenMakine = []
        gecikmeliSecilenJob = []
        gecikmeliSecilenJobSure = []
        JobCizelgelenenOp = []
        jobKalanMakineler = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)]
        tMakine = []
        tJob = []
        makineyeAtanabilecekEnYakinJob_t = []
        _Makine = 0
        makespan_SPT = 0
        # self.SortMakinelerSurelereGore()
        # self.SortJobSurelereGore()
        for x1 in range(self.machine_Count):
            cizelgelenecekMakineler.append(x1)
            tMakine.append(0)
            makineyeAtanabilecekEnYakinJob_t.append(0)
            secilenJob.append(-1)
            secilenJobSure.append(9999)
            
        for x1 in range(self.job_Count):
            cizelgelenecekJoblar.append(x1)
            jobKalanSureler.append(self.jobToplamSureleri[x1])
            tJob.append(0)
            JobCizelgelenenOp.append(0)
            for x2 in range(self.machine_Count):
                jobKalanMakineler[x1][x2] = self.lines_Order[x1][x2]          
            
        while len(cizelgelenecekMakineler) > 0:
            for secilecekMakine in cizelgelenecekMakineler:
                secilenJob[secilecekMakine] = -1
                secilenJobSure[secilecekMakine] = 9999
                for secilecekJob in cizelgelenecekJoblar:
                    if jobKalanMakineler[secilecekJob][0] == secilecekMakine:
                        if tJob[secilecekJob] <= tMakine[secilecekMakine] and jobKalanSureler[secilecekJob] < secilenJobSure[secilecekJob]:
                            secilenJob[secilecekMakine] = secilecekJob
                            secilenJobSure[secilecekMakine] = jobKalanSureler[secilecekJob]
             
            sonSecimMakine = -1   
            sonSecimJob = -1
            sonSecimSure  = 9999  
            for x3 in cizelgelenecekMakineler:
                if secilenJobSure[x3] < sonSecimSure:
                    sonSecimMakine = x3
                    sonSecimJob = secilenJob[x3]
                    sonSecimSure = secilenJobSure[x3]
            
            if sonSecimJob == -1: 
                print("No Job selected")
                for sJob in cizelgelenecekJoblar:
                    sMakine = jobKalanMakineler[sJob][0]
                    if tJob[sJob] > tMakine[sMakine]:
                        gecikmeliSecilenJobSure.append(jobKalanSureler[sJob])
                        gecikmeliSecilenJob.append(sJob)
                        gecikmeliSecilenMakine.append(sMakine)              
                
                for x5 in range(len(gecikmeliSecilenMakine)):
                    if gecikmeliSecilenJobSure[x5]  < sonSecimSure:
                        sonSecimMakine = gecikmeliSecilenMakine[x5]
                        sonSecimJob = gecikmeliSecilenJob[x5]
                        sonSecimSure = gecikmeliSecilenJobSure[x5]
                gecikmeliSecilenJob.clear()
                gecikmeliSecilenJobSure.clear()
                gecikmeliSecilenMakine.clear()
              
            self.s2o[sonSecimMakine].append(sonSecimJob)           
            self.s2x[sonSecimJob][sonSecimMakine] = len(self.s2o[sonSecimMakine])-1 # Bir Op Bir makinede kaçýncý sýrada?
            if tMakine[sonSecimMakine] >= tJob[sonSecimJob]:
                self.s2r[sonSecimMakine].append(tMakine[sonSecimMakine])
                print("To Machine {} Op {} assigned with {} r value". format(sonSecimMakine,sonSecimJob,tMakine[sonSecimMakine]))
                tJob[sonSecimJob] = tMakine[sonSecimMakine] + self.lines_p[sonSecimJob][JobCizelgelenenOp[sonSecimJob]]
            else:
                self.s2r[sonSecimMakine].append(tJob[sonSecimJob])
                print("To Machine {} Op {} assigned with {} r value". format(sonSecimMakine,sonSecimJob,tJob[sonSecimJob] ))
                tJob[sonSecimJob] += self.lines_p[sonSecimJob][JobCizelgelenenOp[sonSecimJob]]
            tMakine[sonSecimMakine] = tJob[sonSecimJob] 
            self.s2p[sonSecimMakine].append(self.lines_p[sonSecimJob][JobCizelgelenenOp[sonSecimJob]])
            self.s2d[sonSecimMakine].append(tJob[sonSecimJob] )
            del jobKalanMakineler[sonSecimJob][0]
            if len(jobKalanMakineler[sonSecimJob]) == 0:
                cizelgelenecekJoblar.remove(sonSecimJob)
                # del cizelgelenecekJoblar[sonSecimJob] 
            jobKalanSureler[sonSecimJob] -= self.lines_p[sonSecimJob][JobCizelgelenenOp[sonSecimJob]]
            JobCizelgelenenOp[sonSecimJob] += 1
            if len(self.s2o[sonSecimMakine]) == self.job_Count:
                cizelgelenecekMakineler.remove(sonSecimMakine)
                # del cizelgelenecekMakineler[sonSecimMakine]
            secilenJob[sonSecimMakine] = -1
            secilenJobSure[sonSecimMakine] = 9999
            if tMakine[sonSecimMakine] > makespan_SPT:
                makespan_SPT = tMakine[sonSecimMakine]  

        return (makespan_SPT)



# %% First Option Func - SPT Modifikasyon 2
    def SPT_v2(self):
        cizelgelenecekMakineler = []
        cizelgelenecekJoblar = []
        jobKalanSureler = []
        secilenJob = []
        secilenJobSure = []
        gecikmeliSecilenMakine = []
        gecikmeliSecilenJob = []
        gecikmeliSecilenJobSure = []
        JobCizelgelenenOp = []
        jobKalanMakineler = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)]
        tMakine = []
        tJob = []
        makineyeAtanabilecekEnYakinJob_t = []
        _Makine = 0
        makespan_SPT = 0
        # self.SortMakinelerSurelereGore()
        # self.SortJobSurelereGore()
        for x1 in range(self.machine_Count):
            cizelgelenecekMakineler.append(x1)
            tMakine.append(0)
            makineyeAtanabilecekEnYakinJob_t.append(0)
            secilenJob.append(-1)
            secilenJobSure.append(9999)
            
        for x1 in range(self.job_Count):
            cizelgelenecekJoblar.append(x1)
            jobKalanSureler.append(self.jobToplamSureleri[x1])
            tJob.append(0)
            JobCizelgelenenOp.append(0)
            for x2 in range(self.machine_Count):
                jobKalanMakineler[x1][x2] = self.lines_Order[x1][x2]          
            
        while len(cizelgelenecekMakineler) > 0:
            for secilecekMakine in cizelgelenecekMakineler:
                secilenJob[secilecekMakine] = -1
                secilenJobSure[secilecekMakine] = 9999
                for secilecekJob in cizelgelenecekJoblar:
                    if jobKalanMakineler[secilecekJob][0] == secilecekMakine:
                        if tJob[secilecekJob] <= tMakine[secilecekMakine] and jobKalanSureler[secilecekJob] < secilenJobSure[secilecekJob]:
                            secilenJob[secilecekMakine] = secilecekJob
                            secilenJobSure[secilecekMakine] = jobKalanSureler[secilecekJob]
             
            sonSecimMakine = -1   
            sonSecimJob = -1
            sonSecimSure  = 9999  
            for x3 in cizelgelenecekMakineler:
                if secilenJobSure[x3] < sonSecimSure:
                    sonSecimMakine = x3
                    sonSecimJob = secilenJob[x3]
                    sonSecimSure = secilenJobSure[x3]
            
            if sonSecimJob == -1: 
                print("No Job selected")
                for sJob in cizelgelenecekJoblar:
                    sMakine = jobKalanMakineler[sJob][0]
                    if tJob[sJob] > tMakine[sMakine]:
                        gecikmeliSecilenJobSure.append(tJob[sJob] - tMakine[sMakine])
                        gecikmeliSecilenJob.append(sJob)
                        gecikmeliSecilenMakine.append(sMakine)              
                
                for x5 in range(len(gecikmeliSecilenMakine)):
                    if gecikmeliSecilenJobSure[x5]  < sonSecimSure:
                        sonSecimMakine = gecikmeliSecilenMakine[x5]
                        sonSecimJob = gecikmeliSecilenJob[x5]
                        sonSecimSure = gecikmeliSecilenJobSure[x5]
                gecikmeliSecilenJob.clear()
                gecikmeliSecilenJobSure.clear()
                gecikmeliSecilenMakine.clear()
              
            self.s2o[sonSecimMakine].append(sonSecimJob)           
            self.s2x[sonSecimJob][sonSecimMakine] = len(self.s2o[sonSecimMakine])-1 # Bir Op Bir makinede kaçýncý sýrada?
            if tMakine[sonSecimMakine] >= tJob[sonSecimJob]:
                self.s2r[sonSecimMakine].append(tMakine[sonSecimMakine])
                print("To Machine {} Op {} assigned with {} r value". format(sonSecimMakine,sonSecimJob,tMakine[sonSecimMakine]))
                tJob[sonSecimJob] = tMakine[sonSecimMakine] + self.lines_p[sonSecimJob][JobCizelgelenenOp[sonSecimJob]]
            else:
                self.s2r[sonSecimMakine].append(tJob[sonSecimJob])
                print("To Machine {} Op {} assigned with {} r value". format(sonSecimMakine,sonSecimJob,tJob[sonSecimJob] ))
                tJob[sonSecimJob] += self.lines_p[sonSecimJob][JobCizelgelenenOp[sonSecimJob]]
            tMakine[sonSecimMakine] = tJob[sonSecimJob] 
            self.s2p[sonSecimMakine].append(self.lines_p[sonSecimJob][JobCizelgelenenOp[sonSecimJob]])
            self.s2d[sonSecimMakine].append(tJob[sonSecimJob] )
            del jobKalanMakineler[sonSecimJob][0]
            if len(jobKalanMakineler[sonSecimJob]) == 0:
                cizelgelenecekJoblar.remove(sonSecimJob)
                # del cizelgelenecekJoblar[sonSecimJob] 
            jobKalanSureler[sonSecimJob] -= self.lines_p[sonSecimJob][JobCizelgelenenOp[sonSecimJob]]
            JobCizelgelenenOp[sonSecimJob] += 1
            if len(self.s2o[sonSecimMakine]) == self.job_Count:
                cizelgelenecekMakineler.remove(sonSecimMakine)
                # del cizelgelenecekMakineler[sonSecimMakine]
            secilenJob[sonSecimMakine] = -1
            secilenJobSure[sonSecimMakine] = 9999
            if tMakine[sonSecimMakine] > makespan_SPT:
                makespan_SPT = tMakine[sonSecimMakine]  
        
        return (makespan_SPT)
                            
                            
    
# %% First Option Func - SPT Orj
    def LPT_Orj(self):
        cizelgelenecekMakineler = []
        cizelgelenecekJoblar = []
        jobKalanSureler = []
        secilenJob = []
        secilenJobSure = []
        jobKalanMakineler = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)]
        Makine_ = 0
        makespan_SPT = 0
        tMakine = []
        tJob = []
        for x1 in range(self.machine_Count):
            cizelgelenecekMakineler.append(x1)
            secilenJob.append(-1)
            secilenJobSure.append(0)
            tMakine.append(0)
            
        for x1 in range(self.job_Count):
            cizelgelenecekJoblar.append(x1)
            jobKalanSureler.append(self.jobToplamSureleri[x1])
            for x2 in range(self.machine_Count):
                jobKalanMakineler[x1][x2] = self.lines_Order[x1][x2]   
            tJob.append(0)  
            
        while len(cizelgelenecekJoblar) > 0:
            for secilecekMakine in cizelgelenecekMakineler:
                secilenJob[secilecekMakine] = -1
                secilenJobSure[secilecekMakine] = 0
                for secilecekJob in cizelgelenecekJoblar:
                    if jobKalanMakineler[secilecekJob][0] == secilecekMakine:
                        if jobKalanSureler[secilecekJob] > secilenJobSure[secilecekJob]:
                            secilenJob[secilecekMakine] = secilecekJob
                            secilenJobSure[secilecekMakine] = jobKalanSureler[secilecekJob]
            
            for Operation in range(self.machine_Count):
                Makine_ = jobKalanMakineler[secilecekJob][Operation]
                self.s2o[Makine_].append(secilecekJob)           
                self.s2x[secilecekJob][Makine_] = len(self.s2o[Makine_])-1 # Bir Op Bir makinede kaçýncý sýrada?
                if tMakine[Makine_] >= tJob[secilecekJob]:
                    self.s2r[Makine_].append(tMakine[Makine_])
                    tJob[secilecekJob] = tMakine[Makine_] + self.lines_p[secilecekJob][Operation]
                else:
                    self.s2r[Makine_].append(tJob[secilecekJob])
                    tJob[secilecekJob] += self.lines_p[secilecekJob][Operation]
                tMakine[Makine_] = tJob[secilecekJob] 
                self.s2p[Makine_].append(self.lines_p[secilecekJob][Operation])
                self.s2d[Makine_].append(tJob[secilecekJob])
                if tMakine[Makine_] > makespan_SPT:
                    makespan_SPT = tMakine[Makine_]  
            cizelgelenecekJoblar.remove(secilecekJob)
            jobKalanSureler[secilecekJob] = 0

        return (makespan_SPT)



# %% First Option Func - SPT Modifikasyon 1
    def LPT_v1(self):
        cizelgelenecekMakineler = []
        cizelgelenecekJoblar = []
        jobKalanSureler = []
        secilenJob = []
        secilenJobSure = []
        gecikmeliSecilenMakine = []
        gecikmeliSecilenJob = []
        gecikmeliSecilenJobSure = []
        JobCizelgelenenOp = []
        jobKalanMakineler = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)]
        tMakine = []
        tJob = []
        makineyeAtanabilecekEnYakinJob_t = []
        _Makine = 0
        makespan_SPT = 0
        # self.SortMakinelerSurelereGore()
        # self.SortJobSurelereGore()
        for x1 in range(self.machine_Count):
            cizelgelenecekMakineler.append(x1)
            tMakine.append(0)
            makineyeAtanabilecekEnYakinJob_t.append(0)
            secilenJob.append(-1)
            secilenJobSure.append(0)
            
        for x1 in range(self.job_Count):
            cizelgelenecekJoblar.append(x1)
            jobKalanSureler.append(self.jobToplamSureleri[x1])
            tJob.append(0)
            JobCizelgelenenOp.append(0)
            for x2 in range(self.machine_Count):
                jobKalanMakineler[x1][x2] = self.lines_Order[x1][x2]          
            
        while len(cizelgelenecekMakineler) > 0:
            for secilecekMakine in cizelgelenecekMakineler:
                secilenJob[secilecekMakine] = -1
                secilenJobSure[secilecekMakine] = 0
                for secilecekJob in cizelgelenecekJoblar:
                    if jobKalanMakineler[secilecekJob][0] == secilecekMakine:
                        if tJob[secilecekJob] <= tMakine[secilecekMakine] and jobKalanSureler[secilecekJob] > secilenJobSure[secilecekJob]:
                            secilenJob[secilecekMakine] = secilecekJob
                            secilenJobSure[secilecekMakine] = jobKalanSureler[secilecekJob]
             
            sonSecimMakine = -1   
            sonSecimJob = -1
            sonSecimSure  = 0  
            for x3 in cizelgelenecekMakineler:
                if secilenJobSure[x3] > sonSecimSure:
                    sonSecimMakine = x3
                    sonSecimJob = secilenJob[x3]
                    sonSecimSure = secilenJobSure[x3]
            
            if sonSecimJob == -1: 
                print("No Job selected")
                for sJob in cizelgelenecekJoblar:
                    sMakine = jobKalanMakineler[sJob][0]
                    if tJob[sJob] > tMakine[sMakine]:
                        gecikmeliSecilenJobSure.append(jobKalanSureler[sJob])
                        gecikmeliSecilenJob.append(sJob)
                        gecikmeliSecilenMakine.append(sMakine)              
                
                for x5 in range(len(gecikmeliSecilenMakine)):
                    if gecikmeliSecilenJobSure[x5]  > sonSecimSure:
                        sonSecimMakine = gecikmeliSecilenMakine[x5]
                        sonSecimJob = gecikmeliSecilenJob[x5]
                        sonSecimSure = gecikmeliSecilenJobSure[x5]
                gecikmeliSecilenJob.clear()
                gecikmeliSecilenJobSure.clear()
                gecikmeliSecilenMakine.clear()
              
            self.s2o[sonSecimMakine].append(sonSecimJob)           
            self.s2x[sonSecimJob][sonSecimMakine] = len(self.s2o[sonSecimMakine])-1 # Bir Op Bir makinede kaçýncý sýrada?
            if tMakine[sonSecimMakine] >= tJob[sonSecimJob]:
                self.s2r[sonSecimMakine].append(tMakine[sonSecimMakine])
                print("To Machine {} Op {} assigned with {} r value". format(sonSecimMakine,sonSecimJob,tMakine[sonSecimMakine]))
                tJob[sonSecimJob] = tMakine[sonSecimMakine] + self.lines_p[sonSecimJob][JobCizelgelenenOp[sonSecimJob]]
            else:
                self.s2r[sonSecimMakine].append(tJob[sonSecimJob])
                print("To Machine {} Op {} assigned with {} r value". format(sonSecimMakine,sonSecimJob,tJob[sonSecimJob] ))
                tJob[sonSecimJob] += self.lines_p[sonSecimJob][JobCizelgelenenOp[sonSecimJob]]
            tMakine[sonSecimMakine] = tJob[sonSecimJob] 
            self.s2p[sonSecimMakine].append(self.lines_p[sonSecimJob][JobCizelgelenenOp[sonSecimJob]])
            self.s2d[sonSecimMakine].append(tJob[sonSecimJob] )
            del jobKalanMakineler[sonSecimJob][0]
            if len(jobKalanMakineler[sonSecimJob]) == 0:
                cizelgelenecekJoblar.remove(sonSecimJob)
                # del cizelgelenecekJoblar[sonSecimJob] 
            jobKalanSureler[sonSecimJob] -= self.lines_p[sonSecimJob][JobCizelgelenenOp[sonSecimJob]]
            JobCizelgelenenOp[sonSecimJob] += 1
            if len(self.s2o[sonSecimMakine]) == self.job_Count:
                cizelgelenecekMakineler.remove(sonSecimMakine)
                # del cizelgelenecekMakineler[sonSecimMakine]
            secilenJob[sonSecimMakine] = -1
            secilenJobSure[sonSecimMakine] = 0
            if tMakine[sonSecimMakine] > makespan_SPT:
                makespan_SPT = tMakine[sonSecimMakine]  

        return (makespan_SPT)



# %% First Option Func - SPT Modifikasyon 2
    def LPT_v2(self):
        cizelgelenecekMakineler = []
        cizelgelenecekJoblar = []
        jobKalanSureler = []
        secilenJob = []
        secilenJobSure = []
        gecikmeliSecilenMakine = []
        gecikmeliSecilenJob = []
        gecikmeliSecilenJobSure = []
        JobCizelgelenenOp = []
        jobKalanMakineler = [[0 for i in range(self.machine_Count)] for j in range(self.job_Count)]
        tMakine = []
        tJob = []
        makineyeAtanabilecekEnYakinJob_t = []
        _Makine = 0
        makespan_SPT = 0
        # self.SortMakinelerSurelereGore()
        # self.SortJobSurelereGore()
        for x1 in range(self.machine_Count):
            cizelgelenecekMakineler.append(x1)
            tMakine.append(0)
            makineyeAtanabilecekEnYakinJob_t.append(0)
            secilenJob.append(-1)
            secilenJobSure.append(0)
            
        for x1 in range(self.job_Count):
            cizelgelenecekJoblar.append(x1)
            jobKalanSureler.append(self.jobToplamSureleri[x1])
            tJob.append(0)
            JobCizelgelenenOp.append(0)
            for x2 in range(self.machine_Count):
                jobKalanMakineler[x1][x2] = self.lines_Order[x1][x2]          
            
        while len(cizelgelenecekMakineler) > 0:
            for secilecekMakine in cizelgelenecekMakineler:
                secilenJob[secilecekMakine] = -1
                secilenJobSure[secilecekMakine] = 0
                for secilecekJob in cizelgelenecekJoblar:
                    if jobKalanMakineler[secilecekJob][0] == secilecekMakine:
                        if tJob[secilecekJob] <= tMakine[secilecekMakine] and jobKalanSureler[secilecekJob] > secilenJobSure[secilecekJob]:
                            secilenJob[secilecekMakine] = secilecekJob
                            secilenJobSure[secilecekMakine] = jobKalanSureler[secilecekJob]
             
            sonSecimMakine = -1   
            sonSecimJob = -1
            sonSecimSure  = 0
            for x3 in cizelgelenecekMakineler:
                if secilenJobSure[x3] > sonSecimSure:
                    sonSecimMakine = x3
                    sonSecimJob = secilenJob[x3]
                    sonSecimSure = secilenJobSure[x3]
            
            if sonSecimJob == -1: 
                sonSecimSure  = 9999
                print("No Jon selected")
                for sJob in cizelgelenecekJoblar:
                    sMakine = jobKalanMakineler[sJob][0]
                    if tJob[sJob] > tMakine[sMakine]:
                        gecikmeliSecilenJobSure.append(tJob[sJob] - tMakine[sMakine])
                        gecikmeliSecilenJob.append(sJob)
                        gecikmeliSecilenMakine.append(sMakine)              
                
                for x5 in range(len(gecikmeliSecilenMakine)):
                    if gecikmeliSecilenJobSure[x5] < sonSecimSure:
                        sonSecimMakine = gecikmeliSecilenMakine[x5]
                        sonSecimJob = gecikmeliSecilenJob[x5]
                        sonSecimSure = gecikmeliSecilenJobSure[x5]
                gecikmeliSecilenJob.clear()
                gecikmeliSecilenJobSure.clear()
                gecikmeliSecilenMakine.clear()
              
            self.s2o[sonSecimMakine].append(sonSecimJob)           
            self.s2x[sonSecimJob][sonSecimMakine] = len(self.s2o[sonSecimMakine])-1 # Bir Op Bir makinede kaçýncý sýrada?
            if tMakine[sonSecimMakine] >= tJob[sonSecimJob]:
                self.s2r[sonSecimMakine].append(tMakine[sonSecimMakine])
                print("To Machine {} Op {} assigned with {} r value". format(sonSecimMakine,sonSecimJob,tMakine[sonSecimMakine]))
                tJob[sonSecimJob] = tMakine[sonSecimMakine] + self.lines_p[sonSecimJob][JobCizelgelenenOp[sonSecimJob]]
            else:
                self.s2r[sonSecimMakine].append(tJob[sonSecimJob])
                print("To Machine {} Op {} assigned with {} r value". format(sonSecimMakine,sonSecimJob,tJob[sonSecimJob] ))
                tJob[sonSecimJob] += self.lines_p[sonSecimJob][JobCizelgelenenOp[sonSecimJob]]
            tMakine[sonSecimMakine] = tJob[sonSecimJob] 
            self.s2p[sonSecimMakine].append(self.lines_p[sonSecimJob][JobCizelgelenenOp[sonSecimJob]])
            self.s2d[sonSecimMakine].append(tJob[sonSecimJob] )
            del jobKalanMakineler[sonSecimJob][0]
            if len(jobKalanMakineler[sonSecimJob]) == 0:
                cizelgelenecekJoblar.remove(sonSecimJob)
                # del cizelgelenecekJoblar[sonSecimJob] 
            jobKalanSureler[sonSecimJob] -= self.lines_p[sonSecimJob][JobCizelgelenenOp[sonSecimJob]]
            JobCizelgelenenOp[sonSecimJob] += 1
            if len(self.s2o[sonSecimMakine]) == self.job_Count:
                cizelgelenecekMakineler.remove(sonSecimMakine)
                # del cizelgelenecekMakineler[sonSecimMakine]
            secilenJob[sonSecimMakine] = -1
            secilenJobSure[sonSecimMakine] = 0
            if tMakine[sonSecimMakine] > makespan_SPT:
                makespan_SPT = tMakine[sonSecimMakine]  
        
        return (makespan_SPT)
    

    def Schrage2(self, J_Index, JsonId, cId, c_Index, M_):
        self.Schrage_Order.clear()
        self.Schrage_r.clear()
        self.Schrage_p.clear()
        self.Schrage_q.clear()
        self.Schrage_q = [0 for i in range(self.job_Count)]
        # print(str(J_Index), str(JsonId), str(cId), str(c_Index), str(M_))
        
        t = 0
        listM_akeSpan = []
        list_t = []
        sortedIndex = 1
        job_Id = 0
        job_r = 0
        job_p = 0 
        job_d = 0
        makeSpan = 0
        lines_Order_g = []
        J_son_JobID = 0
        c_JobId = 99
        J_son_Sorted_Index = 0
        c_Sorted_Index = 99
        x = 0
        makeSpan_J = 0     

        # print(c_Index)
        for i in range(1,self.job_Count):               # 1. iþten sonrasýný geçici listeye ekleriz
            lines_Order_g.append(self.Anlik_Mo[i]) 
        if J_Index != -1:
            del lines_Order_g[c_Index-1]
        # else:
        #     print(self.linesM_Order[M_])
        # print(lines_Order_g)
        
        self.Schrage_Order.append(self.Anlik_Mo[0])     # Çizelgeye 0. iþin eklenmesi
        self.Schrage_r.append(self.Anlik_Mr[0])
        self.Schrage_p.append(self.Anlik_Mp[0])
        self.Schrage_q[0] = self.Anlik_Mq[0]
        # print("r = {}, p = {}, q = {}".format(self.AnlikM_r[0], self.AnlikM_p[0], self.AnlikM_q[0]))
        t = self.Anlik_Mr[0] + self.Anlik_Mp[0]         # t = 0. iþin bitimi
        list_t.append(t)
        makeSpan += t + self.Anlik_Mq[0]                # makespan = 0. iþ bitimi + bekleme süresi
        listM_akeSpan.append(makeSpan)
        while len(lines_Order_g) > 0:                   # Geçici listede iþ kalmayana kadar devam et
            job_Id = lines_Order_g[0]               # Sýradaki çizelgelenecek ilk iþ ele alýnýr
            job_r = self.l2r[job_Id][self.JM_Map[M_][job_Id]]
            job_p = self.l2p[job_Id][self.JM_Map[M_][job_Id]]
            job_q = self.l2q[job_Id][self.JM_Map[M_][job_Id]]
            
            for a in lines_Order_g:                 # Bu for bloðu t izin veriyorsa q en büyük ele alýr
                if t > self.l2r[a][self.JM_Map[M_][a]] and self.l2q[a][self.JM_Map[M_][a]] > job_q:  
                    job_Id = a
                    job_r = self.l2r[a][self.JM_Map[M_][a]] 
                    job_p = self.l2p[a][self.JM_Map[M_][a]]
                    job_q = self.l2q[a][self.JM_Map[M_][a]]
                    
            # print("r = {}, p = {}, q = {}".format(job_r, job_p, job_q))        
            self.Schrage_Order.append(job_Id)       # iþ çizelgeye eklenir
            self.Schrage_p.append(job_p)            # iþin süresi çizelgeye eklenir            
            
            if t > job_r:          # Bu if bloðu t seçilen iþin r deðerinden büyük mü?  
                self.Schrage_r.append(t)                # iþin r deðeri çizelgeye eklenir
                t += job_p           # Büyük ise t ye sadece iþlem süresi eklenir
                x = t + job_q         # makespan = seçilen iþ bitimi + iþin bekleme süresi
                if makeSpan < x:           # Yeni makespan büyük mü?
                    makeSpan = x           # makespan güncellenir
                    J_son_JobID = job_Id   # J bloðunun sonu olarak bu seçilen iþ belirlenir
                    J_son_Sorted_Index = sortedIndex    # J son sýralanmýþ iþlerden kaçýncýsý
            else:                  # if bloðu t seçilen iþin r deðerinden küçükse
                self.Schrage_r.append(job_r)                # iþin r deðeri çizelgeye eklenir
                t = job_r + job_p
                x = t + job_q
                if makeSpan < x:
                    makeSpan = x
                    J_son_JobID = job_Id
                    J_son_Sorted_Index = sortedIndex 
            
            list_t.append(t)                        # t listeye eklenir
            listM_akeSpan.append(makeSpan)          # makespan listeye eklenir
            sortedIndex += 1
            lines_Order_g.remove(job_Id)            # Geçici listeden iþ çýkarýlýr
            
            if job_Id == JsonId and JsonId > -1:
                job_Id = cId
                job_r = self.l2r[cId][self.JM_Map[M_][cId]]
                job_p = self.l2p[cId][self.JM_Map[M_][cId]]
                job_q = self.l2q[cId][self.JM_Map[M_][cId]]
                # print("r = {}, p = {}, q = {}".format(job_r, job_p, job_q))
                self.Schrage_Order.append(job_Id)       # iþ çizelgeye eklenir
                self.Schrage_p.append(job_p)            # iþin süresi çizelgeye eklenir
                
                if t > job_r:          # Bu if bloðu t seçilen iþin r deðerinden büyük mü?   
                    self.Schrage_r.append(t)                # iþin r deðeri çizelgeye eklenir
                    t += job_p           # Büyük ise t ye sadece iþlem süresi eklenir
                    x = t + job_q         # makespan = seçilen iþ bitimi + iþin bekleme süresi
                    if makeSpan < x:         # Yeni makespan büyük mü?
                        makeSpan = x           # makespan güncellenir
                        J_son_JobID = job_Id   # J bloðunun sonu olarak bu seçilen iþ belirlenir
                        J_son_Sorted_Index = self.Anlik_Mo.index(J_son_JobID)    # J son sýralanmýþ iþlerden kaçýncýsý
                else:                  # if bloðu t seçilen iþin r deðerinden küçükse
                    self.Schrage_r.append(job_r)                # iþin r deðeri çizelgeye eklenir
                    t = job_r + job_p
                    x = t + job_q
                    if makeSpan < x:
                        makeSpan = x
                        J_son_JobID = job_Id
                        J_son_Sorted_Index = self.Anlik_Mo.index(J_son_JobID)
                
                list_t.append(t)                        # t listeye eklenir
                listM_akeSpan.append(makeSpan)          # makespan listeye eklenir
                sortedIndex += 1
                
        # print(new_J_son_Level)
        # print(self.lines_q)
        # print(self.lines_Order)
        # print(self.lines_Schrage)
        # print(self.linesM_d[M_])
        gecici_d = 0
        for s in range(self.job_Count-1,-1,-1):
            gecici_Deger = self.l2q[self.Schrage_Order[s]][self.JM_Map[M_][self.Schrage_Order[s]]] 
            if gecici_Deger <= gecici_d:
                self.Schrage_q[s] = gecici_d
            else:
                self.Schrage_q[s] = gecici_Deger
            gecici_d = self.Schrage_q[s] + self.Schrage_p[s] 
        # print(self.Schrage_q)
        
        
        makeSpan_J = self.l2q[self.Schrage_Order[J_son_Sorted_Index]][self.JM_Map[M_][self.Schrage_Order[J_son_Sorted_Index]]]  # Carlier's h(J)>L-d(c) formülü gereði aþaðýda J nin makespan deðeri hesaplanacak
        # makeSpan_J = self.s_d[M_][self.Schrage_Order[J_son_Sorted_Index]]  
        for b in range(J_son_Sorted_Index,-1,-1):        # J nin sonundan geriye doðru c aranacak
            makeSpan_J += self.l2p[self.Schrage_Order[b]][self.JM_Map[M_][self.Schrage_Order[b]]]    # J nin makespaný için elemnlarýnýn p deðerleri eklenir
            if self.l2r[self.Schrage_Order[b]][self.JM_Map[M_][self.Schrage_Order[b]]]  + makeSpan_J + self.l2p[self.Schrage_Order[b]][self.JM_Map[M_][self.Schrage_Order[b-1]]]  > makeSpan:     # Çizelgedeki b-1 sýrasýndaki iþ ile J makespan toplamý makespandan büyük mü?
                c_JobId = self.Schrage_Order[b-1]       # c = çizelgedeki b-1 sýradaki iþtir.
                c_Sorted_Index = self.Anlik_Mo.index(c_JobId)        # c nin indexi b-1 dir.
                # c_Sorted_Index = b-1        # c nin indexi b-1 dir.
                break
        # print(self.Schrage_q)
        # print(listM_akeSpan)
        # print(makeSpan)
        if J_son_Sorted_Index == 0:
            return -1, -1, -1, -1, self.job_Count, makeSpan
        else:
            return J_son_JobID, J_son_Sorted_Index, c_JobId, c_Sorted_Index, self.job_Count, makeSpan
        

    def AnaFunction1(self, J_Index, JsonId, cId, c_Index, M_):
        optimum_Found = False
        makespan = 0
        yeni_Makespan = 0
        max_Lmax = 0
        Lmax = 0
        cizelgelenecek_Machine = 0
        iteration = 0
        Cizelge = []
        donen_Ciz = []
        fileName_ = os.path.join(os.path.dirname(os.path.realpath(__file__)),'instances\\_abz_instances\\abz9.txt')
        
        self = SB_self(fileName_, "")
        C_max, Max_M = self.Read()
        
        # self.insertionSort_ZS(s)
        # self.MapTablosuAyarla() 
          
        while len(self.M_M0) > 0:   
            max_Lmax = 0 - C_max
            makespan = 0
            Lmax = 0
            
            for i in self.M_M0:          
            #self.insertionSort(cizelgelenecek_Machine)
                self.Anlik_Mo.clear()
                self.Anlik_Mr.clear()
                self.Anlik_Mp.clear()
                self.Anlik_Mq.clear()
                for s1 in range(self.job_Count):
                    self.Anlik_Mo.append(s1)
                    self.Anlik_Mr.append(self.l2r[s1][self.JM_Map[i][s1]])
                    self.Anlik_Mp.append(self.l2p[s1][self.JM_Map[i][s1]])
                    self.Anlik_Mq.append(self.l2q[s1][self.JM_Map[i][s1]])
                self.insertionSortQ(i)
                self.insertionSort(i)
                # if i == 5:
                #     print(self.Anlik_Mo)
                #     print(self.Anlik_Mq)
                # if i == 2:
                #     print(self.Anlik_Mq)
                #     print(self.Anlik_Mo)
                #     print(self.Anlik_Mr)
                
                J_son_JobId, J_son_Sorted_Index, c_JobId, c_Sorted_Index, job_Count, yeni_Makespan = self.Schrage2(-1,-1,-1,-1,i)
                # print(J_son_JobId, J_son_Sorted_Index, c_JobId, c_Sorted_Index,yeni_Makespan)
                word += ekword
                optimum_Found = False
                Lmax = yeni_Makespan - C_max
                self.Opt_Order[i] = copy.deepcopy(self.Schrage_Order)
                self.Opt_r[i] = copy.deepcopy(self.Schrage_r)
                self.Opt_p[i] = copy.deepcopy(self.Schrage_p)
                self.Opt_q[i] = copy.deepcopy(self.Schrage_q)
                if J_son_Sorted_Index == job_Count - 1:
                    optimum_Found = True                 
                else:
                    while optimum_Found == False:
                        makespan = yeni_Makespan
                        J_son_JobId, J_son_Sorted_Index, c_JobId, c_Sorted_Index, job_Count, yeni_Makespan = self.Schrage2(J_son_Sorted_Index,J_son_JobId,c_JobId, c_Sorted_Index, i)
                        # print(J_son_JobId, J_son_Sorted_Index, c_JobId, c_Sorted_Index,yeni_Makespan)
                        if yeni_Makespan >= makespan:
                            optimum_Found = True
                        elif J_son_Sorted_Index == job_Count - 1:
                            optimum_Found = True
                            self.Opt_Order[i] = copy.deepcopy(self.Schrage_Order)
                            self.Opt_r[i] = copy.deepcopy(self.Schrage_r)
                            self.Opt_p[i] = copy.deepcopy(self.Schrage_p)
                            self.Opt_q[i] = copy.deepcopy(self.Schrage_q)
                            Lmax = yeni_Makespan - C_max
                        else:
                            self.Opt_Order[i] = copy.deepcopy(self.Schrage_Order)
                            self.Opt_r[i] = copy.deepcopy(self.Schrage_r)
                            self.Opt_p[i] = copy.deepcopy(self.Schrage_p)
                            self.Opt_q[i] = copy.deepcopy(self.Schrage_q)
                            Lmax = yeni_Makespan - C_max
                # print(str(i) + " - " + str(self.Opt_r[i]))
                if Lmax > max_Lmax:
                    max_Lmax = Lmax 
                    cizelgelenecek_Machine = i
            # print(cizelgelenecek_Machine, max_Lmax)
            for ss in range (self.machine_Count):
                self.Anlik_Mo.clear()
                self.Anlik_Mr.clear()
                self.Anlik_Mp.clear()
                self.Anlik_Mq.clear()
                for s1 in range(self.job_Count):
                    self.Anlik_Mo.append(s1)
                    self.Anlik_Mr.append(self.l2r[s1][self.JM_Map[ss][s1]])
                    self.Anlik_Mp.append(self.l2p[s1][self.JM_Map[ss][s1]])
                    self.Anlik_Mq.append(self.l2q[s1][self.JM_Map[ss][s1]])
                self.insertionSort_rPlusd(ss)
                # print(str(ss) + " - " + str(self.Anlik_Mr))
                
            if max_Lmax > 0:
                C_max += max_Lmax
            word += str(cizelgelenecek_Machine) + ", " + str(max_Lmax) + " New Cmax: " + str(C_max)
            self.s2o[cizelgelenecek_Machine] = copy.deepcopy(self.Opt_Order[cizelgelenecek_Machine])
            print(self.Opt_r[cizelgelenecek_Machine])
            # print(self.JM_Map[cizelgelenecek_Machine])
            self.OplariIliskilendir(cizelgelenecek_Machine)
            self.Listeyi_Duzelt(cizelgelenecek_Machine, C_max) # Veriler düzeltilir.
            self.M0.append(cizelgelenecek_Machine)
            self.M_M0.remove(cizelgelenecek_Machine)
            print(iteration)
                            
# %% __main__
if __name__ == "__main__":
    optimum_Found = False
    word = ""
    makespan = 0
    yeni_Makespan = 0
    max_Lmax = 0
    Lmax = 0
    cizelgelenecek_Machine = 0
    Cizelge = []
    donen_Ciz = []
    S = All_Solver()
    C_max, C_job = S.Read()
    _path = os.path.dirname(os.path.realpath(__file__))
    
    # G = GraphDS.Graph(6)
    # G.set_vertexNames(0,'a')
    # G.set_vertexNames(1,'b')
    # G.set_vertexNames(2,'c')
    # G.set_vertexNames(3,'d')
    # G.set_vertexNames(4,'e')
    # G.set_vertexNames(5,'f')
    # G.add_edge(0,4,10)
    # G.add_edge(0,2,20)
    # G.add_edge(2,1,30)
    # G.add_edge(1,4,40)
    # G.add_edge(4,3,50)
    # G.add_edge(5,4,60)

    # G = GraphSB.SBWithGraph(12, S.job_Count, S.machine_Count, S.lines_Order, S.lines_p, S.lines_r, S.lines_d)
    # G.set_vertexNames(0,'S')
    # G.set_vertexNames(1,'0_0')
    # G.set_vertexNames(2,'1_1')
    # G.set_vertexNames(3,'0_2')
    # G.set_vertexNames(4,'1_0')
    # G.set_vertexNames(5,'0_1')
    # G.set_vertexNames(6,'1_2')
    # G.set_vertexNames(7,'2_0')
    # G.set_vertexNames(8,'3_1')
    # G.set_vertexNames(9,'3_2')
    # G.set_vertexNames(10,'2_1')
    # G.set_vertexNames(11,'T')
    # G.add_edge(0, 1, 0)
    # G.add_edge(0, 2, 0)
    # G.add_edge(0, 3, 0)
    # G.add_edge(1, 4, 10)
    # G.add_edge(4, 7, 8)
    # G.add_edge(7, 11, 4)
    # G.add_edge(2, 5, 8)
    # G.add_edge(5, 8, 3)
    # G.add_edge(8, 10, 5)
    # G.add_edge(10, 11, 6)
    # G.add_edge(3, 6, 4)
    # G.add_edge(6, 9, 7)
    # G.add_edge(9, 11, 3)

    # Djk = GraphSB.SBWithGraph.dijkstra(G, 0)
    # print(Djk)
    # for vertex in range(len(Djk)):
    #     print("Distance from vertex 0 to vertex", vertex, "is", Djk[vertex])
        
    # print("Vertices of Graph")
    # print(G.get_vertex())
    # print("Edges of Graph")
    # print(G.get_edges())
    # print("Adjacency Matrix of Graph")
    # print(G.get_matrix())
    #This code is contributed by Rajat Singhal

    # SB_ = GraphSB.Solver(S.job_Count, S.machine_Count, S.lines_Order, S.lines_p, S.lines_r, S.lines_d)
    # fileName = _path + "\\Ciktilar\\ShiftingBottleneck_" + datetime.now().strftime("%I.%M%p on %B %d, %Y")
    # fileHandler = FileOperations(fileName)
    # fileHandler.open_files(fileName)
    # fileHandler.write_files("\nShiftingBottleneck.py\n\nlines_Order:")
    # makespan = G.ScheduleAll()


# # %% FCFS Yani ilk gelen ilk hizmet alýr  os.path.join(os.path.dirname(os.path.realpath(__file__)),
    # folderNumber = "sayfa (1)"
    folderNumber = "100-1"
    folderName = _path + "\\instances\\ABZ5_Sonuclar\\" + folderNumber
    folderName2 = _path + "\\instances\\ABZ5_Sonuclar\\"
    NumberOfSolutions = 100
    fileName = _path + "\\Ciktilar\\Algorithm3_"+ folderNumber +"_" + datetime.now().strftime("%I.%M%p on %B %d, %Y")
    fileHandler = FileOperations(fileName)
    fileHandler.open_files(fileName)
    sonuc_xx = S.Read()
    
    fileHandler.list_files(folderName)
    # Check_files = fileHandler.CalculateIfThereIsFile(folderName)
    Check_files = fileHandler.CalcAlgorithm3(folderName, folderName2, NumberOfSolutions)
    
    # # fileHandler.open_files(fileName)
    fileHandler.write_files("\nSiradanCizelgeleme.py\n")
    makespan = S.Baslangic_r_degerleri_Hesapla()    
    for ss1 in range(S.machine_Count):
        print(S.s2r[ss1])
    
    # %% SB Deneme
    # fileName = _path + "\\Ciktilar\\ShiftingBottleneck_" + datetime.now().strftime("%I.%M%p on %B %d, %Y")
    # fileHandler = FileOperations(fileName)
    # fileHandler.open_files(fileName)
    # fileHandler.write_files("\nShiftingBottleneck.py\n")
    # S2 = SB_.SB_Solver(S.file_path)
    # makespan, word = S2.MainFunc()
    # iterasyon 1
    #--Makespan deðerlerine göre sýrasýyla tüm makineleri Schrage yap
    #--Sonra Makespan deðerlerine göre 2. en yüksek makineyi ilk sýrada yapýp tüm makineleri Schrage yap
    #--Sonra Makespan deðerlerine göre 3-(en iyi 1-2 sýrasý) yada (en iyi 1-2 sýrasý)-3 yapýp tüm makineleri Schrage yap
    #--Sonra Makespan deðerlerine göre 4-(en iyi 1-2-3 sýrasý) yada (en iyi 1-2-3 sýrasý)-4 yapýp tüm makineleri Schrage yap
    
    
# %% MakineToplamSurelerineGore
    # fileName = _path + "\\Ciktilar\\MakineToplamSürelerineGoreCizelgeleme_" + datetime.now().strftime("%I.%M%p on %B %d, %Y")
    # fileHandler = FileOperations(fileName)
    # fileHandler.open_files(fileName)
    # fileHandler.write_files("\nMakineToplamSürelerineGoreCizelgeleme.py\n")
    # makespan = S.MakineToplamSurelerineGoreCizelgele()

    
# %% SPT
#     fileName = _path + "\\Ciktilar\\SPT_Orj" + datetime.now().strftime("%I.%M%p on %B %d, %Y")
#     fileHandler = FileOperations(fileName)
#     fileHandler.open_files(fileName)
#     fileHandler.write_files("\nSPT_Orj.py\n")
#     makespan = S.SPT_Orj() 
    
    # fileName = _path + "\\Ciktilar\\SPT_v1_" + datetime.now().strftime("%I.%M%p on %B %d, %Y")
    # fileHandler = FileOperations(fileName)
    # fileHandler.open_files(fileName)
    # fileHandler.write_files("\nSPT_v1.py\n")
    # makespan = S.SPT_v1()    
    
#     fileName = _path + "\\Ciktilar\\SPT_v2_" + datetime.now().strftime("%I.%M%p on %B %d, %Y")
#     fileHandler = FileOperations(fileName)
#     fileHandler.open_files(fileName)
#     fileHandler.write_files("\nSPT_v2.py\n")
#     makespan = S.SPT_v2()
    
    
# %% LPT
    # fileName = _path + "\\Ciktilar\\LPT_Orj" + datetime.now().strftime("%I.%M%p on %B %d, %Y")
    # fileHandler = FileOperations(fileName)
    # fileHandler.open_files(fileName)
    # fileHandler.write_files("\nLPT_Orj.py\n")
    # makespan = S.LPT_Orj() 
    
    # fileName = _path + "\\Ciktilar\\LPT_v1_" + datetime.now().strftime("%I.%M%p on %B %d, %Y")
    # fileHandler = FileOperations(fileName)
    # fileHandler.open_files(fileName)
    # fileHandler.write_files("\nLPT_v1.py\n")
    # makespan = S.LPT_v1()    
    
    # fileName = _path + "\\Ciktilar\\LPT_v2_" + datetime.now().strftime("%I.%M%p on %B %d, %Y")
    # fileHandler = FileOperations(fileName)
    # fileHandler.open_files(fileName)
    # fileHandler.write_files("\nLPT_v2.py\n")
    # makespan = S.LPT_v2()
    
    
# %% txt üst bilgilerini Yazdýrma  
    #solver.s2r[0][0] = 31
    #solver.s2r[5][3] = 104
    # fileHandler.write_files("\n s2Order: ")
    # for a1 in range(S.machine_Count):
    #     word = word + "\n"
    #     for a2 in range(S.job_Count):
    #         word = word + str(S.s2o[a1][a2]) + "\t"
    # fileHandler.write_files(word)
    # word = ""
    # fileHandler.write_files("\n s2r: ")
    # for a1 in range(S.machine_Count):
    #     word = word + "\n"
    #     for a2 in range(S.job_Count):
    #         word = word + str(S.s2r[a1][a2]) + "\t"# fileHandler.write_files(word)
    # fileHandler.write_files(word)
    # word = ""
    # fileHandler.write_files("\n job_Order: ")
    # for a1 in range(S.job_Count):
    #     word = word + "\n"
    #     for a2 in range(S.machine_Count):
    #         word = word + str(S.l2r[a1][a2]) + "\t"# fileHandler.write_files(word)
    # fileHandler.write_files(word)
    # word = ""
    # fileHandler.write_files("\n As The Jobs ")
    # for a1 in range(S.job_Count):
    #     word = word + "\n"
    #     for a2 in range(S.machine_Count):
    #         word = word + str(S.s2r[S.lines_Order[a1][a2]][S.s2x[a1][a2]]) + "_" + str(S.lines_p[a1][a2]) + "\t"# fileHandler.write_files(word)
    # fileHandler.write_files(word)
    
# %% Kontrol ve Performans Hesaplama 
    # fileHandler.write_files(S.sr2_KontrolEt())
    # fileHandler.write_files(S.PerformansHesapla())
    # fileHandler.write_files(S.PerformansHesapla2())
    # S.GanttChartShow(S.machine_Count, S.job_Count, fileName, S.machine_Count, makespan)
    fileHandler.close_files()  
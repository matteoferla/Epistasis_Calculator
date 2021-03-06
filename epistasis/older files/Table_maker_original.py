# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:04:56 2018

@author: Poul
"""
#here the first table code
import random
from random import randint
import numpy
import pandas
import math
"""
I have added some comments here and there to help you understand the code. I hope it will be alright, sorry for the mess !
CRUCIAL HOW TO RUN : 
1) First run the programm until the line with "checkpoint table 1" (around line 100)
3) complete carefully what the programm asks, this will influence a lot what the output is
2) you will get an excel in which you have the different mutants, in this excel put the experimental replicates values instead of the "X"
3) then run the rest of the program, you will get a second excel with the results !

"""
mutations_list = []
replicate_list = []
mutant_list = []
value_list=[]
your_study = input("Do you use selectivity or conversion values? Please answer with S (Selectivity) or C (Conversion): ")
mutation_number = int(input("Please indicate your mutation number: "))
replicate_number = int(input("Please indicate your replicate number (if some replicates are faulty, please fill the table with the average of the others otherwise the program might give unexpected results) : "))
your_data = input("Please enter the name of your replicate table (don't forget the file extension !): ")
your_data2 = input("Please enter the name of the file you want your results in (don't forget the file extension !): ")
#very important lines that determine a lot the output of the code. This gives flexibility to the code and intercations with the user.
for elt3 in range(1, replicate_number+1):
    replicate_list.append("Replicate n°%s" % (elt3))
for elt2 in range(1,mutation_number+1):
    mutations_list.append(input("Please indicate the mutation n°%s: " % (elt2)))
for elt4 in range(1,2**mutation_number+1):
    mutant_list.append("Mutant %s" % (elt4)) #these lines are very imortant to make a list of the mutations, a list of the replicates names and the mutants names. They will be used to make the table and combinations.

def create_combination(mutation_number):#this function creates the mutant combinations based on the number you indicated
    dic_list = []
    while len(mutant_list)>len(dic_list):
        for elt in mutant_list:
            elt = {}
            for elt2 in range(1, mutation_number+1): #here we attribute a number for + and - and roll the dice to obtain a random combination under the form of a dictionary !
                evolution_dice = random.randint(0,1)
                if evolution_dice == 0:
                    elt[mutations_list[elt2-1]] = "+"
                else:
                    elt[mutations_list[elt2-1]] = "-"
            count = 0
            for elt3 in dic_list:
                if elt.items() != elt3.items(): #this line will scan each combination of the list and compare it to the new combination
                        count+= 1
            if count == len(dic_list):
                dic_list.append(elt) #we add this combination to a new list. If this combination is already in the list, then we thrash it and do it again
        
    return dic_list

Mutant_number = len(create_combination(mutation_number)) #the number of mutants if equal to the number of combinations
box = ["X"]*Mutant_number*(mutation_number+replicate_number) #here we make a number of empty cases filled with "X"proportional to the number of mutants and mutations
final_table1 = numpy.reshape(box,((Mutant_number),(mutation_number+len(replicate_list))))  #here we make a matrix with the boxes above with the number of rows being equal to the number of mutants and the number of column being equal to the number of mutations + the number of replicates

for mutant in create_combination(mutation_number):
    sign_list = []
    for combinations in mutant:
        sign_list.append(mutant[combinations])
    value_list.append(sign_list) #this creates a list of the the combinations

def value_list_sorter(value_list): #this put the combinations of signs together based on the number of + they have
    sorted_values = []
    final = []
    ref_list = []
    count = 0
    value_dic = {}
    for value in value_list:
        count = value.count("+")
        ref_list.append(count)
        value_dic[str(value)]=count
    ref_list.sort()
    for num in ref_list:
        for item in value_dic.items():
            if num == item[1]:
                sorted_values.append(item[0])
                del value_dic[item[0]]
                break
    for elt in sorted_values:
        for elt2 in value_list:
            if elt == str(elt2):
                final.append(elt2)
    return final
final_value_list = value_list_sorter(value_list) #this is our sorted sign list !
def table_filler(final_table1, final_value_list, mutation_number):#this will fill the matrix with our ordered sign list
    i = 0
    while i < mutation_number:
        j = 0
        while j < len(mutant_list):
            final_table1[j][i] = final_value_list[j][i]
            j = j + 1
        i = i + 1
    return final_table1

excel_table1 = pandas.DataFrame(table_filler(final_table1, final_value_list, mutation_number), columns=mutations_list+replicate_list, index=mutant_list)
writer = pandas.ExcelWriter(your_data)
excel_table1.to_excel(writer, sheet_name="sheet_name", index = True)   #finally we write everything on a new excel, of which the name is given by the user
writer.close()
print("checkpoint after table1--------------------------------------------")

#from here the second table code


table1 = pandas.read_excel(your_data) #here we take the input given by the user in the excel tqble we previously generated
foundment = table1.iloc[:,:mutation_number]#foundment is the matrix of all the signs and mutants we obtained above
total_replicate_data = table1.iloc[:, mutation_number:]
replicate_matrix = total_replicate_data.values #this isolates the values that the user put in the input excel file. That way we obtain a matrix with the number of lines = number of mutants and number of columns = number of replicates
data_array = table1.values#This is all the data (signs/mutants and associated replicates)

def mean_and_sd_maker(data_array): #this function will look into the vqlues of each mutants and make an average and standard deviation out of it. In the final table those are called "experimental average" and "experimental standard deviation"
    data_dic = {}
    mean_and_sd = []
    for array in data_array:
        data = array[mutation_number:]
        data_float = numpy.array(data).astype(numpy.float64)
        mutant = str(array[:mutation_number])
        average = float(numpy.average(data_float))
        std = float(numpy.std(data_float))/math.sqrt(replicate_number)
        data_dic[mutant] = [average,std]
    for elt in data_dic.values():
        mean_and_sd.append(elt)
    return data_dic, mean_and_sd

#This function gives a tuple (dictionary of mutants associated with mean and std, array of mean and std)
mean_and_sd_dic = mean_and_sd_maker(data_array)[0] #here we just take the first element of the tuple, which is the dictionarry. I frankly don't even remember why I did a tuple and not just the dictionary but hey)
mean_and_sd_array = numpy.reshape(mean_and_sd_maker(data_array)[1], ((Mutant_number),2))
foundment_values = foundment.values #this line is to obtain readable values from the variable foundment, which will then be a matrix of signs.

def origin_finder(foundment_values): #this is the first function that will permit to find possible combinations between mutqnts. This one is useful to find double mutqnts. For exqmple [+ - + -] and [- + - +].
    additivity_list = []
    foundment_values[foundment_values == "+"] = 1 #here I change the + and - for 1 and 0. This is useful for calculations
    foundment_values[foundment_values == "-"] = 0
    i= 1
    while i < len(foundment_values)-1: #I go through the sign mqtrix
        j = i
        while j < len(foundment_values)-1:#and a second time, so I cqn isolqte two combinqtions qt q time qnd compare them
            res = foundment_values[i] + foundment_values[j+1] #so here we hqve this vqriqble "res". For example if the two combinations are [+ - +] and [- + -], res will be [1,1,1]. However, if the combinations are [+ + -] and [+ - +], res will be [2, 1, 1]
            for array in foundment_values: #we tqke this res and compare it to the mutants we have
                if numpy.array_equal(res, array) == True: #if res is equal to one of the mutant, we have found a combination !
                    additivity_list.append((list(res),(i+1,j+2))) #here we write the combination in a tuple with the combination and what mutants form it
            j = j + 1
        i = i + 1
    return additivity_list

origins = origin_finder(foundment_values)
def please_more_combinations(origins,foundment_values, mutations_list): #now is probably the trickiest function I had to do. The code above works for double mutants but not for triple, quadruple etc... The idea is that I use recurcivity to obtain new combinations
    final_comb_list = origins #we retake the combination list we obtain in the previous function
    cycle_number = len(mutations_list) #here we define the number of cycle the function will do. Everytime we have a new mutation the nuber of cycle increases by 1
    comb_comparator = []
    if cycle_number>1: #that is the recursivity condition. The function will stop after the number of cycles is down to one
        for comb in final_comb_list:#so the idea is to scan the comb list we obtained above. In that case we can make combinations of combinations to obtain more combinations !
            for array2 in foundment_values[1:]:
                res2 = numpy.array(comb[0] + array2)
                for array3 in foundment_values:
                    if numpy.array_equal(res2, array3) == True: #same principle as above
                        new_comb = list(comb[1])
                        new_comb.append(foundment_values.tolist().index(array2.tolist())+1)
                        count = 0
                        for elt in final_comb_list:
                            a_comb = list(elt[1])
                            a_comb.sort()
                            comb_comparator.append(a_comb)
                            new_comb.sort()
                        for elt2 in comb_comparator:#those lines make sure the newly formed combination has not been already made. This is probably a litle more complicated but I must admit I don't really recall everything
                            if elt2 == new_comb:
                                count += 1
                        if count == 0:
                            final_comb_list.append((list(res2), tuple(new_comb)))
        cycle_number = cycle_number - 1#we delete one cycle and go on
    else:
        please_more_combinations(final_comb_list)#and we repeat the function for the final cycle but with the final list as a variable
    return final_comb_list
        

all_combinations = please_more_combinations(origins,foundment_values, mutations_list)

#here will be made the combinations table
count_list = []
for elt in all_combinations:
    count_list.append((elt[0]).count(1))
count_list.sort() #this is just a variable coresponding to the number of combinations
ordered_combs = []
for elt in count_list:
    for elt2 in all_combinations:
        if list(elt2[0]).count(1) == elt:
            all_combinations.remove(elt2)
            ordered_combs.append(elt2)
#I think this was to remove any potential duplicate of combinations that somehow ended up in the list    

comb_index=[]
for elt in range(1,len(ordered_combs)+1):
    comb_index.append("Combination n°%s" % (elt))
#this line is important for the final table, it gives a proper name to each combination

combs_only = []
for elt in ordered_combs:
    combs_only.append(elt[1])
#this gives a list of the mutant combinations only
    
signs_only = []
for elt in ordered_combs:
    signs_only.append(elt[0])
#same as above but for the signs only 
    

reshaped_signs = numpy.reshape(signs_only, ((len(signs_only),(len(mutations_list)))))
reshaped_combs = numpy.reshape(combs_only, ((len(signs_only), 1)))
#reshqping everything to have a god format for the final table

final_comb_table = numpy.c_[reshaped_signs,reshaped_combs]
final_comb_table[final_comb_table == 1] = "+"
final_comb_table[final_comb_table == 0] = "-"
foundment_values[foundment_values == 1] = "+"
foundment_values[foundment_values == 0] = "-" #reconverting all 1 and 0 into + and - 
foundment_values = numpy.c_[foundment_values, mean_and_sd_array] #we also add the averages and standard deviation (experimental) to the sign matrix

def theoretical_stats_selectivity(mean_and_sd_dic, final_comb_table, combs_only, mean_and_sd_array):
    grand_final = []
    all_of_it = []
    for elt in final_comb_table:
        for elt2 in mean_and_sd_dic.keys():
            if str(elt[:mutation_number]) == str(elt2):
                elt = numpy.append(elt, list(mean_and_sd_dic[elt2]))
        for elt3 in combs_only:
            if numpy.array_equal(elt[len(mutations_list)], elt3) == True:
                theor_mean = numpy.array([0])
                replicate_values = numpy.zeros((1,len(replicate_matrix[0])))
                for elt4 in elt3:            
                    target = mean_and_sd_array[elt4-1][0]
                    theor_mean = numpy.add(theor_mean, target)
                    target2 =replicate_matrix[elt4-1]
                    replicate_values = numpy.add(replicate_values,target2)
                theor_sd = (numpy.std(replicate_values))/math.sqrt(replicate_number)
                elt =  numpy.append(elt, list(theor_mean))
                elt = numpy.append(elt, theor_sd)
                grand_final.append(elt)
    for elt5 in grand_final:
        at_last = (elt5[len(mutations_list)+1:][0])-(elt5[len(mutations_list)+1:][2])
        elt5 =  numpy.append(elt5, at_last)
        all_of_it.append(elt5)
        
    return numpy.array(all_of_it)
#the function above calculates the theoretical average and standard deviations based on the article that Carlos and his colleagues has written. This is for selectivity values

def theoretical_stats_conversion(mean_and_sd_dic, final_comb_table, combs_only, mean_and_sd_array):
    grand_final = []
    all_of_it = []
    keys = list(mean_and_sd_dic.keys())
    WT = keys[0]
    avgWT = mean_and_sd_dic[WT][0]
    for elt in final_comb_table:
        for elt2 in mean_and_sd_dic.keys():
            if str(elt[:mutation_number]) == str(elt2):
                elt = numpy.append(elt, list(mean_and_sd_dic[elt2]))
        for elt3 in combs_only:
            if numpy.array_equal(elt[len(mutations_list)], elt3) == True:
                theor_mean = numpy.array([0])
                replicate_values = numpy.zeros((1,len(replicate_matrix[0])))
                for elt4 in elt3:
                    new_target = []
                    target = mean_and_sd_array[elt4-1][0]-avgWT
                    theor_mean = numpy.add(theor_mean, target)
                    target2 =replicate_matrix[elt4-1]
                    for value in target2:
                        value = value - avgWT
                        new_target.append(value)
                    replicate_values = numpy.add(replicate_values,new_target)
                good_one = list(theor_mean)[0]
                good_one = avgWT+good_one
                theor_sd = (numpy.std(replicate_values))/math.sqrt(replicate_number)
                elt =  numpy.append(elt, good_one)
                elt = numpy.append(elt, theor_sd)
                grand_final.append(elt)
    for elt5 in grand_final:
        at_last = (elt5[len(mutations_list)+1:][0])-(elt5[len(mutations_list)+1:][2])
        elt5 =  numpy.append(elt5, at_last)
        all_of_it.append(elt5)
        
    return numpy.array(all_of_it)

#this time for conversion, which is a little different albeit very close. 
    
if your_study == "S": #at the very beginning of the code we ask for "selectivity" or "conversion" from the USER so that the program actually adapt to what the user wants. 
    all_of_it = theoretical_stats_selectivity(mean_and_sd_dic, final_comb_table, combs_only, mean_and_sd_array)
elif your_study == "C":
    all_of_it = theoretical_stats_conversion(mean_and_sd_dic, final_comb_table, combs_only, mean_and_sd_array)


def what_epistasis_sign_selectivity(all_of_it, replicate_matrix):
    sign = []
    epi_list = []
    what_epi = []
    i = 0
    for elt in all_of_it:
        noinspi = elt[len(mutations_list)+1:]
        Gexp = noinspi[0]
        Gexpstd = noinspi[1]
        Gcomb = noinspi[2]
        Gcombstd = noinspi[3]
        GexpES = Gexp - Gexpstd
        GcombES = Gcomb + Gcombstd
        GexpES2 = Gexp + Gexpstd
        GcombES2 = Gcomb - Gcombstd
        if GexpES < GcombES and Gexp > Gcomb: 
            sign.append("Additive")
        elif GexpES2 > GcombES2 and Gexp < Gcomb : 
            sign.append("Additive")
        elif Gexp < Gcomb :
            sign.append("- ")
        elif Gexp > Gcomb:
            sign.append("+ ")
    for elt2 in combs_only:
        combavg = []
        for lign in all_of_it:
            if lign[len(mutations_list)] == elt2:
                double_mutant_avg = lign[len(mutations_list)+1]
        for elt3 in elt2:
            mutant_avg = replicate_matrix[elt3-1]
            mutant_avg = float(numpy.average(mutant_avg))
            combavg.append(mutant_avg)
        count = 0
        for avg in combavg:
            if avg < 0: 
                count = count - 1
            elif avg > 0 : 
                count = count + 1
        if abs(count) == len(combavg):
            if count > 0 and double_mutant_avg > 0 or count < 0 and double_mutant_avg < 0:
                epi_list.append("Magnitude epistasis")
            elif count > 0 and double_mutant_avg < 0 or count < 0 and double_mutant_avg > 0:
                epi_list.append("Reciprocal sign epistasis")
        elif abs(count) != len(combavg):
            epi_list.append("Sign epistasis")
            
    while i < len(sign):
        if sign[i] != "Additive":
            what_epi.append(sign[i] + epi_list[i])
        else:
            what_epi.append(sign[i])
        i = i + 1
    return what_epi
#finally the great last function that also uses Carlos'equations to determine the nature of epistasis.
def what_epistasis_sign_conversion(all_of_it, replicate_matrix):
    sign = []
    epi_list = []
    what_epi = []
    i = 0
    keys = list(mean_and_sd_dic.keys())
    WT = keys[0]
    avgWT = mean_and_sd_dic[WT][0]
    for elt in all_of_it:
        noinspi = elt[len(mutations_list)+1:]
        Gexp = noinspi[0] - avgWT
        Gexpstd = noinspi[1]
        Gcomb = noinspi[2]- avgWT
        Gcombstd = noinspi[3]
        GexpES = Gexp - Gexpstd
        GcombES = Gcomb + Gcombstd
        GexpES2 = Gexp + Gexpstd
        GcombES2 = Gcomb - Gcombstd
        if GexpES < GcombES and Gexp > Gcomb: 
            sign.append("Additive")
        elif GexpES2 > GcombES2 and Gexp < Gcomb : 
            sign.append("Additive")
        elif Gexp < Gcomb :
            sign.append("- ")
        elif Gexp > Gcomb:
            sign.append("+ ")
    for elt2 in combs_only:
        combavg = []
        for lign in all_of_it:
            if lign[len(mutations_list)] == elt2:
                double_mutant_avg = lign[len(mutations_list)+1]
        for elt3 in elt2:
            mutant_avg = replicate_matrix[elt3-1] - avgWT
            mutant_avg = float(numpy.average(mutant_avg))
            combavg.append(mutant_avg)
        count = 0
        for avg in combavg:
            if avg < 0: 
                count = count - 1
            elif avg > 0 : 
                count = count + 1
        if abs(count) == len(combavg):
            if count > 0 and double_mutant_avg > 0 or count < 0 and double_mutant_avg < 0:
                epi_list.append("Magnitude epistasis")
            elif count > 0 and double_mutant_avg < 0 or count < 0 and double_mutant_avg > 0:
                epi_list.append("Reciprocal sign epistasis")
        elif abs(count) != len(combavg):
            epi_list.append("Sign epistasis")
            
    while i < len(sign):
        if sign[i] != "Additive":
            what_epi.append(sign[i] + epi_list[i])
        else:
            what_epi.append(sign[i])
        i = i + 1
    return what_epi
#similarily to before, conversion and sleectivity differ a little so I had to adapt the code
if your_study == "C":#same logic as before regarding adaptation of the code to what the user wants
    epistasis = what_epistasis_sign_conversion(all_of_it, replicate_matrix)
elif your_study == "S":
    epistasis = what_epistasis_sign_selectivity(all_of_it, replicate_matrix)
all_of_it = numpy.c_[all_of_it,epistasis]
#this all_of_it value is all the data we need, across the program we complete it as it goes


suppinfo = ["Combinations", "Experimental average", "Experimental standard deviation", "Theoretical average", "Theoretical standard deviation", "Exp.avg - Theor.avg", "Epistasis type"]

excel_table2= pandas.DataFrame(all_of_it, columns=mutations_list+suppinfo, index=comb_index)
excel_table3= pandas.DataFrame(foundment_values, columns=mutations_list+["Average", "Standard deviation"], index=mutant_list)
writer2 = pandas.ExcelWriter(your_data2)
excel_table2.to_excel(writer2, sheet_name="Theoretical results table", index = True)
excel_table3.to_excel(writer2, sheet_name="Experimental results table", index = True)
writer2.close()
#and here are the lines to write the final excel table ! THe final file has two sheet, one with all the values and combinations, and the other with the experimental values only and the single mutants.
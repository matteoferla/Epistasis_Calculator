# -*- coding: utf-8 -*-
__description__ = \
    """
I have added some comments here and there to help you understand the code. I hope it will be alright, sorry for the mess !
CRUCIAL HOW TO RUN : 
1) First run the programm until the line with "checkpoint table 1" (around line 100)
3) complete carefully what the programm asks, this will influence a lot what the output is
2) you will get an excel in which you have the different mutants, in this excel put the experimental replicates values instead of the "X"
3) then run the rest of the program, you will get a second excel with the results !

MF. Modded so it uses argparse.    
    """
__author__ = 'Paul. Classified by MF'
__version__ = '1.1'
__date__ = 'Mon Apr 16 21:04:56 2018'

import argparse, math, random, pandas
import numpy as np

##### METHODS #######

class Epistatic():
    """

    The original functionality of the script is retained as the class method `user_input` which will ask for input.
    The altered usage has a way of creating the scheme thusly:
                Epistatic.create_input_scheme('C', '3', '3', 'test.xlsx')
    Running from file and calculating and saving:
                Epistatic.from_file('C', 'raw.xlsx').calculate().save('wow.xlsx')
    Running from panda table:
                Epistatic.from_pandas('C',table)
    Running from values:
                Epistatic(your_study, mutation_number,replicate_number,replicate_list,mutations_list, mutant_list,foundment_values,data_array,replicate_matrix)
            Methods:
            * create_combination
            * mean_and_sd_maker
            * origin_finder
            * please_more_combinations
            * table_filler
            * theoretical_stats_conversion
            * theoretical_stats_selectivity
            * value_list_sorter
            * what_epistasis_sign_conversion
            * what_epistasis_sign_selectivity
            Class method: user_input for interactive input. (no parameters! `Epistasis.user_input()`)
            Attributes:
            TODO
    """

    @classmethod
    def create_input_scheme(cls,your_study, mutation_number,replicate_number,outfile='scheme.xlsx',replicate_list=None,mutations_list=None, mutant_list=None):
        ## Sanitise
        assert isinstance(your_study, str), 'Study can only be str value'
        mutation_number = int(mutation_number)
        replicate_number = int(replicate_number)
        assert isinstance(outfile, str), 'For now outfile and outfile2 can only be str value'
        for l in (replicate_list, mutations_list):
            if l:
                assert isinstance(l, list), 'replicate list and mutations_list can only be blank or lists of str'

        # This is really bad form. I modified the code before understanding that there were two programs in one.
        self=cls(your_study=your_study,
                 mutation_number=mutation_number,
                 replicate_number=replicate_number,
                 replicate_list=replicate_list,
                 mutations_list=mutations_list,
                 mutant_list=mutant_list)

        # these lines are very imortant to make a list of the mutations, a list of the replicates names and the mutants names. They will be used to make the table and combinations.

        Mutant_number = len(
            self.create_combination())  # the number of mutants if equal to the number of combinations
        box = ["X"] * Mutant_number * (self.mutation_number + self.replicate_number)  # here we make a number of empty cases filled with "X"proportional to the number of mutants and mutations
        final_table1 = np.reshape(box, (Mutant_number, (self.mutation_number + self.replicate_number)))
        # here we make a matrix with the boxes above with the number of rows being equal to the number of mutants and the number of column being equal to the number of mutations + the number of replicates

        value_list = [[mutant[combinations] for combinations in mutant] for mutant in self.create_combination()]
        # this creates a list of the the combinations

        final_value_list = self.value_list_sorter(value_list)  # this is our sorted sign list !

        excel_table1 = pandas.DataFrame(self.table_filler(final_table1, final_value_list),
                                        columns=self.mutations_list + self.replicate_list, index=self.mutant_list)
        writer = pandas.ExcelWriter(outfile)
        excel_table1.to_excel(writer, sheet_name="sheet_name",
                              index=True)  # finally we write everything on a new excel, of which the name is given by the user
        writer.close()

    @classmethod
    def from_file(cls,your_study, infile):
        # No sanitisation... TODO
        table = pandas.read_excel(infile)  # here we take the input given by the user in the excel tqble we previously generated
        return cls.from_pandas(your_study, table)

    @classmethod
    def from_pandas(cls,your_study, table):
        # Determine
        for mutation_number, v in enumerate(table.iloc[0]):
            if str(v) not in '-+':
                break
        replicate_number = len(table.iloc[0]) - mutation_number
        mutations_list=list(table)[:mutation_number]
        replicate_list=list(table)[mutation_number:]
        mutant_list = list(table.index)

        foundment = table.iloc[:,:mutation_number]  # foundment is the matrix of all the signs and mutants we obtained above
        foundment_values = foundment.values
        total_replicate_data = table.iloc[:, mutation_number:]
        replicate_matrix = total_replicate_data.values  # this isolates the values that the user put in the input excel file. That way we obtain a matrix with the number of lines = number of mutants and number of columns = number of replicates
        data_array = table.values  # This is all the data (signs/mutants and associated replicates)
        # none of the data passed is a pandas table...
        return cls(your_study=your_study,
                   mutation_number=mutation_number,
                   replicate_number=replicate_number,
                   replicate_list=replicate_list,
                   mutations_list=mutations_list,
                   mutant_list=mutant_list,
                   foundment_values=foundment_values,
                   data_array=data_array,
                   replicate_matrix=replicate_matrix)


    def __init__(self, your_study, mutation_number,replicate_number,replicate_list=None,mutations_list=None, mutant_list=None,foundment_values=None,data_array=None,replicate_matrix=None):
        """

        :param your_study: Do you use selectivity or conversion values? Please answer with S (Selectivity) or C (Conversion):
        :param mutation_number: Please indicate your mutation number:
        :param replicate_number: Please indicate your replicate number (if some replicates are faulty, please fill the table with the average of the others otherwise the program might give unexpected results) :
        :param replicate_list (optinal): Replicate n°%s
        :param mutations_list (optinal): Please indicate the mutation n°%s:
        :param mutant_list (optinal):
        :param foundment_values (optinal):  The +/- np array
        :param data_array (optinal):        All the np array
        :param replicate_matrix (optinal):  The number part of the np array
        """
        ## Compute
        if not mutations_list:
            mutations_list = ['M{}'.format(i) for i in range(1, mutation_number + 1)]
        if not replicate_list:
            replicate_list = ["Replicate n°%s" % (elt3) for elt3 in range(1, replicate_number + 1)]
        if not mutant_list:
            mutant_list = ["Mutant %s" % (elt4) for elt4 in range(1, 2 ** mutation_number + 1)]
        #not a loop because of copy.
        if isinstance(foundment_values,list):
            foundment_values = np.array(foundment_values)
        if isinstance(replicate_matrix,list):
            replicate_matrix = np.array(replicate_matrix)
        if isinstance(data_array,list):  # technically this should be generated... TODO
            data_array = np.array(data_array)


        ## Save
        local = locals()
        for variable in ('your_study',
                         'mutation_number',
                         'replicate_number',
                         'replicate_list',
                         'mutations_list',
                         'mutant_list',
                         'mutation_number',
                         'replicate_number',
                         'foundment_values',
                         'replicate_matrix',
                         'data_array'):
            setattr(self, variable, local[variable])
        # Preallocation
        self.mean_and_sd_dic=None
        self.mean_and_sd_array=None
        self.all_of_it=None
        self.final_comb_table=None
        self.combs_only=None
        self.comb_index=None

    def calculate(self):
        if type(self.foundment_values) is None:
            raise AssertionError('No data')

        # This function gives a tuple (dictionary of mutants associated with mean and std, array of mean and std)
        self.mean_and_sd_dic = self.mean_and_sd_maker()[0]  # here we just take the first element of the tuple, which is the dictionarry. I frankly don't even remember why I did a tuple and not just the dictionary but hey)
        # line with Mutant_number
        # self.mean_and_sd_array = np.reshape(self.mean_and_sd_maker(data_array)[1], ((Mutant_number), 2))
        self.mean_and_sd_array = np.reshape(self.mean_and_sd_maker()[1], (len(self.create_combination()), 2))
        origins = self.origin_finder()

        all_combinations = self.please_more_combinations(origins)

        # here will be made the combinations table
        count_list = []
        for elt in all_combinations:
            count_list.append((elt[0]).count(1))
        count_list.sort()  # this is just a variable coresponding to the number of combinations
        ordered_combs = []
        for elt in count_list:
            for elt2 in all_combinations:
                if list(elt2[0]).count(1) == elt:
                    all_combinations.remove(elt2)
                    ordered_combs.append(elt2)
        # I think this was to remove any potential duplicate of combinations that somehow ended up in the list
        self.comb_index = ["Combination n°%s" % (elt) for elt in range(1, len(ordered_combs) + 1)]
        # this line is important for the final table, it gives a proper name to each combination

        self.combs_only = [elt[1] for elt in ordered_combs]

        # this gives a list of the mutant combinations only
        signs_only = []
        for elt in ordered_combs:
            signs_only.append(elt[0])
        # same as above but for the signs only
        reshaped_signs = np.reshape(signs_only, ((len(signs_only), (len(self.mutations_list)))))
        reshaped_combs = np.reshape(self.combs_only, ((len(signs_only), 1)))
        # reshqping everything to have a god format for the final table

        #so a method (the origin one) was altering foundament and here is reverted. I made a copy of it as it was a fishy piece of code,
        # so no reconversion needed.
        self.final_comb_table = np.c_[reshaped_signs, reshaped_combs]
        self.final_comb_table[self.final_comb_table == 1] = "+"
        self.final_comb_table[self.final_comb_table == 0] = "-"
        temp=np.zeros(self.foundment_values.shape,dtype=str)  #purity of dtype
        temp[self.foundment_values == 1] = "+"
        temp[self.foundment_values == 0] = "-"  # reconverting all 1 and 0 into + and -
        self.foundment_values = np.c_[
            temp, self.mean_and_sd_array]  # we also add the averages and standard deviation (experimental) to the sign matrix

        # this time for conversion, which is a little different albeit very close.

        if self.your_study == "S":  # at the very beginning of the code we ask for "selectivity" or "conversion" from the USER so that the program actually adapt to what the user wants.
            all_of_it = self.theoretical_stats_selectivity()
        elif self.your_study == "C":
            all_of_it = self.theoretical_stats_conversion()

        # similarily to before, conversion and sleectivity differ a little so I had to adapt the code
        if self.your_study == "C":  # same logic as before regarding adaptation of the code to what the user wants
            epistasis = self.what_epistasis_sign_conversion(all_of_it)
        elif self.your_study == "S":
            epistasis = self.what_epistasis_sign_selectivity(all_of_it)
        self.all_of_it = np.c_[all_of_it, epistasis]
        # this all_of_it value is all the data we need, across the program we complete it as it goes
        return self

    ##### Other methods
    def save(self, outfile='out.xlsx'):
        suppinfo = ["Combinations", "Experimental average", "Experimental standard deviation", "Thoretical average",
                    "Theoretical standard deviation", "Exp.avg - Theor.avg", "Epistasis type"]

        excel_table2 = pandas.DataFrame(self.all_of_it, columns=self.mutations_list + suppinfo, index=self.comb_index)
        excel_table3 = pandas.DataFrame(self.foundment_values,
                                        columns=self.mutations_list + ["Average", "Standard deviation"],
                                        index=self.mutant_list)
        writer2 = pandas.ExcelWriter(outfile)
        excel_table2.to_excel(writer2, sheet_name="Theoretical results table", index=True)
        excel_table3.to_excel(writer2, sheet_name="Experimental results table", index=True)
        writer2.close()
        # and here are the lines to write the final excel table ! THe final file has two sheet, one with all the values and combinations, and the other with the experimental values only and the single mutants.

    def create_combination(self):
        """
        this function creates the mutant combinations based on the number you indicated in mutation_number
        :return: list of dicts
        """
        dic_list = []
        while len(self.mutant_list) > len(dic_list):
            for elt in self.mutant_list:
                elt = {}
                for elt2 in range(1,
                                  self.mutation_number + 1):  # here we attribute a number for + and - and roll the dice to obtain a random combination under the form of a dictionary !
                    evolution_dice = random.randint(0, 1)
                    if evolution_dice == 0:
                        elt[self.mutations_list[elt2 - 1]] = "+"
                    else:
                        elt[self.mutations_list[elt2 - 1]] = "-"
                count = 0
                for elt3 in dic_list:
                    if elt.items() != elt3.items():  # this line will scan each combination of the list and compare it to the new combination
                        count += 1
                if count == len(dic_list):
                    dic_list.append(
                        elt)  # we add this combination to a new list. If this combination is already in the list, then we thrash it and do it again

        return dic_list

    def value_list_sorter(self,value_list):
        """
        this put the combinations of signs together based on the number of + they have
        :param value_list:
        :return: list called final
        """
        sorted_values = []
        final = []
        ref_list = []
        count = 0
        value_dic = {}
        for value in value_list:
            count = value.count("+")
            ref_list.append(count)
            value_dic[str(value)] = count
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

    def table_filler(self,final_table1, final_value_list):
        """
        this will fill the matrix with our ordered sign list
        :param final_table1:
        :param final_value_list:
        :param mutation_number:
        :return:
        """
        i = 0
        while i < self.mutation_number:
            j = 0
            while j < len(self.mutant_list):
                final_table1[j][i] = final_value_list[j][i]
                j = j + 1
            i = i + 1
        return final_table1

    def mean_and_sd_maker(self):
        """
        this function will look into the vqlues of each mutants and make an average and standard deviation out of it.
        In the final table those are called "experimental average" and "experimental standard deviation
        :return:
        """
        data_dic = {}
        mean_and_sd = []
        for array in self.data_array:
            data = array[self.mutation_number:]
            data_float = np.array(data).astype(np.float64)
            mutant = str(array[:self.mutation_number])
            average = float(np.average(data_float))
            std = float(np.std(data_float)) / math.sqrt(self.replicate_number)
            data_dic[mutant] = [average, std]
        for elt in data_dic.values():
            mean_and_sd.append(elt)
        return data_dic, mean_and_sd

    def origin_finder(self):
        """
        this is the first function that will permit to find possible combinations between mutqnts.
        This one is useful to find double mutqnts. For exqmple [+ - + -] and [- + - +].
        :param foundment_values:
        :return:
        """
        # I don't know why but this method alters foundment_values, which may not be intended? MF
        # actually this makes a shallow copy... so  shmeh
        foundment_values=self.foundment_values

        additivity_list = []
        if np.any(foundment_values == '+'):
            foundment_values[
                foundment_values == "+"] = 1  # here I change the + and - for 1 and 0. This is useful for calculations
            foundment_values[foundment_values == "-"] = 0
        i = 1
        while i < len(foundment_values) - 1:  # I go through the sign mqtrix
            j = i
            while j < len(
                    foundment_values) - 1:  # and a second time, so I cqn isolqte two combinqtions qt q time qnd compare them
                res = foundment_values[i] + foundment_values[j + 1]
                # so here we hqve this vqriqble "res". For example if the two combinations are [+ - +] and [- + -], res will be [1,1,1]. However, if the combinations are [+ + -] and [+ - +], res will be [2, 1, 1]
                for array in foundment_values:  # we tqke this res and compare it to the mutants we have
                    if np.array_equal(res,
                                         array) == True:  # if res is equal to one of the mutant, we have found a combination !
                        additivity_list.append((list(res), (i + 1,
                                                            j + 2)))  # here we write the combination in a tuple with the combination and what mutants form it
                j = j + 1
            i = i + 1
        return additivity_list

    def please_more_combinations(self,origins):
        """
        now is probably the trickiest function I had to do. The code above works for double mutants but not for triple, quadruple etc...
        The idea is that I use recurcivity to obtain new combinations
        :param origins:
        :param foundment_values:
        :return:
        """
        final_comb_list = origins  # we retake the combination list we obtain in the previous function
        cycle_number = len(
            self.mutations_list)  # here we define the number of cycle the function will do. Everytime we have a new mutation the nuber of cycle increases by 1
        comb_comparator = []
        if cycle_number > 1:  # that is the recursivity condition. The function will stop after the number of cycles is down to one
            for comb in final_comb_list:  # so the idea is to scan the comb list we obtained above. In that case we can make combinations of combinations to obtain more combinations !
                for array2 in self.foundment_values[1:]:
                    res2 = np.array(comb[0] + array2)
                    for array3 in self.foundment_values:
                        if np.array_equal(res2, array3) == True:  # same principle as above
                            new_comb = list(comb[1])
                            new_comb.append(self.foundment_values.tolist().index(array2.tolist()) + 1)
                            count = 0
                            for elt in final_comb_list:
                                a_comb = list(elt[1])
                                a_comb.sort()
                                comb_comparator.append(a_comb)
                                new_comb.sort()
                            for elt2 in comb_comparator:  # those lines make sure the newly formed combination has not been already made. This is probably a litle more complicated but I must admit I don't really recall everything
                                if elt2 == new_comb:
                                    count += 1
                            if count == 0:
                                final_comb_list.append((list(res2), tuple(new_comb)))
            cycle_number = cycle_number - 1  # we delete one cycle and go on
        else:
            self.please_more_combinations(
                final_comb_list)  # and we repeat the function for the final cycle but with the final list as a variable
        return final_comb_list

    def theoretical_stats_selectivity(self):
        """
        the function above calculates the theoretical average and standard deviations based on the article that Carlos and his colleagues has written. This is for selectivity values
        :return:
        """
        grand_final = []
        all_of_it = []
        for elt in self.final_comb_table:
            for elt2 in self.mean_and_sd_dic.keys():
                if str(elt[:self.mutation_number]) == str(elt2):
                    elt = np.append(elt, list(self.mean_and_sd_dic[elt2]))
            for elt3 in self.combs_only:
                if np.array_equal(elt[len(self.mutations_list)], elt3) == True:
                    theor_mean = np.array([0])
                    replicate_values = np.zeros((1, len(self.replicate_matrix[0])))
                    for elt4 in elt3:
                        target = self.mean_and_sd_array[elt4 - 1][0]
                        theor_mean = np.add(theor_mean, target)
                        target2 = self.replicate_matrix[elt4 - 1]
                        replicate_values = np.add(replicate_values, target2)
                    theor_sd = (np.std(replicate_values)) / math.sqrt(self.replicate_number)
                    elt = np.append(elt, list(theor_mean))
                    elt = np.append(elt, theor_sd)
                    grand_final.append(elt)
        for elt5 in grand_final:
            at_last = (elt5[len(self.mutations_list) + 1:][0]) - (elt5[len(self.mutations_list) + 1:][2])
            elt5 = np.append(elt5, at_last)
            all_of_it.append(elt5)

        return np.array(all_of_it)

    def theoretical_stats_conversion(self):
        grand_final = []
        all_of_it = []
        keys = list(self.mean_and_sd_dic.keys())
        WT = keys[0]
        avgWT = self.mean_and_sd_dic[WT][0]
        for elt in self.final_comb_table:
            for elt2 in self.mean_and_sd_dic.keys():
                print(str(elt[:self.mutation_number]).replace("'","").replace(" ",""),str(elt2).replace('0.','-').replace('1.','+').replace("'","").replace("'","").replace(" ",""))
                if str(elt[:self.mutation_number]).replace("'","").replace("'","").replace(" ","") == str(elt2).replace('0.','-').replace('1.','+').replace("'","").replace("'","").replace(" ",""):
                    elt = np.append(elt, list(self.mean_and_sd_dic[elt2]))
                    print('MATCH')
            for elt3 in self.combs_only:
                if np.array_equal(elt[len(self.mutations_list)], elt3) == True:
                    theor_mean = np.array([0])
                    replicate_values = np.zeros((1, len(self.replicate_matrix[0])))
                    for elt4 in elt3:
                        new_target = []
                        target = self.mean_and_sd_array[elt4 - 1][0] - avgWT
                        theor_mean = np.add(theor_mean, target)
                        target2 = self.replicate_matrix[elt4 - 1]
                        for value in target2:
                            value = value - avgWT
                            new_target.append(value)
                        replicate_values = np.add(replicate_values, new_target)
                        #print(replicate_values)
                    good_one = list(theor_mean)[0]
                    good_one = avgWT + good_one
                    theor_sd = (np.std(replicate_values)) / math.sqrt(self.replicate_number)
                    elt = np.append(elt, good_one)
                    elt = np.append(elt, theor_sd)
                    grand_final.append(elt)
        print('mutationlist',self.mutations_list)
        print('grand_final',grand_final)
        for elt5 in grand_final:
            at_last = (elt5[len(self.mutations_list) + 1:][0]) - (elt5[len(self.mutations_list) + 1:][2])
            elt5 = np.append(elt5, at_last)
            all_of_it.append(elt5)

        return np.array(all_of_it)

    def what_epistasis_sign_selectivity(self,all_of_it):
        sign = []
        epi_list = []
        what_epi = []
        i = 0
        for elt in all_of_it:
            noinspi = elt[len(self.mutations_list) + 1:]
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
            elif GexpES2 > GcombES2 and Gexp < Gcomb:
                sign.append("Additive")
            elif Gexp < Gcomb:
                sign.append("- ")
            elif Gexp > Gcomb:
                sign.append("+ ")
        for elt2 in self.combs_only:
            combavg = []
            for lign in all_of_it:
                if lign[len(self.mutations_list)] == elt2:
                    double_mutant_avg = lign[len(self.mutations_list) + 1]
            for elt3 in elt2:
                mutant_avg = self.replicate_matrix[elt3 - 1]
                mutant_avg = float(np.average(mutant_avg))
                combavg.append(mutant_avg)
            count = 0
            for avg in combavg:
                if avg < 0:
                    count = count - 1
                elif avg > 0:
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

    # finally the great last function that also uses Carlos'equations to determine the nature of epistasis.
    def what_epistasis_sign_conversion(self,all_of_it):
        sign = []
        epi_list = []
        what_epi = []
        i = 0
        keys = list(self.mean_and_sd_dic.keys())
        WT = keys[0]
        avgWT = self.mean_and_sd_dic[WT][0]
        for elt in all_of_it:
            noinspi = elt[len(self.mutations_list) + 1:]
            Gexp = noinspi[0] - avgWT
            Gexpstd = noinspi[1]
            Gcomb = noinspi[2] - avgWT
            Gcombstd = noinspi[3]
            GexpES = Gexp - Gexpstd
            GcombES = Gcomb + Gcombstd
            GexpES2 = Gexp + Gexpstd
            GcombES2 = Gcomb - Gcombstd
            if GexpES < GcombES and Gexp > Gcomb:
                sign.append("Additive")
            elif GexpES2 > GcombES2 and Gexp < Gcomb:
                sign.append("Additive")
            elif Gexp < Gcomb:
                sign.append("- ")
            elif Gexp > Gcomb:
                sign.append("+ ")
        for elt2 in self.combs_only:
            combavg = []
            for lign in all_of_it:
                if lign[len(self.mutations_list)] == elt2:
                    double_mutant_avg = lign[len(self.mutations_list) + 1]
            for elt3 in elt2:
                mutant_avg = self.replicate_matrix[elt3 - 1] - avgWT
                mutant_avg = float(np.average(mutant_avg))
                combavg.append(mutant_avg)
            count = 0
            for avg in combavg:
                if avg < 0:
                    count = count - 1
                elif avg > 0:
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

    ############# Alt input

    @classmethod
    def user_input(cls):
        """
        The old input via `input()`, now a class method. Calling thusly:
            Epistatic.user_input()
        :return: a normal instance.
        """
        # here the first table code
        mutations_list = []
        replicate_list = []
        your_study = input(
            "Do you use selectivity or conversion values? Please answer with S (Selectivity) or C (Conversion): ")
        mutation_number = int(input("Please indicate your mutation number: "))
        replicate_number = int(input(
            "Please indicate your replicate number (if some replicates are faulty, please fill the table with the average of the others otherwise the program might give unexpected results) : "))
        your_data = input("Please enter the name of your replicate table (don't forget the file extension !): ")
        outfile = input(
            "Please enter the name of the file you want your results in (don't forget the file extension !): ")
        # very important lines that determine a lot the output of the code. This gives flexibility to the code and intercations with the user.
        for elt3 in range(1, replicate_number + 1):
            replicate_list.append("Replicate n°%s" % (elt3))
        for elt2 in range(1, mutation_number + 1):
            mutations_list.append(input("Please indicate the mutation n°%s: " % (elt2)))
        #call class to make instance
        Epistatic.create_input_scheme(your_study, mutation_number,replicate_number,your_data,replicate_list=replicate_list,mutations_list=mutations_list)
        input('Please add data to the file {},save and then press the Any key.'.format(your_data))
        Epistatic.from_file(your_study, your_data).calculate().save(outfile)

if __name__ == "__main__":
    # your_study, mutation_number, replicate_number, your_data, outfile, replicate_list, mutations_list)
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("your_study", help="Do you use selectivity or conversion values? Please answer with S (Selectivity) or C (Conversion)")
    parser.add_argument("mutation_number",type=int, help="Please indicate your mutation number:")
    parser.add_argument("replicate_number",type=int, help="Please indicate your replicate number (if some replicates are faulty, please fill the table with the average of the others otherwise the program might give unexpected results)")
    parser.add_argument("your_data", help="Please enter the name of your replicate table (don't forget the file extension !): (Put the name of the excel file you want your first table to be in)")
    parser.add_argument("outfile", help="Please enter the name of the file you want your results in (don't forget the file extension !): (same here but for the excel you want your results in)")
    parser.add_argument('--version', action='version', version=__version__)
    args = parser.parse_args()
    #TODO... alter
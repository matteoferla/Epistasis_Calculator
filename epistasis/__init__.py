__author__ = 'Paul. Made OO by MF'
__version__ = '1.3'
__date__ = '3 Sept 2020'

import numpy as np
from warnings import warn
import math, random

from .epi_aux_mixin import EpiAuxMixin as _EA
from .epi_base_mixin import EpiBaseMixin as _EB

from typing import List


class Epistatic(_EA, _EB):
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
            * theoretical_stats
            * value_list_sorter
            * what_epistasis_sign
            Class method: user_input for interactive input. (no parameters! `Epistasis.user_input()`)
            Attributes:
            TODO
    """

    # ============== Central method ====================================================================================

    def calculate(self):
        if type(self.foundment_values) is None:
            raise AssertionError('No data')

        # This function gives a tuple (dictionary of mutants associated with mean and std, array of mean and std)
        self.mean_and_sd_dic = self.mean_and_sd_maker()[0]
        # here we just take the first element of the tuple,
        # which is the dictionarry. I frankly don't even remember why I did a tuple and not just the dictionary but hey)
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
        self.comb_index = [f"Combination n°{elt}" for elt in range(1, len(ordered_combs) + 1)]
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

        # so a method (the origin one) was altering foundament and here is reverted.
        # I made a copy of it as it was a fishy piece of code,
        # so no reconversion needed.
        self.final_comb_table = np.c_[reshaped_signs, reshaped_combs]
        self.final_comb_table[self.final_comb_table == 1] = "+"
        self.final_comb_table[self.final_comb_table == 0] = "-"
        temp = np.zeros(self.foundment_values.shape, dtype=str)  # purity of dtype
        temp[self.foundment_values == 1] = "+"
        temp[self.foundment_values == 0] = "-"  # reconverting all 1 and 0 into + and -
        self.foundment_values = np.c_[temp, self.mean_and_sd_array]
        # we also add the averages and standard deviation (experimental) to the sign matrix

        # this time for conversion, which is a little different albeit very close.

        # the "selectivity" or "conversion" difference (self.your_study) is handled now by the avgWT dyn property
        all_of_it = self.theoretical_stats()
        epistasis = self.what_epistasis_sign(all_of_it)
        self.all_of_it = np.c_[all_of_it, epistasis]
        # this all_of_it value is all the data we need, across the program we complete it as it goes
        return self

    # ============== property methods ==================================================================================

    _avgWT = None # cached property
    @property
    def avgWT(self):
        # avgWT is zero for selectivity.
        if self._avgWT is not None:
            pass
        elif self.your_study == 'S':
            self._avgWT = 0
        elif self.your_study == 'C':
            WT = list(self.mean_and_sd_dic.keys())[0]  # This seems dangerous
            self._avgWT = self.mean_and_sd_dic[WT][0]
        else:
            raise ValueError
        return self._avgWT

    # ============== Dependant methods =================================================================================

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
                                  self.mutation_number + 1):
                    # here we attribute a number for + and - and roll the dice to obtain a random combination under
                    # the form of a dictionary !
                    evolution_dice = random.randint(0, 1)
                    if evolution_dice == 0:
                        elt[self.mutations_list[elt2 - 1]] = "+"
                    else:
                        elt[self.mutations_list[elt2 - 1]] = "-"
                count = 0
                for elt3 in dic_list:
                    if elt.items() != elt3.items():
                        # this line will scan each combination of the list and compare
                        # it to the new combination
                        count += 1
                if count == len(dic_list):
                    dic_list.append(elt)
                    # we add this combination to a new list. If this combination is already in the list,
                    # then we thrash it and do it again

        return dic_list

    def value_list_sorter(self, value_list):
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

    def table_filler(self, final_table1, final_value_list):
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
        foundment_values = self.foundment_values
        additivity_list = []
        # foundment_values is a np.array of 1/0. however, user may have given a +/-
        if foundment_values.dtype == np.dtype('<U1'): # formerly: np.any(foundment_values == '+') (FutureWarning)
            foundment_values[foundment_values == "+"] = 1
            # here I change the + and - for 1 and 0. This is useful for calculations
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

    def please_more_combinations(self, origins):
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

    def theoretical_stats(self) -> np.ndarray:
        """
        the function above calculates the theoretical average and standard deviations based on the article that Carlos
        and his colleagues have written.

        This is a refactored method based on the observation that avgWT was the only difference.

        :return: np.ndarray
        """
        grand_final = []
        all_of_it = []
        # this operation, which I am not sure why it is needed, was repeated  - MF
        strigify = lambda table: str(table).replace('0', '-')\
                                           .replace('1', '+')\
                                           .replace('.', '')\
                                           .replace("'", "")\
                                           .replace("'", "")\
                                           .replace(" ","")
        # =========================================
        for elt in self.final_comb_table:
            # elt is np.ndarray: ['+' '+' '-' (2, 3)] to which stuff gets added...
            # ======== Empirical
            for elt2 in self.mean_and_sd_dic.keys(): # this is np.array of +/- in binary style
                if self.verbose: # present in conversion only
                    print(strigify(elt[:self.mutation_number]), strigify(elt2))
                if strigify(elt[:self.mutation_number]) == strigify(elt2):
                    elt = np.append(elt, list(self.mean_and_sd_dic[elt2]))
                    if self.verbose:
                        print('MATCH')
                    break
            else:
                raise ValueError('Experimental values could not be calculated because of odd +/- format')
            # ======== Theoretical
            for elt3 in self.combs_only:
                if np.array_equal(elt[len(self.mutations_list)], elt3) == True:
                    theor_mean = np.array([0])
                    replicate_values = np.zeros((1, len(self.replicate_matrix[0])))
                    for elt4 in elt3:
                        target = self.mean_and_sd_array[elt4 - 1][0] - self.avgWT # avgWT is 0 for S
                        target2 = self.replicate_matrix[elt4 - 1]
                        theor_mean = np.add(theor_mean, target)
                        replicate_values = np.add(replicate_values, target2)
                        # the following is new_target == target2 for argWT == 0
                        new_target = []
                        for value in target2:
                            value = value - self.avgWT
                            new_target.append(value)
                        replicate_values = np.add(replicate_values, new_target)
                        # print(replicate_values)
                    good_one = list(theor_mean)[0]
                    good_one = self.avgWT + good_one
                    theor_sd = (np.std(replicate_values)) / math.sqrt(self.replicate_number)
                    # NB. Blind refactoring: list(theor_mean) in S, good_one in C. Different types??
                    elt = np.append(elt, good_one)
                    elt = np.append(elt, theor_sd)
                    grand_final.append(elt)
                    # elt is a numpy.ndarray row ['+' '+' '+' (4, 5) 68.4 4.4 30.40 4.0]
                    # grand_final is a table
        if self.verbose:
            print('mutationlist', self.mutations_list)
            print('grand_final', grand_final)
        # =========================================
        for elt5 in grand_final:
            # ['+' '+' '-' (2, 3) 1.0 0.0]
            at_last = (elt5[len(self.mutations_list) + 1:][0]) - (elt5[len(self.mutations_list) + 1:][2])
            elt5 = np.append(elt5, at_last)
            all_of_it.append(elt5)
        return np.array(all_of_it)

    def what_epistasis_sign(self, all_of_it: np.ndarray) -> List[str]:
        sign = []
        epi_list = []
        what_epi = []
        i = 0
        for elt in all_of_it:
            noinspi = elt[len(self.mutations_list) + 1:]
            Gexp = noinspi[0] - self.avgWT
            Gexpstd = noinspi[1]
            Gcomb = noinspi[2] - self.avgWT
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
            else:
                sign.append("= ")
        for elt2 in self.combs_only:
            combavg = []
            for lign in all_of_it:
                if lign[len(self.mutations_list)] == elt2:
                    double_mutant_avg = lign[len(self.mutations_list) + 1]
            for elt3 in elt2:
                mutant_avg = self.replicate_matrix[elt3 - 1] - self.avgWT
                mutant_avg = float(np.average(mutant_avg))
                combavg.append(mutant_avg)
            count = 0
            for avg in combavg:
                if avg < 0:
                    count = count - 1
                elif avg > 0:
                    count = count + 1
                else:
                    pass
            if abs(count) == len(combavg):
                if count > 0 and double_mutant_avg > 0 or count < 0 and double_mutant_avg < 0:
                    epi_list.append("Magnitude epistasis")
                elif count > 0 and double_mutant_avg < 0 or count < 0 and double_mutant_avg > 0:
                    epi_list.append("Reciprocal sign epistasis")
                else:
                    raise ValueError('No idea. Unterminated if statement. MF')
            elif abs(count) != len(combavg):
                epi_list.append("Sign epistasis")
            else:
                raise ValueError('No idea. Unterminated if statement. MF')
        # end of combo_only loop
        while i < len(sign):
            if sign[i] != "Additive":
                what_epi.append(sign[i] + epi_list[i])
            else:
                what_epi.append(sign[i])
            i = i + 1
        return what_epi



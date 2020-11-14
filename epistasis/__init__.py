__author__ = 'Paul. Made OO by MF'
__version__ = '1.3'
__date__ = '3 Sept 2020'

import numpy as np
#from scipy.stats import ttest_ind_from_stats as ttest
from warnings import warn
import math, random

from .epi_aux_mixin import EpiAuxMixin as _EA
from .epi_base_mixin import EpiBaseMixin as _EB

from typing import List, Tuple, Union, Dict, Iterable


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
                Epistatic(your_study, mutation_number,replicate_number,replicate_list,mutation_names, mutant_list,foundment_values,data_array,replicate_matrix)
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

    The output can be accessed via .theoretical_results and .experimental_results pandas dataframes.
    """

    # ============== Central method ====================================================================================

    def calculate(self):
        if type(self.foundment_values) is None:
            raise AssertionError('No data')

        # This function gives a tuple (dictionary of mutants associated with mean and std, array of mean and std)
        if not self.mean_and_sd_dic:
            self.mean_and_sd_dic, array_mean_and_sd = self.mean_and_sd_maker()
        # here we just take the first element of the tuple,
        # which is the dictionarry. I frankly don't even remember why I did a tuple and not just the dictionary but hey)
        # line with Mutant_number
        # self.mean_and_sd_array = np.reshape(self.mean_and_sd_maker(data_array)[1], ((Mutant_number), 2))
        self.mean_and_sd_array = np.reshape(array_mean_and_sd, (len(self.create_combination()), 2))
        origins = self.origin_finder()
        all_combinations = self.please_more_combinations(origins)
        # ## here will be made the combinations table
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
        reshaped_signs = np.reshape(signs_only, ((len(signs_only), (len(self.mutation_names)))))
        # in the case of 2 mutants only the math needs a hack or (2,1) => (1,1) fails. MF
        # reshaped_combs normally is a np.array of tuples... but gets cast "incorrectly" when there's only one.
        if len(signs_only) != 1:  # more than 2
            reshaped_combs = np.reshape(self.combs_only, (len(signs_only), 1))
        else:
            reshaped_combs = np.zeros((1, 1)).astype(object)
            reshaped_combs[0, 0] = self.combs_only[0]

        # reshaping everything to have a good format for the final table

        # so a method (the origin one) was altering foundament and here is reverted.
        # I made a copy of it as it was a fishy piece of code,
        # so no reconversion needed.
        self.final_comb_table = np.c_[reshaped_signs, reshaped_combs]  # .astype('object')
        self.final_comb_table[self.final_comb_table == 1] = "+"
        self.final_comb_table[self.final_comb_table == 0] = "-"
        temp = np.zeros(self.foundment_values.shape, dtype=str)  # purity of dtype
        temp[self.foundment_values == 1] = "+"
        temp[self.foundment_values == 0] = "-"  # reconverting all 1 and 0 into + and -
        self.foundment_values = np.c_[temp, self.mean_and_sd_array]
        # we also add the averages and standard deviation (experimental) to the sign matrix
        # this time for conversion, which is a little different albeit very close.
        # the "selectivity" or "conversion" difference (self.your_study) is handled now by the avgWT dyn property
        self.stats = self.get_theoretical_stats()  # List[Dict[str, Union[str, float]]]
        # this all_of_it value is all the data we need, across the program we complete it as it goes
        return self

    # ============== property methods ==================================================================================

    _avgWT = None  # cached property

    @property
    def avgWT(self):
        # avgWT is zero for selectivity.
        if self._avgWT is not None:
            pass
        elif not self.wildtype_centred: # S-mode
            self._avgWT = 0
        elif self.wildtype_centred: # C-mode
            self._avgWT = self.mean_and_sd_dic[self.WT][0]
        else:
            raise ValueError
        return self._avgWT

    @property
    def WT(self):
        WT = '-' * self.mutation_number
        assert WT in self.mean_and_sd_dic, 'Please fill in WT or make a mutant the WT and remove datapoints without it.'
        return WT

    # ============== Dependant methods =================================================================================

    def create_combination(self) -> List[dict]:
        """
        this function creates the mutant combinations based on the number you indicated in mutation_number

        :return: list of dicts
        """
        dic_list = []
        while len(self.mutant_list) > len(dic_list):
            for i in self.mutant_list:
                elt = {}
                for elt2 in range(1, self.mutation_number + 1):
                    # here we attribute a number for + and - and roll the dice to obtain a random combination under
                    # the form of a dictionary !
                    evolution_dice = random.randint(0, 1)
                    if evolution_dice == 0:
                        elt[self.mutation_names[elt2 - 1]] = "+"
                    else:
                        elt[self.mutation_names[elt2 - 1]] = "-"
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
        for array in self.data_array: #[ 0. 0. 0. 40.408327 37.176372 35.776619]
            data = array[self.mutation_number:]
            data_float = np.array(data).astype(np.float64)
            mutant = self.strigify(array[:self.mutation_number])
            if not self.median: # mean
                average = float(np.nanmean(data_float))
            else:
                average = float(np.nanmedian(data_float))
            N_replicates = np.count_nonzero(~np.isnan(data_float))
            if N_replicates:  # non-empty row.
                std = float(np.nanstd(data_float)) / math.sqrt(N_replicates)
                data_dic[mutant] = [average, std]
            else:
                data_dic[mutant] = [np.nan, np.nan]
        for row in data_dic.values():
            mean_and_sd.append(row)
        return data_dic, mean_and_sd

    def origin_finder(self):
        """
        this is the first function that will permit to find possible combinations between mutqnts.
        This one is useful to find double mutqnts. For exqmple [+ - + -] and [- + - +].
        Returns a list of tuples of

        * +-+ as a 1,0 list and the combination

        [([1, 1, 0, 0], (2, 3)), ([1, 0, 1, 0], (2, 4)),

        :param foundment_values: 2D array of + - +
        :return:
        """
        # I don't know why but this method alters foundment_values, which may not be intended? MF
        # actually this makes a shallow copy... so  shmeh
        foundment_values = self.foundment_values  ## 2D array of + - +
        additivity_list = []
        # foundment_values is a np.array of 1/0. however, user may have given a +/-
        if foundment_values.dtype == np.dtype('<U1') or foundment_values.dtype == np.dtype('object'):
            # formerly: np.any(foundment_values == '+') (FutureWarning)
            foundment_values[foundment_values == "+"] = 1
            # here I change the + and - for 1 and 0. This is useful for calculations
            foundment_values[foundment_values == "-"] = 0
        else:
            pass
            # print('Not +-', foundment_values.dtype)
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
        now is probably the trickiest function I had to do.
        The code above works for double mutants but not for triple, quadruple etc...
        The idea is that I use recursivity to obtain new combinations

        :param origins:
        :param foundment_values:
        :return:
        """
        final_comb_list = origins  # we retake the combination list we obtain in the previous function
        cycle_number = len(
            self.mutation_names)  # here we define the number of cycle the function will do. Everytime we have a new mutation the nuber of cycle increases by 1
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

    def get_theoretical_stats(self) -> List[Dict[str, Union[str, float]]]:
        """
        the function above calculates the theoretical average and standard deviations based on the article that Carlos
        and his colleagues have written.

        This is a refactored method based on the observation that avgWT was the only difference.

        """
        data = []
        # =========================================
        for combination_row in self.final_comb_table:
            # combination_row is np.ndarray: ['+' '+' '-' (2, 3)] to which stuff gets added...
            signage = list(combination_row[:self.mutation_number])  # list +, -, +
            combination = combination_row[self.mutation_number]  # (2,3)
            # ======== Empirical
            emp_mean, emp_se = self._get_empirical_for_signage(signage)
            # ======== Theoretical
            theor_mean, theor_se = self._get_theoretical_for_combination(combination)
            # ======== store
            data.append({'signage': signage,
                         'combination': combination,
                         'emp_mean': emp_mean,
                         'emp_sd': emp_se,
                         'theor_mean': theor_mean,
                         'theor_sd': theor_se,
                         'diff': emp_mean - theor_mean,
                         'type': self.get_epistasis_sign(emp_mean, emp_se, theor_mean, theor_se, combination)
                         }
                        )
            # final_row was a numpy.ndarray row ['+' '+' '+' (4, 5) 68.4 4.4 30.40 4.0]
            # now it is a list of dict
            # grand_final is a table
            if self.verbose:
                print('mutationlist', self.mutation_names)
                print('grand_final', data)
            # =========================================
        return data

    def get_epistasis_sign(self, emp_mean, emp_se, theor_mean, theor_se, combination) -> str:
        nor_emp_mean = emp_mean - self.avgWT
        nor_theor_mean = theor_mean - self.avgWT
        emp_lower = nor_emp_mean - emp_se  # GexpES
        emp_upper = nor_emp_mean + emp_se  # GexpES2
        theor_upper = nor_theor_mean + theor_se  # GcombES
        theor_lower = nor_theor_mean - theor_se  # GcombES2
        # t,pvalue = ttest(mean1=nor_emp_mean, std1=emp_se * np.sqrt(self.replicate_number), nobs1=self.replicate_number,
        #                  mean2=nor_theor_mean, std2=theor_se * np.sqrt(self.replicate_number), nobs2=self.replicate_number,
        #                  equal_var=True) # possibly heteroskedatic. But dont think so.
        # if t > 0.05:
        #     return "Additive"  # no significant epistasis
        if nor_emp_mean >= nor_theor_mean and emp_lower <= theor_upper:
            return "Additive"  # no significant epistasis
        elif nor_emp_mean <= nor_theor_mean and emp_upper >= theor_lower:
            return "Additive"  # no significant epistasis
        elif nor_emp_mean < nor_theor_mean:
            sign = "-"
        elif nor_emp_mean > nor_theor_mean:
            sign = "+"
        else:
            raise ValueError("Mathematically Impossible")  # this is not correct.
        # determine if contribution sign is the same for all parent variants
        positivity = 0
        for parent in combination:  # former code: elt3 in elt2:
            positivity += 1 if self.get_empirical_for_element(parent)[0] - self.avgWT > 0 else -1
        if abs(positivity) != len(combination):
            # the contribution have different signs
            return f"{sign} Sign epistasis"
        elif (positivity > 0 and nor_emp_mean > 0) or (positivity < 0 and nor_emp_mean < 0):
            # all contribution have positive signs and the empirical mean is positive
            # all contribution have negative signs and the empirical mean is negative
            # former code: count > 0 and double_mutant_avg > 0 or count < 0 and double_mutant_avg < 0
            return f"{sign} Magnitude epistasis"
        elif (positivity > 0 and nor_emp_mean < 0) or (positivity < 0 and nor_emp_mean > 0):
            # all contribution have positive signs but the empirical mean is negative
            # all contribution have negative signs and the empirical mean is positive
            # former code: count > 0 and double_mutant_avg < 0 or count < 0 and double_mutant_avg > 0
            return f"{sign} Reciprocal sign epistasis"
        else:
            return "Insufficient data"

    def strigify(self, signage: Iterable) -> str:
        # [+,-,+] = +-+
        # this operation, which I am not sure why it is needed, was repeated  - MF
        convert = lambda value: value if isinstance(value, str) else ('-', '+')[int(value)]
        return (''.join([convert(x) for x in signage]).replace('0', '-')
                .replace('–', '-')  # en dash
                .replace('–', '-')  # em dash
                .replace('1', '+')
                .replace(',', '')
                .replace('.', '')
                .replace("'", "")
                .replace("'", "")
                .replace(" ", ""))

    def get_empirical_for_element(self, element: int) -> List[float]:
        """
        given a off-by-one empirical index return the avg and ste

        :param index: off-by-one index. 1 = wt.
        :return: avg & sd_err
        """
        signage = self.element2signage(element)
        return self.mean_and_sd_dic[signage]

    def element2signage(self, element: int) -> str:
        """
        Given an off-by-one element (1 = wt) returns the sign str (e.g. '+-+')

        :param element: int
        :return: +-+
        """
        return list(self.mean_and_sd_dic.keys())[element - 1]


    def _get_empirical_for_signage(self, signage: Iterable) -> List[float]:
        """
        Returns for a give sign str/list/np.ndarray the empirical theoretical mean and the se

        :param combination: (2,3) style.
        :return: mean, se
        """
        clean_signage = self.strigify(signage)
        if clean_signage in self.mean_and_sd_dic:
            return list(self.mean_and_sd_dic[clean_signage])
        else:
            raise ValueError(f'Experimental values could not be calculated because of odd +/- format ({signage} --> {clean_signage})')

    def _get_theoretical_for_combination(self, combination: Tuple[int]) -> List[float]:
        """
        Returns for a give combination the additive theoretical mean and the se

        :param combination: (2,3) style.
        :return:
        """
        parents_means = []
        parents_var = []
        for parent in combination:
            parents_means.append(self.get_empirical_for_element(parent)[0] - self.avgWT)
            replicates = np.array(self.data_array[parent - 1][self.mutation_number:]).astype(np.float64)
            parents_var.append(np.nanvar(replicates))
        theor_mean = np.nansum(parents_means) + self.avgWT
        theor_se = np.sqrt(np.nansum(parents_var)/self.replicate_number)
        return [theor_mean, theor_se]


        # So the theoretical mean/sd is the sum of the benefits of each
        # this is not quite correct.
        #parent_replicates = np.zeros((1, len(self.replicate_matrix[0])))
        # But isn't len(self.replicate_matrix[0]) simply 2^self.mutation_number?
        # the following is incorrect.
        # print('bg', self.avgWT)
        # for parent in combination:
        #     print(self.replicate_matrix[parent - 1])
        #     parent_replicates += self.replicate_matrix[parent - 1] - self.avgWT  # np elementwise
        # # the following ratio  is for sterr.
        # # The rooted part (N_replicates) is == len(replicates) if no nans present.
        # parent_replicates = parent_replicates.astype(np.float64)
        # N_replicates = np.count_nonzero(~np.isnan(parent_replicates))
        # theor_mean = np.nansum(parent_replicates) + self.avgWT
        # if N_replicates > 0:
        #     theor_sd = (np.nanstd(parent_replicates) / math.sqrt(N_replicates))
        #     # NB. Blind refactoring: list(theor_mean) in S, good_one in C. Different types??
        # else:
        #     theor_sd = np.nan
        #return theor_mean, theor_sd

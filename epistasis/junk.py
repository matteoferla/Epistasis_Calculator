class JunkEpi:
    """
    These are methods that are getting removed
    """

    def theoretical_stats_selectivity(self) -> np.ndarray:
        """
        the function above calculates the theoretical average and standard deviations based on the article that Carlos
        and his colleagues has written. This is for selectivity values
        :return:
        """
        warn('This method will likely be phased out', category=FutureWarning)
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
        if self.verbose:
            print('mutationlist', self.mutations_list)
            print('grand_final', grand_final)
        for elt5 in grand_final:
            at_last = (elt5[len(self.mutations_list) + 1:][0]) - (elt5[len(self.mutations_list) + 1:][2])
            elt5 = np.append(elt5, at_last)
            all_of_it.append(elt5)
        return np.array(all_of_it)

    def theoretical_stats_conversion(self) -> np.ndarray:
        warn('This method will likely be phased out', category=FutureWarning)
        grand_final = []
        all_of_it = []
        keys = list(self.mean_and_sd_dic.keys())
        WT = keys[0]
        avgWT = self.mean_and_sd_dic[WT][0]
        for elt in self.final_comb_table:
            for elt2 in self.mean_and_sd_dic.keys():
                if self.verbose:
                    print(str(elt[:self.mutation_number]).replace("'", "").replace(" ", ""),
                          str(elt2).replace('0.', '-').replace('1.', '+').replace("'", "").replace("'", "").replace(" ",
                                                                                                                    ""))
                if str(elt[:self.mutation_number]).replace("'", "").replace("'", "").replace(" ", "") == str(
                        elt2).replace('0.', '-').replace('1.', '+').replace("'", "").replace("'", "").replace(" ", ""):
                    elt = np.append(elt, list(self.mean_and_sd_dic[elt2]))
                    if self.verbose:
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
                        # print(replicate_values)
                    good_one = list(theor_mean)[0]
                    good_one = avgWT + good_one
                    theor_sd = (np.std(replicate_values)) / math.sqrt(self.replicate_number)
                    elt = np.append(elt, good_one)
                    elt = np.append(elt, theor_sd)
                    grand_final.append(elt)
        if self.verbose:
            print('mutationlist', self.mutations_list)
            print('grand_final', grand_final)
        for elt5 in grand_final:
            at_last = (elt5[len(self.mutations_list) + 1:][0]) - (elt5[len(self.mutations_list) + 1:][2])
            elt5 = np.append(elt5, at_last)
            all_of_it.append(elt5)
        return np.array(all_of_it)

    def what_epistasis_sign_selectivity(self, all_of_it) -> List[str]:
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
    def what_epistasis_sign_conversion(self, all_of_it) -> List[str]:
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
import pandas as pd
import numpy as np

from .epi_base_mixin import EpiBaseMixin

class EpiAuxMixin(EpiBaseMixin):
    # === Alt input

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
            mutations_list.append(input("Please indicate the mutation n°{elt2}: "))
        # call class to make instance
        cls.create_input_scheme(your_study, mutation_number, replicate_number, your_data,
                                replicate_list=replicate_list, mutations_list=mutations_list)
        input('Please add data to the file {},save and then press the Any key.'.format(your_data))
        cls.from_file(your_study, your_data).calculate().save(outfile)

    @classmethod
    def create_input_scheme(cls, your_study, mutation_number, replicate_number, outfile='scheme.xlsx',
                            replicate_list=None, mutations_list=None, mutant_list=None):
        ## Sanitise
        assert isinstance(your_study, str), 'Study can only be str value'
        mutation_number = int(mutation_number)
        replicate_number = int(replicate_number)
        assert isinstance(outfile, str), 'For now outfile and outfile2 can only be str value'
        for l in (replicate_list, mutations_list):
            if l:
                assert isinstance(l, list), 'replicate list and mutations_list can only be blank or lists of str'

        # This is really bad form. I modified the code before understanding that there were two programs in one.
        self = cls(your_study=your_study,
                   mutation_number=mutation_number,
                   replicate_number=replicate_number,
                   replicate_list=replicate_list,
                   mutations_list=mutations_list,
                   mutant_list=mutant_list)

        # these lines are very imortant to make a list of the mutations, a list of the replicates names and the mutants names. They will be used to make the table and combinations.

        Mutant_number = len(
            self.create_combination())  # the number of mutants if equal to the number of combinations
        box = ["X"] * Mutant_number * (
                    self.mutation_number + self.replicate_number)  # here we make a number of empty cases filled with "X"proportional to the number of mutants and mutations
        final_table1 = np.reshape(box, (Mutant_number, (self.mutation_number + self.replicate_number)))
        # here we make a matrix with the boxes above with the number of rows being equal to the number of mutants and the number of column being equal to the number of mutations + the number of replicates

        value_list = [[mutant[combinations] for combinations in mutant] for mutant in self.create_combination()]
        # this creates a list of the the combinations

        final_value_list = self.value_list_sorter(value_list)  # this is our sorted sign list !

        excel_table1 = pd.DataFrame(self.table_filler(final_table1, final_value_list),
                                        columns=self.mutations_list + self.replicate_list, index=self.mutant_list)
        writer = pd.ExcelWriter(outfile)
        excel_table1.to_excel(writer, sheet_name="sheet_name",
                              index=True)  # finally we write everything on a new excel, of which the name is given by the user
        writer.close()

    @classmethod
    def from_file(cls, your_study, infile):
        # No sanitisation... TODO
        # here we take the input given by the user in the excel tqble we previously generated
        table = pd.read_excel(infile)
        return cls.from_pandas(your_study, table)

    @classmethod
    def from_pandas(cls, your_study, table):
        # Determine
        # case where the first column is the index.
        if table.iloc[0,0] in ('-','+'):
            pass
        elif table.iloc[0,1] in ('-','+'):
            # the first column is meant to be the index
            table = table.set_index(table.columns[0])
        else:
            raise ValueError('This file is not formatted correctly')
        # figure out the mutation number.
        for mutation_number, v in enumerate(table.iloc[0]):
            if mutation_number == 0: # first may be name
                continue
            elif str(v) not in '-+':
                break
        replicate_number = len(table.iloc[0]) - mutation_number
        mutations_list = list(table)[:mutation_number]
        replicate_list = list(table)[mutation_number:]
        mutant_list = list(table.index)

        foundment = table.iloc[:,
                    :mutation_number]  # foundment is the matrix of all the signs and mutants we obtained above
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

    @property
    def theoretical_results(self):
        suppinfo = ["Combinations", "Experimental average", "Experimental standard deviation", "Thoretical average",
                    "Theoretical standard deviation", "Exp.avg - Theor.avg", "Epistasis type"]
        return pd.DataFrame(self.all_of_it, columns=self.mutations_list + suppinfo, index=self.comb_index)

    @property
    def experimental_results(self):
        return pd.DataFrame(self.foundment_values,
                                        columns=self.mutations_list + ["Average", "Standard deviation"],
                                        index=self.mutant_list)

    ##### Other methods
    def save(self, outfile='out.xlsx'):
        writer2 = pd.ExcelWriter(outfile)
        self.theoretical_results.to_excel(writer2, sheet_name="Theoretical results table", index=True)
        self.experimental_results.to_excel(writer2, sheet_name="Experimental results table", index=True)
        writer2.close()
        # and here are the lines to write the final excel table ! THe final file has two sheet, one with all the values and combinations, and the other with the experimental values only and the single mutants.

import numpy as np

class EpiBaseMixin:
    verbose = False

    def __init__(self, your_study:str,
                 mutation_number:int,
                 replicate_number:int,
                 replicate_list=None,
                 mutation_names=None,
                 mutant_list=None,
                 foundment_values=None,
                 data_array=None,
                 replicate_matrix=None,
                 median:bool=False):
        """
        :param your_study: Do you use selectivity or conversion values? Please answer with S (Selectivity) or C (Conversion)
        :param mutation_number: Please indicate your mutation number:
        :param replicate_number: Please indicate your replicate number (if some replicates are faulty, please fill the table with the average of the others otherwise the program might give unexpected results) :
        :param replicate_list (optinal): Replicate n°%s
        :param mutation_names (optinal): Please indicate the mutation n°%s: The list of the names of the mutations
        :param mutant_list (optinal): The list of variants (each with a set of mutations)
        :param foundment_values (optinal):  The +/- np array
        :param data_array (optinal):        All the np array
        :param replicate_matrix (optinal):  The number part of the np array

        Do note that in the code ``your_study` (S|C) has been replaced by the boolean ``self.wildtype_centred``.
        """
        # =============================== Parsing
        if your_study == 'C':
            self.wildtype_centred = True
        elif your_study == 'S':
            self.wildtype_centred = False
        else:
            ValueError('Study can only be C or S')
        # A mutation is a specific residue mutation. A mutant (=variant) is a combination of zero or more mutations.
        self.mutation_names, self.mutation_number = self.parse_mutations(mutation_names, mutation_number)
        self.mutant_names, self.mutant_number = self.parse_mutants(mutant_list, mutation_number)

        #
        if not mutant_list:
            self.mutant_list = [f"Mutant {elt4}" for elt4 in range(1, 2 ** mutation_number + 1)]
        else:
            self.mutant_list = mutant_list
        #
        if not replicate_list:
            self.replicate_list = [f"Replicate n°{elt3}" for elt3 in range(1, replicate_number + 1)]
        else:
            self.replicate_list = replicate_list
        self.replicate_number = replicate_number
        # not a loop because of copy.
        if isinstance(foundment_values, list):
            self.foundment_values = np.array(foundment_values)
        else:
            self.foundment_values = foundment_values
        if isinstance(replicate_matrix, list):
            self.replicate_matrix = np.array(replicate_matrix, dtype=np.float)
        else:
            self.replicate_matrix = replicate_matrix
        #
        if isinstance(data_array, list):  # technically this should be generated... TODO
            self.data_array = np.array(data_array)
        else:
            self.data_array = data_array
        # =============================== Preallocation
        self.mean_and_sd_dic = None
        self.mean_and_sd_array = None
        self.final_comb_table = None
        self.combs_only = None
        self.comb_index = None
        self.stats = []
        self.median = median

    def parse_mutations(self, mutation_names=None, mutation_number=None):
        """
        A mutation is a specific residue mutation. A variant is a combination of zero or more mutations.

        :param mutation_names:
        :param mutation_number:
        :return:
        """
        if not mutation_names and not mutation_number:
            raise ValueError('Please specify either mutation_names or mutation_number')
        elif not mutation_names:
            mutation_names = [f'M{i}' for i in range(1, mutation_number + 1)]
        elif not mutation_number:
            mutation_number = len(mutation_names)
        else:
            assert len(mutation_names) == mutation_number, f'There are {len(mutation_names)} names, but was expecting {mutation_number}'
        return mutation_names, mutation_number

    def parse_mutants(self, mutant_names=None, mutation_number=None):
        """
        A mutant is a combination of zero or more mutations.

        :param mutant_names:
        :param mutation_number:
        :return:
        """
        if not mutant_names and not mutation_number:
            raise ValueError('Please specify either mutant_names or mutation_number')
        elif not mutant_names:
            mutant_names = [f"Mutant {elt4}" for elt4 in range(1, 2 ** mutation_number + 1)]
        elif not mutation_number:
            mutation_number = len(mutant_names)
        else:
            assert len(mutant_names) == 2 ** mutation_number, f'There are {len(mutant_names)} names, but was expecting {2 ** mutation_number}'
        return mutant_names, 2 ** mutation_number

    @property
    def all_of_it(self):
        return np.array([[*stat['signage'], *[stat[key] for key in stat if key != 'signage']] for stat in self.stats])

    def calculate(self):
        raise NotImplementedError('This is an abstract method.')

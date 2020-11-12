import numpy as np

class EpiBaseMixin:
    verbose = False

    def __init__(self, your_study:str,
                 mutation_number:int,
                 replicate_number:int,
                 replicate_list=None,
                 mutations_list=None,
                 mutant_list=None,
                 foundment_values=None,
                 data_array=None,
                 replicate_matrix=None,
                 median=False):
        """

        :param your_study: Do you use selectivity or conversion values? Please answer with S (Selectivity) or C (Conversion):
        :param mutation_number: Please indicate your mutation number:
        :param replicate_number: Please indicate your replicate number (if some replicates are faulty, please fill the table with the average of the others otherwise the program might give unexpected results) :
        :param replicate_list (optinal): Replicate n°%s
        :param mutations_list (optinal): Please indicate the mutation n°%s: The list of the names of the mutations
        :param mutant_list (optinal): The list of variants (each with a set of mutations)
        :param foundment_values (optinal):  The +/- np array
        :param data_array (optinal):        All the np array
        :param replicate_matrix (optinal):  The number part of the np array
        """
        # =============================== Parsing
        if your_study in ('C', 'S'):
            self.your_study = your_study
        else:
            ValueError('Study can only be C or S')
        #
        if not mutations_list:
            self.mutations_list = [f'M{i}' for i in range(1, mutation_number + 1)]
        else:
            self.mutations_list = mutations_list
        self.mutation_number = mutation_number
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

    @property
    def all_of_it(self):
        return np.array([[*stat['signage'], *[stat[key] for key in stat if key != 'signage']] for stat in self.stats])

    def calculate(self):
        raise NotImplementedError('This is an abstract method.')

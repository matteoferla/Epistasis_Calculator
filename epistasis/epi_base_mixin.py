import numpy as np

class EpiBaseMixin:
    def __init__(self, your_study, mutation_number, replicate_number, replicate_list=None, mutations_list=None,
                 mutant_list=None, foundment_values=None, data_array=None, replicate_matrix=None):
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
            mutations_list = [f'M{i}' for i in range(1, mutation_number + 1)]
        if not replicate_list:
            replicate_list = [f"Replicate n°{elt3}" for elt3 in range(1, replicate_number + 1)]
        if not mutant_list:
            mutant_list = [f"Mutant {elt4}" for elt4 in range(1, 2 ** mutation_number + 1)]
        # not a loop because of copy.
        if isinstance(foundment_values, list):
            foundment_values = np.array(foundment_values)
        if isinstance(replicate_matrix, list):
            replicate_matrix = np.array(replicate_matrix)
        if isinstance(data_array, list):  # technically this should be generated... TODO
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
        self.mean_and_sd_dic = None
        self.mean_and_sd_array = None
        self.all_of_it = None
        self.final_comb_table = None
        self.combs_only = None
        self.comb_index = None

    def calculate(self):
        raise NotImplementedError('This is an abstract method.')

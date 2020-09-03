import argparse

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

__author__ = 'Paul. Made OO by MF'
__version__ = '1.3'
__date__ = '3 Sept 2020'

from epistasis import Epistatic

# ======================================================================================================================
if __name__ == "__main__":
    # your_study, mutation_number, replicate_number, your_data, outfile, replicate_list, mutations_list)
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("your_study",
                        help="Do you use selectivity or conversion values? Please answer with S (Selectivity) or C (Conversion)")
    parser.add_argument('-m',
                        dest="mutation_number",
                        type=int,
                        help="Please indicate your mutation number:")
    parser.add_argument("-r",
                        dest="replicate_number",
                        type=int,
                        help="Please indicate your replicate number (if some replicates are faulty, please fill the table with the average of the others otherwise the program might give unexpected results)")
    parser.add_argument('-d',
                        dest="your_data",
                        help="Please enter the name of your replicate table (don't forget the file extension !): (Put the name of the excel file you want your first table to be in)")
    parser.add_argument("outfile",
                        default='out.xlsx',
                        help="Please enter the name of the file you want your results in (don't forget the file extension !): (same here but for the excel you want your results in)")
    parser.add_argument('--version',
                        action='version',
                        version=__version__)
    args = parser.parse_args()
    if args.your_data:
        Epistatic.from_file(your_study=args.your_study,
                            infile=args.your_data)\
                 .calculate()\
                 .save(args.outfile)
    else:
        Epistatic.create_input_scheme(your_study=args.your_study,
                                      mutation_number=args.mutation_number,
                                      replicate_number=args.replicate_number,
                                      outfile=args.outfile)


# Epistasis
## Description
Script v1.0 written by Paul Lubrano. Slightly modified by myself (v1.1) and made app compatible (v1.2).
Original file can be found in `epistasis/old_files`.

* To run the webserver locally see run `python3 app.py`
* To use as a module `from epistasis import Epistatic`
* To run as a command line script, run `python3 epistasis_script.py` with appropriate arguments
* To run the original script, in python call `Epistatic.user_input()` (don't)

## Folders

There are two folders:

* `epistasis`, which contains the class `Epistatic`, which does the calculations
* `epiapp`, which is the Pyramid web app

## module

To install `pip install .`

Please see the docstrings in the methods for more info.

    from epistasis import Epistatic
    
    Epistatic(your_study='C'|'S', 
              mutation_number, 
              replicate_number, 
              replicate_list=None, 
              mutations_list=None, 
              mutant_list=None, 
              foundment_values=None, 
              data_array=None, 
              replicate_matrix=None)\
          .calculate()\
          .save('out.xls')

The original functionality of the script is retained as the class method `user_input` which will ask for input.
The altered usage has a way of creating the scheme thusly:
    
    Epistatic.create_input_scheme('C', '3', '3', 'test.xlsx')
    
Running from file and calculating and saving:

    Epistatic.from_file('C', 'raw.xlsx').calculate().save('wow.xlsx')

Running from panda table:

    Epistatic.from_pandas('C',table)
    
Running from values:

    Epistatic(your_study, mutation_number,replicate_number,replicate_list,mutations_list, mutant_list,foundment_values,data_array,replicate_matrix)

In addition to saving an Excel file, one can get the data as dataframes

    epi.save('wow.xlsx')
    epi.experimental_results #pandas dataframe
    epi.theoretical_results #pandas dataframe
       

The attributes are:

* your_study: Do you use selectivity or conversion values? Please answer with S (Selectivity) or C (Conversion):
* mutation_number: Please indicate your mutation number:
* replicate_number: Please indicate your replicate number (if some replicates are faulty, please fill the table with the average of the others otherwise the program might give unexpected results) :
* replicate_list (optinal): Replicate n°%s
* mutations_list (optinal): Please indicate the mutation n°%s:
* mutant_list (optinal):
* foundment_values (optinal):  The +/- np array
* data_array (optinal):        All the np array
* replicate_matrix (optinal):  The number part of the np array

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


To get some information during the run for debug purposes, set `Epistatic.verbose` to True.
              
## Power set

Mathematically, a combination is a set that contains all the subsets of size _k_ of _N_ items. 
Say `{Alice, Bob, Charlie}` has the following combinations of pairs: `{Alice, Bob}`, `{Alice, Charlie}`, `{Bob, Charlie}`.

Given N items, the set that contains none, combinations of 2, 3+ and all is called a power set.
Using the above example, the power set contains `{}`, `{Alice, Bob}`, `{Alice, Charlie}`, `{Bob, Charlie}`, `{Alice, Bob, Charlie}`.

However, for ease of speaking the words combination and power set are intermixed in the code.

## web app

To run the web app locally run `python3 app.py`.
              
## epistasis_script.py

It need to be run twice, no install.

    usage: epistasis_script.py [-h] [-m MUTATION_NUMBER] [-r REPLICATE_NUMBER]
                               [-d YOUR_DATA] [--version]
                               your_study outfile
                               usage: epistasis_script.py [-h] [-m MUTATION_NUMBER] [-r REPLICATE_NUMBER]
                           [-d YOUR_DATA] [--version]
                           your_study outfile

I have added some comments here and there to help you understand the code. I
hope it will be alright, sorry for the mess ! CRUCIAL HOW TO RUN : 1) First
run the programm until the line with "checkpoint table 1" (around line 100) 3)
complete carefully what the programm asks, this will influence a lot what the
output is 2) you will get an excel in which you have the different mutants, in
this excel put the experimental replicates values instead of the "X" 3) then
run the rest of the program, you will get a second excel with the results !
MF. Modded so it uses argparse.
    
positional arguments:

      your_study           Do you use selectivity or conversion values? Please
                           answer with S (Selectivity) or C (Conversion)
      outfile              Please enter the name of the file you want your results
                           in (don't forget the file extension !): (same here but
                           for the excel you want your results in)
    
optional arguments:

      -h, --help           show this help message and exit
      -m MUTATION_NUMBER   Please indicate your mutation number:
      -r REPLICATE_NUMBER  Please indicate your replicate number (if some
                           replicates are faulty, please fill the table with the
                           average of the others otherwise the program might give
                           unexpected results)
      -d YOUR_DATA         Please enter the name of your replicate table (don't
                           forget the file extension !): (Put the name of the
                           excel file you want your first table to be in)
      --version            show program's version number and exit
      
      
## To Do

* There are a few todos in the code.
* `/Users/matteo/Coding/Epistasis_Calculator/epistasis/__init__.py:221`: FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison
  if np.any(foundment_values == '+'):
* saving a uuid named file can be avoided by using streams

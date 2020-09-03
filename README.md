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
          
Alternatively use:

* `Epistatic.from_files`
* `Epistatic.from_pandas`
              
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
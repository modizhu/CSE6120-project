# CSE6120-project
CSE 6140 project, Fall 2022

## Team Members: 
Mayank Vanani, Vivek Bokkisa, Sanshrit Singhai, Modi Zhu 

_Note: All team members contributed equally_

## Directory Structure
- CSE6120-project
  - Code
    - main.py
    - BnB.py
    - Approx.py
    - LS1.py
    - LS2.py
  - Output
    - _<contains .sol files and .trace files for the solutions for each algorithm>_
  - DATA
    - _<contains .graph files which would be input for the algorithm>_
  - CSE6140_2022_project_instruction.pdf
  - README.md

## CLI Instructions
**Input Arguments:** 
  - inst _<path of .graph file for which the algorithm needs to be run>_
  - alg _<[BnB|Approx|LS1|LS2]>_
  - time _<cutoff time (in seconds)>_
  - seed _<non zero arbitrary integer>_
  
**How to run CLI and few examples**: 
Open the terminal at "CSE6120-project" directory level.
  - To run particular algorithm for single graph file
  > $ python Code/main.py -inst DATA/jazz.graph -alg LS1 -time 60 -seed 145
  
  - To run an algorithm on more than one graph
  > $ python Code/main.py -inst DATA/jazz.graph DATA/karate.graph -alg LS2 -time 600 -seed 1405
  
  - To run an algorithm on all graphs
  > $ python Code/main.py -inst DATA/* -alg LS2 -time 600 -seed 1405
  
  - To run an algorithm with multiple seed values
  > $ python Code/main.py -inst DATA/star2.graph -alg Approx -time 600 -seed 1 340 1303 2004 5001
  
  - To run all algorithms with multiple seed values
  > $ python Code/main.py -inst DATA/* -alg BnB -time 600 -seed 1 340 1303 2004 5001
  

## Algorithms Implemented
* Branch and Bound
* Approximation
* Local Search 1 - Fast VC
* Local Search 2 - Simmulated Annealing
  
More information can be found on the white paper and as _docstrings_ of respective .py files inside the 'Code' Directory.



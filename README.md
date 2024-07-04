# Report for Assignment 1

## Project chosen

Name: gdsfactory\
URL: https://github.com/gdsfactory/gdsfactory \
Number of lines of code and the tool used to count it:  45356, lizard\
Programming language: Python

## Coverage measurement
### Coverage.py

I then cloned the original repository:\
git clone https://github.com/gdsfactory/gdsfactory.git\
Then I changed the directory to /gdsfactory.\
cd gdsfactory\
Then I installed all the required dependencies and modules.\
pip install .\
pip install pytest_regressions\
pip install jsondiff\
pip install jsonschema\
I used coverage.py to measure coverage after installing it and its requirements.\
Finally, I ran coverage.py.\
coverage run -m pytest -s\
coverage report\
coverage html


As the coverage report is long, I only included the overall coverage result as well as the coverage result of the files that contain the functions for which I will improve the branch coverage.
[coverage pictures]([https://github.com/keylad/gdsfactory/tree/main/pictures/coverage](https://github.com/keylad/gdsfactory/blob/main/pictures/coverage/old/Screenshot%202024-07-03%20at%2018.49.22.png))
[coverage pictures](https://github.com/keylad/gdsfactory/blob/main/pictures/coverage/old/Screenshot%202024-07-03%20at%2018.50.05.png)
[coverage pictures](https://github.com/keylad/gdsfactory/blob/main/pictures/coverage/old/Screenshot%202024-07-03%20at%2018.50.14.png)

## Coverage improvement

### def parse_coordinate
Identifying the requirements to be tested:
[problem areas](https://github.com/keylad/gdsfactory/blob/main/pictures/Screenshot%202024-07-03%20at%2019.02.05.png)

Here you can see the new test created for the parse_coordinate function since the original tests do not directly cover the function. The original coverage comes from other functions that use the parse_coordinate function. 
[new tests](https://github.com/keylad/gdsfactory/blob/main/pictures/Screenshot%202024-07-03%20at%2018.58.29.png)

This is the original coverage of the function:
[original coverage](https://github.com/keylad/gdsfactory/blob/main/pictures/coverage/old/Screenshot%202024-07-03%20at%2018.49.44.png)

This is the new coverage of the function:
[new coverage](https://github.com/keylad/gdsfactory/blob/main/pictures/coverage/new/Screenshot%202024-07-03%20at%2018.51.07.png)

The coverage is upped from 56% to 100% because before the introduction of this new test only the body of the elif branch was covered by tests and the other branches were not. This new test allows for the bodies of all the branches to be covered as it tests every possible case, including error cases.


### def get_min_sbend_size
Identifying the requirments to be tested:
[problem areas](https://github.com/keylad/gdsfactory/blob/main/pictures/Screenshot%202024-07-03%20at%2019.02.42.png)

Below is the new test created for the get_min_sbend_size function since the original tests also do not directly cover the fuction for the same reasons that were mentioned before.
[new tests](https://github.com/keylad/gdsfactory/blob/main/pictures/Screenshot%202024-07-03%20at%2018.58.18.png)

This is the original coverage of the function:
[original coverage](https://github.com/keylad/gdsfactory/blob/main/pictures/coverage/old/Screenshot%202024-07-03%20at%2018.50.37.png) 

This is the new coverage of the function:
[new coverage](https://github.com/keylad/gdsfactory/blob/main/pictures/coverage/new/Screenshot%202024-07-03%20at%2018.51.34.png)

The coverage is upped from 74% to 92%. It wasn't upped to 100% because the function also contains a for-loop that gives off a warning:
[for loop](https://github.com/keylad/gdsfactory/blob/main/pictures/Screenshot%202024-07-04%20at%2011.58.36.png)
Other than that the new test is applied to all prossible cases.

### Overall

<Provide a screenshot of the old coverage results by running an existing tool (the same as you already showed above)>

<Provide a screenshot of the new coverage results by running the existing tool using all test modifications made by the group>

## Statement of individual contributions

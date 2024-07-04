# Report for Assignment 1

## Project chosen

Name: gdsfactory\
URL: https://github.com/gdsfactory/gdsfactory \
Number of lines of code and the tool used to count it:  45356\
Programming language: Python

## Coverage measurement
### Coverage.py

We used coverage.py to measure coverage after installing it and its requirements.\
We then cloned the original repository.\
git clone https://github.com/gdsfactory/gdsfactory.git\
Then we changed the directory to /gdsfactory.\
cd gdsfactory\
Then we installed all the required dependencies and modules.\
pip install .\
pip install pytest_regressions\
pip install jsondiff\
pip install jsonschema\
Finally, we ran coverage.py.\
coverage run -m pytest -s\
coverage report\
coverage html

[coverage pictures](https://github.com/keylad/gdsfactory/tree/main/pictures/coverage)

### Your own coverage tool


#### Keyla Domingos Lopes - kdo208
def _parse_coordinate
[link](https://github.com/keylad/gdsfactory/blob/main/pictures/parse_coordinate/Screenshot%202024-06-27%20at%2017.20.24.png)
[link](https://github.com/keylad/gdsfactory/blob/main/pictures/parse_coordinate/Screenshot%202024-06-27%20at%2017.20.31.png)

Using this example input, we get the following result:
[link](https://github.com/keylad/gdsfactory/blob/main/pictures/parse_coordinate/Screenshot%202024-06-27%20at%2017.20.38.png)

def get_min_sbend_size
[link](https://github.com/keylad/gdsfactory/blob/main/pictures/get_min_bend_size/Screenshot%202024-06-27%20at%2017.20.50.png)
[link](https://github.com/keylad/gdsfactory/blob/main/pictures/get_min_bend_size/Screenshot%202024-06-27%20at%2017.20.58.png)
[link](https://github.com/keylad/gdsfactory/blob/main/pictures/get_min_bend_size/Screenshot%202024-06-27%20at%2017.21.04.png)
Using this example we get, the following results:
[link](https://github.com/keylad/gdsfactory/blob/main/pictures/get_min_bend_size/Screenshot%202024-06-27%20at%2017.21.11.png)


## Coverage improvement

test_parse_coordinate.py

The tests do not directly cover the def _parse_coordinate, which is why we created an entirely new test that exclusively covers the function and its branches.
[link](https://github.com/keylad/gdsfactory/blob/main/pictures/parse_coordinate/test/Screenshot%202024-06-27%20at%2017.23.11.png)

The original branch coverage of the function was as follows:
[link](https://github.com/keylad/gdsfactory/tree/main/pictures/parse_coordinate/test/old%20coverage)
The new branch coverage of the function after the new test is as follows:
[link](https://github.com/keylad/gdsfactory/tree/main/pictures/new%20coverage)

The coverage is improved because before the introduction of this new test only the body of the elif branch was covered by tests and the other branches were not. This new test allows for the bodies of all the branches to be covered as it tests every possible case.


test_bend_s.py
The tests do not directly cover the def get_min_sbend_size, which is why we created an entirely new test that exclusively covers the function and its branches.
[link](https://github.com/keylad/gdsfactory/tree/main/pictures/get_min_bend_size/test)

The original branch coverage of the function was as follows:
[link](https://github.com/keylad/gdsfactory/tree/main/pictures/get_min_bend_size/old%20coverage)

The new branch coverage of the function after the new test is as follows:
[link](https://github.com/keylad/gdsfactory/tree/main/pictures/get_min_bend_size/new%20coverage)

The new test cases cover all the branches and conditions to make sure that each path, exception handling and different input scenarios, is executed at least once to improve the overall branch coverage. The for loop, however, is not covered by these test cases.

### Overall

<Provide a screenshot of the old coverage results by running an existing tool (the same as you already showed above)>

<Provide a screenshot of the new coverage results by running the existing tool using all test modifications made by the group>

## Statement of individual contributions

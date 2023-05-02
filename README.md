# witsmcq
For providing feedback to students using the Wits MCQ card system


## Overview

This program can be run to produce individual feedback for each student for an
MCQ test done using the Wits physical card system.

It produces
-- a PDF which contains one page per student showing for each student
   whether they got a question right or wrong
-- an Excel spreadsheet showing the marks for the students (you should have this
   already but you can use discrepancies to check for anomalies or problems)
   

## To install

Open up the Terminal

Download the code

`git clone https://github.com/shaze/witsmcq`

A directory with the code will be created.

You need Python 3.7 or above running, and the following packages
* pandas
* openpyxl

You can install the packages by typing

`pip3 install pandas openpyxl`


## Running the code

You need to have two files
* The file with the individual students' responses. You can ask Wits ICT for this -- ask for the  `dat` file
* An Excel spreadsheet with the answers for the individual questions. The spreadsheet should have two columns: _Question Number_ and _Answer_ spelt exactly like this.

In the simplest case, you can run by jusy saying (changing the file names appropriately)

`./witsmcq.py  responses.dat answers.xlsx`

The program will create a file _results.pdf_ with one page per student and _results.xlsx_ with the mark list.

Here's a slighly more complex example. In this case note that the one file name has spaces in it and so we have to put a backslash in before each space to that the computer knows that the space is part of the file name and not separating different file names. Also in this example, we explicitly name the output files _ass3-mcq.pdf_ and _ass3-mcq.xlsx`

```
witsmcq.py Downloads/ELEN2021-20230405.dat Documents/Assess\ 3\ Answers.xlsx   --output-name ass3-mcq
```

## Other options


### Heading at the top of each page

By default, each page in the PDF file starts with "Test Feedback". To change this use `--heading`

```
witsmcq.py --heading "Quiz A"  Answers.xlsx   --output-name ass3-mcq
```


### Number of rows and columns

By default the feedback has 25 rows per column and enough columns to  fit all your answers in. If you want to change the number of rows use the `-num-rows` option.



```
witsmcq.py --heading "Quiz A"  --num-rows 2  Answers.xlsx   --output-name ass3-mcq
witsmcq.py  --num-rows 3  --output-name ass3-mcq  Answers.xlsx
witsmcq.py  --num-rows 5 witsmcq.py   --output-name ass3-mcq     
```


```

import streamlit as st
import pandas as pd
import numpy as np
from simpleai.search import CspProblem, backtrack

st.title('Crypto Puzzle Solver')

input1 = st.text_input('First Input', '')
input2 = st.text_input('Second Input', '')
outputword= st.text_input('Output', '')
result = st.button("Solve")

templist = [] # Temporary List to fill with the all the letter of the word to convert to variables tuple later

domains = {
    
} #creating domains dict to fill later

if result:
     
    templist.append(input1[0]) #adding first letter to temporary variables list
    domains.update({input1[0]: list(range(1,10))}) #ensuring first digit of word has to be 1 or more
    if input1[0] != input2[0]: #checking if first letter of word is already added to ensure no duplicates in domains/variables
        domains.update({input2[0]: list(range(1,10))})
        templist.append(input2[0])
    if input1[0] or input2[0] != outputword[0] : #checking if first letter of word is already added to ensure no duplicates in domains/variables
        domains.update({outputword[0]: list(range(1,10))})
        templist.append(outputword[0])


    for i in input1: #adding every letter of input1 to variables/domains
        if not i in templist: #checking if letter already exists in variables/domains
            templist.append(i)
            domains.update({i: list(range(0,10))})

    for i in input2: #adding every letter of input2 to variables/domains
        if not i in templist: #checking if letter already exists in variables/domains
            templist.append(i)
            domains.update({i: list(range(0,10))})

    for i in outputword: #adding every letter of outputword to variables/domains
        if not i in templist: #checking if letter already exists in variables/domains
            templist.append(i)
            domains.update({i: list(range(0,10))})


    variables = tuple(templist) # converting temporary variable list to tuple for use in solution


    def constraint_unique(variables, values):
        return len(values) == len(set(values))  # remove repeated values and count

    def constraint_add(variables, values):
        def sum_word(word): #method to fill the addition methods dynamically based on the words inputted by the user
            if len(word) == 0: #base case for when the word is null
                return ""
            else:
                return str(values[variables.index(word[0])]) + sum_word(word[1:]) #filling the equation to be solved

        factor1 = int(sum_word(input1))
        factor2 = int(sum_word(input2))
        result = int(sum_word(outputword))
        return (factor1 + factor2) == result

    constraints = [
        (variables, constraint_unique),
        (variables, constraint_add),
    ]

    problem = CspProblem(variables, domains, constraints) #setting up problem to be solved

    output = backtrack(problem) #solving problem
    print('\nSolutions:', output)

    #setting placeholders to process output
    answer1 = ""
    answer2 = ""
    answer3 = ""

    for i in input1: #processing output of first input
        answer1 = answer1 + str(output.get(input1[input1.index(i)]))
    
    for i in input2: #processing output of second input
        answer2 = answer2 + str(output.get(input2[input2.index(i)]))
    
    for i in outputword: #processing output of third input
        answer3 = answer3 + str(output.get(outputword[outputword.index(i)]))


    st.write(input1 + " + " + input2 + " = " + outputword) #display input
    st.write(answer1 + " + " + answer2 + " = " + answer3) #display processed output

    for x, y in output.items():
        st.write(str(x).upper() + " is equal to value " + str(y))

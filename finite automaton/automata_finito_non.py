#!/usr/bin/python3

# project: universal simulator for FA
# date:
# Authors: Laura Quispe, Jarlinton Moreno
# professor: Diego Amancio
# University: Universidade de S\xc3o Paulo

import sys


def mapper_transitions(tran, map_transition):
    if map_transition.get(tran[0], -1) == -1:
        map_transition[tran[0]] = {}
    if map_transition[tran[0]].get(tran[1], -1) == -1:
        map_transition[tran[0]][tran[1]] = []
    map_transition[tran[0]][tran[1]] = map_transition[tran[0]][tran[1]] + [tran[2]]


def process_input_file(file_path):
    '''
        This method process the file from the user..
    '''
    # open the file and save into a variable.
    with open(file_path, 'r') as text:
        file_to_process = text.readlines()
        text.close()  #close_file_processed

    # remove \n from the original file.
    clean_file = [lines.strip() for lines in file_to_process]

    # get the values from the lines.
    num_states = int(clean_file[0])

    # validate the number of states
    if 0 < num_states <= 10:
        # make the states q0 to qn-1
        states = [str(s) for s in range(0,num_states)]

    info_simbols = clean_file[1].strip().split(' ')
    num_simbols = int(info_simbols[0])

    if 0 < num_simbols <= 10:
        terminal_simbols = info_simbols[1:num_simbols+1]

    num_initial_states = int(clean_file[2])

    if 0 < num_initial_states <= 10:
        # define for AFD only at this point
        # we suposse that only have one initial state
        initial_state = states[0]

    info_final_states = clean_file[3].strip().split(' ')

    num_final_states = int(info_final_states[0])

    if 0 < num_final_states <= 10:
        final_states = info_final_states[1:num_final_states+1]


    # calculate the transitions between states
    num_of_transitions = int(clean_file[4])
    map_transition = {}
    new_index = 0
    for t in range(num_of_transitions):
        tran = clean_file[5+t].split()
        mapper_transitions(tran, map_transition)
        new_index += 1

    num_of_strings = int(clean_file[5 + new_index])

    # get the total amount of string for test..
    for st in range(1, num_of_strings+1):
        string_to_test = clean_file[5+new_index+st]
        # call to the evalute cadeia
        print("Cadeia %s" % string_to_test)
        print("Cadeia %s %s" % (string_to_test, evaluate_automatus(map_transition, initial_state, final_states, string_to_test)))


def evaluate_automatus(map_transition, initial_state, final_states, string_to_test):
    # begin from the initial state
    actual_states = [initial_state]

    if string_to_test == "-":
        string_to_test = string_to_test
    else:
        string_to_test = "-".join(string_to_test)
        string_to_test = "-" + string_to_test + "-"
    # verify every character into the string to test.
    for ch in string_to_test:
        new_states = []
        for actual_state in actual_states:
            if map_transition.get(actual_state, -1) != -1 and map_transition[actual_state].get(ch, -1) != -1:
                for state in map_transition[actual_state][ch]:
                    new_states.append(state)
                    print("(%s, %s) -> %s" % (actual_state, ch, state))
            else:
                if ch == "-":
                    new_states = actual_states
        actual_states = new_states
        # print(actual_states, new_states, final_states,ch)
    # we reach a final state??
    for actual_state in actual_states:
        if actual_state in final_states:
            return "Aceita"

    return "Rejeita"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        process_input_file(path)
    else:
        file_name = 'afnd_1.txt'
        process_input_file(file_name)
        # print("Insert the name for the file, to be process.")
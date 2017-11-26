import sys


class ReaderAutomaton:
    def __init__(self):
        self.states = []
        self.alphabet_input = []
        self.alphabet_stack = []
        self.final_states = []
        self.transitions = []
        self.test_cases = []

    def __call__(self, filename):
        file = open(filename, 'r')
        lines = file.readlines()
        num_states = int(lines[0])
        if 0 < num_states <= 10:
            self.states = [str(s) for s in range(0, num_states)]
        info_alphabet_input = lines[1].strip().split(' ')
        num_alphabet_input = int(info_alphabet_input[0])
        if 0 < num_alphabet_input <= 10:
            self.alphabet_input = info_alphabet_input[1:num_alphabet_input+1] + ["-"]
        info_alphabet_stack = lines[2].strip().split(' ')
        num_alphabet_stack = int(info_alphabet_stack[0])
        if 0 < num_alphabet_stack <= 10:
            self.alphabet_stack = info_alphabet_stack[1:num_alphabet_stack]
        info_final_states = lines[3].strip().split(' ')
        num_final_states = int(info_final_states[0])
        if 0 < num_final_states <= 10:
            self.final_states = info_final_states[1:num_final_states+1]
        num_transitions = int(lines[4])
        # 0 a Z 0 AZ
        for i in range(num_transitions):
            self.transitions.append(lines[5 + i].split())

        num_test_cases = int(lines[5+num_transitions])
        for i in range(1, num_test_cases+1):
            self.test_cases.append(lines[5+num_transitions+i].strip())


class StackAutomaton(object):
    def __init__(self, states, alphabet_input, alphabet_stack, final_states, transitions):
        self.states = states
        self.alphabet_input = alphabet_input
        self.alphabet_stack = alphabet_stack
        self.final_states = final_states
        self.transitions = transitions
        self.stack = []
        self.map_transition = dict()

    def __call__(self):
        self.build()

    def build(self):
        for info_transition in self.transitions:
            print info_transition
            p = info_transition[0]
            x = info_transition[1]
            Z = info_transition[2]
            q = info_transition[3]
            o = info_transition[4]
            self.mapper_transition(p, x, Z, q, o)

    def mapper_transition(self, p, x, Z, q, o):
        if self.map_transition.get(p, -1) == -1:
            self.map_transition[p] = {}
        if self.map_transition[p].get(x, -1) == -1:
            self.map_transition[p][x] = {}
        if self.map_transition[p][x].get(Z, -1) == -1:
            self.map_transition[p][x][Z] = {}
        self.map_transition[p][x][Z] = [(q, o)]

    def evaluate(self, string):
        self.stack = [self.alphabet_stack[0]]
        current_states = {self.states[0]}
        string = string + "-"
        idx = 0
        while idx < len(string):
            i = string[idx]
            new_states = set()
            for state in current_states:
                # Desempilha
                if len(self.stack) > 0:
                    top = self.stack.pop()
                else:
                    # Nao pode desempilhar e ainda tem alfabeto para leer.
                    return "reject"
                if self.map_transition.get(state, -1) != -1 and \
                   self.map_transition[state].get(i, -1) != -1 and \
                   self.map_transition[state][i].get(top, -1) != -1:
                    for novo_state, novo_stack in self.map_transition[state][i][top]:
                        new_states.update([novo_state])
                        if novo_stack != "-":
                            # Empilha
                            self.stack.extend(novo_stack[::-1])
                        # se substitution da pilha is "-" so pop
                        idx += 1
                        print "(%s, %s, %s) -> (%s, %s)" % (state, i, top, novo_state, novo_stack[::-1])
                elif self.map_transition.get(state, -1) != -1 and \
                        self.map_transition[state].get("-", -1) != -1 and \
                        self.map_transition[state]["-"].get(top, -1) != -1:
                    for novo_state, novo_stack in self.map_transition[state]["-"][top]:
                        new_states.update([novo_state])
                        if novo_stack != "-":
                            # Empilha
                            self.stack.extend(novo_stack[::-1])
                        # se substitution da pilha is "-" so pop
                        print "(%s, %s, %s) -> (%s, %s)" % (state, "-", top, novo_state, novo_stack[::-1])
                else:
                    print "(%s, %s, %s) -> (?, %s)" % (state, i, top, top)
                    self.stack.extend(top)
                    return "accept" if len(self.stack) == 0 and current_states.intersection(self.final_states) else "reject"
            current_states = new_states
        return "accept" if len(self.stack) == 0 and current_states.intersection(self.final_states) else "reject"


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
    else:
        file_name = 'apnd_1.txt'
    reader = ReaderAutomaton()
    reader(file_name)
    stack_automaton = StackAutomaton(reader.states, reader.alphabet_input, reader.alphabet_stack, reader.final_states, reader.transitions)
    stack_automaton()
    for test_case in reader.test_cases:
        print("Cadeia:" + test_case)
        print("Cadeia: %s = %s" % (test_case, stack_automaton.evaluate(test_case)))
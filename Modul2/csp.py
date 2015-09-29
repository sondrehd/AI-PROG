__author__ = 'paulpm, sondredyvik'
from variable import Variable
from constraint import Constraint
import state


class CSP:

    def __init__(self):
        self.variables = []
        self.constraints = {}
        self.queue = []

    ##Not used yet

    def makefunc(self, var_names, expression, environment=globals()):
        args = ""
        for n in var_names:
            args = args + ',' + n
        return eval('(lambda ' + args[1:] + ': ' + expression + ')', environment)

    def revise(self, focal_variable, constraint):
        revised = False
        for focal_color in focal_variable.domain:
            satisfies_constraint = False
            for other_color in constraint.vertices[1].domain:
                if constraint.check_if_satisfies(focal_color, other_color):
                    satisfies_constraint = True
                    break

            if satisfies_constraint is False:
                focal_variable.domain.pop(focal_color)
                revised = True

        return revised

    def domain_filter(self):
        while len(self.queue) > 0:
            focal_variable, other_variable = self.queue.pop()
            if self.revise(focal_variable, other_variable):
                self.add_all_tuples_in_which_variable_occurs(focal_variable, other_variable)


    def add_all_tuples_in_which_variable_occurs(self, focal_state, focal_variable, focal_constraint):
        constraints_containing_variable = []
        for key, list_of_values in self.constraints.iteritems():
                    for constraint_in_list_of_values in list_of_values:
                        if focal_constraint is None:
                            if constraint_in_list_of_values.contains_variable(focal_variable):
                                constraints_containing_variable.append(constraint_in_list_of_values)
                        elif constraint_in_list_of_values.contains_variable(focal_variable) and not constraint_in_list_of_values == focal_constraint:
                            constraints_containing_variable.append(constraint_in_list_of_values)
                    for focal_constraint in constraints_containing_variable:
                        self.queue.append((focal_state, focal_constraint.get_other(focal_variable), focal_constraint))


    def rerun(self, state, var):
        self.add_all_tuples_in_which_variable_occurs(state, var, None)
        self.domain_filter()

    def initialize_queue(self):
        for variable in self.variables:
            for focal_constraint in self.constraints[variable]:
                self.queue.append((variable, focal_constraint))




colors = ['red', 'green', 'blue', 'yellow', 'black', 'pink']


def create_csp(graph_file, domain_size):
    csp = CSP()
    f = open(graph_file, 'r')
    number_of_vertices, number_of_edges = [int(x) for x in f.readline().strip().split(' ')]

    for i in range(number_of_vertices):
        index, x, y = [i for i in f.readline().strip().split(' ')]
        vertex = Variable(int(index), float(x), float(y))
        csp.variables.append(vertex)
        csp.constraints[vertex] = []

    for j in range(number_of_edges):
        i1, i2 = [int(i) for i in f.readline().strip().split(' ')]
        this_vertex = csp.variables[i1]
        other_vertex = csp.variables[i2]
        csp.constraints[this_vertex].append(Constraint([this_vertex, other_vertex]))
        csp.constraints[other_vertex].append(Constraint([other_vertex, this_vertex]))

    for k in csp.variables:
        k.domain = [colors[x] for x in range(domain_size)]

    f.close()
    return csp


def main():
    csp = create_csp("graph-color-1.txt", len(colors))

    csp.initialize_queue()
    csp.domain_filter()

    #csp.rerun(searchstate, csp.variables[0])


def generate_initial_searchstate(csp):
    return state.State(csp.domains)



if __name__ == "__main__":
    main()
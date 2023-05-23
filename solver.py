import sys
from typing import List , Tuple
from copy import deepcopy
from itertools import combinations
import random

NUM_DIGITS = 5

def print_clauses(clauses) -> None:
    for clause in clauses:
        print("clause: ", end=" ")
        for literal in clause:
            print(f"literal{literal}", end=" ")
        print()

class Literal:
    def __init__(self, name: str, sign) -> None:
        self.name = name
        self.sign = sign

    def __str__(self) -> str:
        return self.name if self.sign else f"-{self.name}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Literal):
            return False
        return self.name == other.name and self.sign == other.sign

    @classmethod
    def opposite(cls, literal1, literal2) -> bool:
        if not isinstance(literal1, Literal) or not isinstance(literal2, Literal):
            print(f"literal1: {literal1} , literal2: {literal2}")
            print(f"literal1 type: {type(literal1)} , literal2 type: {type(literal2)}")
            raise TypeError("literal1 and literal2 must be Literal objects")
        return literal1.name == literal2.name and literal1.sign != literal2.sign


class SatSolver:
    def __init__(self, clauses=None, literal_values=None) -> None:
        self.assignment = {}
        self.clauses = clauses or []
        self.literal_values = literal_values or []
        self.current_literal_index = 0 
    def read_input(self) -> None:
        print("enter your clauses:")
        self.clauses = []
        while True:
            clause_input = input()
            if not clause_input:
                break
            clause = []
            literals_input = clause_input.split()
            for literal_str in literals_input:
                if literal_str.startswith("-"):
                    literal = Literal(literal_str[1:], False)
                else:
                    literal = Literal(literal_str, True)
                clause.append(literal)
                if literal.name not in self.literal_values:
                    self.literal_values.append(literal.name)
            self.clauses.append(clause)

    def _print_clauses(self, clauses) -> None:
        for clause in clauses:
            print("clause: ", end=" ")
            for literal in clause:
                print(f"literal{literal}", end=" ")
            print()

    def unit_propagation(self, formula: List) -> List:
        while True :
            found = False
            literal:Literal = None
            for clause in formula:
                if len(clause) == 1:
                    found = True
                    # print(f"clause: {clause} , len(clause) = {len(clause)} , type(clause) = {type(clause)} , clause[0] = {clause[0]}")
                    literal = clause[0]
                    print(f"unit propagation: {literal} , literal.sign = {literal.sign}")
                    self.assignment[str(literal.name)] = literal.sign
                    # print(f"assignment: {str(literal.name)}")
                    # print(f"literal : {literal}")
                    break
            if literal : 
                formula = self._delete_clauses_with_literal(formula, literal)
                formula = self._delete_literal_from_clauses(formula, literal)
            if not found:
                break
        return formula

    def _delete_clauses_with_literal(self, formula, literal) -> List:
        # print(f"deleting clauses with literal {literal}")
        new_formula = []
        for clause in formula:
            found = any(l == literal for l in clause)
            if not found:
                new_formula.append(clause)
        return new_formula

    def _delete_literal_from_clauses(self, formula, literal) -> List:
        new_formula = [
            [l for l in clause if not Literal.opposite(l, literal)]
            for clause in formula
        ]
        return new_formula

    def pure_literal_elimination(self, formula) -> bool:
        while pure_literal := self._get_pure_literal(formula):
            print(f"pure literal: {pure_literal}")
            self.assignment[pure_literal.name] = pure_literal.sign
            if pure_literal.sign and pure_literal.name in ["00" ,"01"]:
                print(f"setting pure literal {pure_literal} to true")
            formula = self._delete_clauses_with_literal(formula, pure_literal)
        return formula

    def _get_pure_literal(self, formula) -> Literal:
        if not formula:
            return None

        for literal in self.literal_values:
            unique = True
            found = False
            sign = None
            for clause in formula:
                for l in clause:
                    if l.name == literal:
                        if sign is None:
                            sign = l.sign
                            found = True
                        elif sign != l.sign:
                            unique = False
                            break
            if unique and found:
                return Literal(literal, sign)

        return None

    def dpll_solve(self, formula, i=0, assignment=None) -> Tuple[bool, dict]:
        
        if assignment is None:
            assignment = {}
        if not formula:
            return True, self.assignment
        # print("step")
        # self._print_clauses(formula)
        print(f"length before unit propagation: {len(formula)}")
        formula = self.unit_propagation(formula)
        print(f"length after unit propagation: {len(formula)}")
        print(f"After unit propagation:\n ")
        # self._print_clauses(formula)
        if [] in formula:
            return False, None
        print(f"assignment: {self.assignment}")
        formula = self.pure_literal_elimination(formula)
        print(f"After pure literal elimination:\n")
        # self._print_clauses(formula)
        print(f"assignment: {self.assignment}")

        if not formula:
            return True, self.assignment 

        if [] in formula:
            return False, None

        if self.current_literal_index >= len(self.literal_values):
            return False, None

        choice = self.literal_values[i]

        if choice in self.assignment:
            return self.dpll_solve(formula , i+1)

        print(f"trying choice {choice} , true")
        assignment_copy = deepcopy(self.assignment)
        satisfied, answer = self.dpll_solve(formula + [[Literal(choice , True)]] , i+1)

        if satisfied:
            # print("here")
            return True, answer

        self.assignment = deepcopy(assignment_copy)
        # else : 
        #     print(f"choice {choice} {True} failed ")

        print(f"trying choice {choice} , false")

        satisfied, answer = self.dpll_solve(formula + [[Literal(choice , False)]],i+1)
        if satisfied:
            # print("there")
            return True, answer

        # self.assignment = deepcopy(assignment_copy)
        return False, None

    def solve(self, formula):
        satisfied, assignment = self.dpll_solve(formula)
        if not satisfied:
            return None
        for literal in self.literal_values:
            if literal not in assignment:
                assignment[literal] = False
                # assignment[literal] = random.choice([True, False])
        return assignment


# print(clauses)


# solver = SatSolver()
# solver.read_input()
# answer = solver.solve(solver.clauses)
# print(answer)

# OR_clauses = []
# for i in range(5):
#     clause = []
#     for j in range(1,10):
#         clause.append(Literal(f'{i}{j}' , True))
#     OR_clauses.append(clause)

# # for clause in OR_clauses:
# #     for literal in clause:
# #         print(literal , end=' ')
# #     print()

# AND_caluses = convert_OR_clauses_to_AND_clauses(OR_clauses)
# for clause in AND_caluses:
#     for literal in clause:
#         print(literal , end=' ')
#     print()



class NumberMindSolver:
    def __init__(self) -> None:
        self.variables =[ [f"{i}{j}" for j in range(10)] for i in range(NUM_DIGITS) ] 
        self.guesses = [
            # ("12" , 0) , 
            # ("15" , 0 ), 
            
            
            ("90342", 2),
            ("70794", 0),
            ("39458", 2),
            ("34109", 1),
            ("51545", 2), 
        ]
        self.clauses = []

    def add_starting_clauses(self):
        # # Adding clauses for each digit for each number from 1 to 9
        # OR_clauses = []
        # for digit in range(5):
        #     clause = [Literal(f"{digit}{number}", True) for number in range(1, 10)]
        #     OR_clauses.append(clause)
    
        # # Converting OR clauses to AND clause to be CNF clauses
        # AND_clauses = self.convert_OR_clauses_to_AND_clauses(OR_clauses)
        
        # for clause in AND_clauses:
        #     for literal in clause:
        #         print(literal , end=' ')
        #     print()
        
        
        for digit in range(NUM_DIGITS):
            self.clauses.extend(self.exactly_one(self.variables[digit]))

    def exactly_one(self, variables) -> List[Tuple[Literal]]:
        print(f"variables passed {variables}")
        true_literals = [Literal(variable, True) for variable in variables]
        at_least_one :List[Tuple[Literal]] = [true_literals]
        
        
        false_literals = [Literal(variable, False) for variable in variables]
        at_most_one : List[Tuple[Literal]] = list(combinations(false_literals, 2))
        exactly_one = at_least_one + at_most_one
        # print("exactly_one")
        # print_clauses(exactly_one)
        return exactly_one
        
    # def convert_OR_clauses_to_AND_clauses(self, clauses):
    #     if len(clauses) == 1:
    #         return clauses
    #     c1 = clauses[0]
    #     c2 = clauses[1]
    #     new_clauses = self.covert_OR_clause_to_AND_clauses(c1, c2)
    #     for i in range(2, len(clauses)):
    #         c = clauses[i]
    #         new_clauses = self.covert_OR_clause_to_AND_clauses(new_clauses, c)
    #         print(f"new clauses: {new_clauses}")
    #     return new_clauses

    # def covert_OR_clause_to_AND_clauses(self, c1, c2):
    #     clauses = []
    #     for l1 in c1:
    #         for l2 in c2:
    #             clauses.append([l1, l2])
    #     return clauses

    def at_most_k_true(self, guess, k):
        literals = [Literal(f"{i}{guess[i]}", False) for i in range(len(guess))]
        return list(combinations(literals, k + 1))

    def at_least_k_true(self, guess, k):
        literals = [Literal(f"{i}{guess[i]}", True) for i in range(len(guess))]
        return list(combinations(literals, len(guess) - k+1))

    def exactly_k(self, guess, k):
        # if k==0 :
        #     return []
        return self.at_most_k_true(guess, k) + self.at_least_k_true(guess, k)

    def encode_guesses(self):
        clauses = []
        for guess, correct_digits in self.guesses:
            clauses.extend(self.exactly_k(guess, correct_digits))

        return clauses    

    def solve(self):
        self.add_starting_clauses()
        # for clause in self.clauses:
        #     for literal in clause:
        #         print(literal , end=' ')
        #     print()
            
        
        self.clauses.extend(self.encode_guesses())
        domain = [f"{i}{j}" for i in range(NUM_DIGITS) for j in range(10)]
        solver = SatSolver(self.clauses, domain)
        answer = solver.solve(self.clauses)
        if not answer: 
            return "No solution found"
        
        ans = ["" for _ in range(NUM_DIGITS)]
        print(answer.items())
        for key , val in answer.items():
            if val:
                print(key)
                if ans[int(key[0])] != "":
                    # violating the condition of one value per digit ?
                    print(f"wrong solution incoming{key[0]} {ans[int(key[0])]} {key[1]}")
                    raise Exception("Wrong solution")
                ans[int(key[0])] = key[1]
        return "".join(ans)


solver = NumberMindSolver()
print(solver.solve())
import sys
from typing import List, Tuple
from copy import deepcopy
from itertools import combinations
import random


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
        while True:
            found = False
            literal: Literal = None
            for clause in formula:
                if len(clause) == 1:
                    found = True
                    literal = clause[0]
                    print(
                        f"unit propagation: {literal} , literal.sign = {literal.sign}"
                    )
                    self.assignment[str(literal.name)] = literal.sign
                    break
            if literal:
                formula = self._delete_clauses_with_literal(formula, literal)
                formula = self._delete_literal_from_clauses(formula, literal)
            if not found:
                break
        return formula

    def _delete_clauses_with_literal(self, formula, literal) -> List:
        print(f"deleting clauses with literal {literal}")
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
            if pure_literal.sign and pure_literal.name in ["00", "01"]:
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

        formula = self.unit_propagation(formula)
        if [] in formula:
            return False, None

        formula = self.pure_literal_elimination(formula)

        if not formula:
            return True, self.assignment

        if [] in formula:
            return False, None

        if self.current_literal_index >= len(self.literal_values):
            return False, None

        choice = self.literal_values[i]

        if choice in self.assignment:
            return self.dpll_solve(formula, i + 1)

        print(f"trying choice {choice} , true")
        assignment_copy = deepcopy(self.assignment)
        satisfied, answer = self.dpll_solve(formula + [[Literal(choice, True)]], i + 1)

        if satisfied:
            return True, answer

        self.assignment = deepcopy(assignment_copy)

        print(f"trying choice {choice} , false")

        satisfied, answer = self.dpll_solve(formula + [[Literal(choice, False)]], i + 1)

        return (True, answer) if satisfied else (False, None)

    def solve(self, formula)-> List:
        satisfied, assignment = self.dpll_solve(formula)
        if not satisfied:
            return None
        for literal in self.literal_values:
            if literal not in assignment:
                assignment[literal] = False
        return assignment

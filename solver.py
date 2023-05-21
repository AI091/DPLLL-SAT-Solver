import sys 
from typing import List
from copy import deepcopy
import random 

class Literal: 
    def __init__(self, name: str , sign) -> None:
        self.name = name
        self.sign = sign 
        
    def __str__(self) -> str:
        return self.name if self.sign else f'-{self.name}'
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Literal):
            return False
        return self.name == other.name and self.sign == other.sign
    
    @classmethod
    def opposite(cls, literal1, literal2) -> bool:
        if not isinstance(literal1, Literal) or not isinstance(literal2, Literal):
            raise TypeError('literal1 and literal2 must be Literal objects')
        return literal1.name == literal2.name and literal1.sign != literal2.sign
    
    


class SatSolver: 
    def __init__(self) -> None:
        self.assignment = {}
        self.clauses = [] 
        self.literal_values = []
    
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
                if literal_str.startswith('-'):
                    literal = Literal(literal_str[1:], False)
                else:
                    literal = Literal(literal_str, True)
                clause.append(literal)
                if literal.name not in self.literal_values:
                    self.literal_values.append(literal.name)
            self.clauses.append(clause)
        
    
    def _print_clauses(self ,clauses) -> None:
        for clause in clauses:
            for literal in clause:
                print(literal, end=' ')
            print()

    def unit_propagation(self , formula:List) -> bool:
        for clause in formula:
            if len(clause)==1: 
                literal = clause[0]
                print(f"unit propagation: {literal} , literal.sign = {literal.sign}")
                self.assignment[literal.name] = literal.sign
                formula = self._delete_clauses_with_literal(formula , literal)
                formula = self._delete_literal_from_clauses(formula , literal)
        return formula
                            

    def _delete_clauses_with_literal(self , formula , literal) -> None:
        new_formula = []
        for clause in formula:
            found = any(l == literal for l in clause)
            if not found :
                new_formula.append(clause)
        return new_formula
    
    def _delete_literal_from_clauses(self , formula , literal) -> None:
        new_formula = []
        for clause in formula:
            new_clause = [l for l in clause if not Literal.opposite(l , literal)]
            new_formula.append(new_clause)
        return new_formula
        
    
    def pure_literal_elimination(self , formula) -> bool:
        while pure_literal := self._get_pure_literal(formula): 
            self.assignment[pure_literal.name] = pure_literal.sign
            formula = self._delete_clauses_with_literal(formula , pure_literal)
        return formula 
    
    def _get_pure_literal(self ,formula) -> Literal: 
        if not formula : 
            return None
         
        for literal in self.literal_values: 
            unique = True 
            found = False
            sign = None
            for clause in formula: 
                for l in clause :
                    if l.name == literal : 
                        if sign is None : 
                            sign = l.sign
                            found = True
                        elif sign != l.sign : 
                            unique = False
                            break 
            if unique and found : 
                return Literal(literal , sign)
        
        return None
                        
        
        
                
            
    
    def dpll_solve(self , formula , i): 
        print("step")
        formula = self.unit_propagation(formula)
        print(f"After unit propagation:\n ")
        self._print_clauses(formula)
        if [] in formula :
            return False , None
        print(f"assignment: {self.assignment}")
        formula = self.pure_literal_elimination(formula)
        print(f"After pure literal elimination:\n")
        self._print_clauses(formula)
        print(f"assignment: {self.assignment}")
        
        if not formula :
            return True , self.assignment

        for index in range (i , len(self.literal_values)):
            choice = self.literal_values[index]
            print(f"trying choice {choice} , true")
            formula_copy = deepcopy(formula) 
            formula_copy.append([Literal(choice , True)])
            satisfied , assignment = self.dpll_solve(formula_copy , i+1)
            if satisfied : 
                print("here")
                return True , assignment
            
            print(f"trying choice {choice} , false")
            formula_copy = deepcopy(formula)
            formula_copy.append([Literal(choice , False)])
            satisfied , assignment = self.dpll_solve(formula_copy , i+1)
            if satisfied :
                print("there")
                return True , assignment
        
        return False , None
    
    def solve(self , formula ):
        satisfied , assignment = self.dpll_solve(formula , 0)
        if satisfied :
            for literal in self.literal_values:
                if literal not in assignment:
                    print(f"literal {literal} not in assignment")
                    assignment[literal] = random.choice([True , False])
        return satisfied , assignment
    
    
            
        
        
    
solver = SatSolver()
solver.read_input()
answer = solver.solve(solver.clauses)
print(answer)


    
    
    
        
        
        
        
                    
            
from DPLL import *
from typing import List, Tuple
from itertools import combinations

NUM_DIGITS = 5


def print_clauses(clauses) -> None:
    for clause in clauses:
        print("clause: ", end=" ")
        for literal in clause:
            print(f"literal{literal}", end=" ")
        print()


class NumberMindSolver:
    def __init__(self) -> None:
        self.variables = [[f"{i}{j}" for j in range(10)] for i in range(NUM_DIGITS)]
        self.guesses = [
            ("90342", 2),
            ("70794", 0),
            ("39458", 2),
            ("34109", 1),
            ("51545", 2),
            ("12531", 1),
        ]
        self.clauses = []

    def add_starting_clauses(self):
        for digit in range(NUM_DIGITS):
            self.clauses.extend(self.exactly_one(self.variables[digit]))

    def exactly_one(self, variables) -> List[List[Literal]]:
        print(f"variables passed {variables}")
        true_literals = [Literal(variable, True) for variable in variables]
        at_least_one: List[Tuple[Literal]] = [true_literals]

        false_literals = [Literal(variable, False) for variable in variables]
        at_most_one: List[List[Literal]] = list(combinations(false_literals, 2))
        exactly_one = at_least_one + at_most_one
        return exactly_one

    def at_most_k_true(self, guess, k) -> List[List[Literal]]:
        literals = [Literal(f"{i}{guess[i]}", False) for i in range(len(guess))]
        return list(combinations(literals, k + 1))

    def at_least_k_true(self, guess, k) -> List[List[Literal]]:
        literals = [Literal(f"{i}{guess[i]}", True) for i in range(len(guess))]
        return list(combinations(literals, len(guess) - k + 1))

    def exactly_k(self, guess, k) ->List[List[Literal]]:
        return self.at_most_k_true(guess, k) + self.at_least_k_true(guess, k)

    def encode_guesses(self) ->List[List[Literal]]:
        clauses = []
        for guess, correct_digits in self.guesses:
            clauses.extend(self.exactly_k(guess, correct_digits))

        return clauses

    def solve(self) -> str:
        self.add_starting_clauses()

        self.clauses.extend(self.encode_guesses())
        domain = [f"{i}{j}" for i in range(NUM_DIGITS) for j in range(10)]
        solver = SatSolver(self.clauses, domain)
        answer = solver.solve(self.clauses)
        if not answer:
            return "No solution found"

        ans = ["" for _ in range(NUM_DIGITS)]
        print(answer.items())
        for key, val in answer.items():
            if val:
                ans[int(key[0])] = key[1]
        return "".join(ans)

if __name__ == "__main__":
    solver = NumberMindSolver()
    print(solver.solve())

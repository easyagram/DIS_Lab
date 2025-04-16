import re
import pandas as pd


terminal_symbols = {
    "true": "true",
    "false": "false",
    "*": "*",
    "/": "/",
    "+": "+",
    "-": "-",
    "or": "or",
    "and": "and",
    "not": "not",
    "end": "end",
    "const": "const",
    "def": "def",
    "=": "=",
    "<": "<",
    ">": ">",
    "(": "(",
    ")": ")",
    ",": ","
}

class Lexer:
    def __init__(self, input_string):
        self.tokens = self.tokenize(input_string)
        self.current_index = 0

    def tokenize(self, input_string):
        words = input_string.split()
        tokens = list(map(lambda w: terminal_symbols.get(w, w), words))
        tokens.append("end")
        return tokens

    def get_current_token(self):
        return self.tokens[self.current_index] if self.current_index < len(self.tokens) else None

    def accept(self, symbol):
        (lambda: setattr(self, 'current_index', self.current_index + 1)
         if self.get_current_token() == symbol else None)()

    def error(self, symbol, valid_symbols):
        (lambda: (_ for _ in ()).throw(ValueError("ERROR"))
         if symbol not in valid_symbols else None)()

class Stack:
    def __init__(self):
        self.stack = []

    push = lambda self, item: self.stack.append(item)
    pop = lambda self: self.stack.pop() if self.stack else None
    is_empty = lambda self: not self.stack
    __repr__ = lambda self: str(self.stack)

class IState:
    execute = lambda self: None

class LL1Parser:
    state_map = {
        (0, 0, 0, 0): lambda *args: args[2],
        (0, 0, 0, 1): lambda *args: args[3].error(args[1], args[5]) or args[2],
        (0, 1, 0, 1): lambda *args: args[3].error(args[1], args[5]) or args[4].push(args[0] + 1) or args[2],
        (0, 0, 1, 1): lambda *args: args[3].error(args[1], args[5]) or args[3].accept(args[1]) or args[2],
        (1, 0, 0, 1): lambda *args: args[3].error(args[1], args[5]) or (args[4].pop() if not args[4].is_empty() else args[2]),
        (1, 0, 1, 1): lambda *args: args[3].error(args[1], args[5]) or args[3].accept(args[1]) or (args[4].pop() if not args[4].is_empty() else args[2])
    }

    def __init__(self, transitions):
        self.transitions = transitions
        self.current_state = 1
        self.stack = Stack()
        self.lexer = None

    def process(self, tokens):
        self.lexer = Lexer(" ".join(tokens))
        current_token = self.lexer.get_current_token()

        while current_token is not None:
            (lambda: print("Parsing complete") or exit()
             if current_token == 'end' and self.stack.is_empty() else None)()
            state_data = self.transitions[self.current_state]
            print(f"State: {self.current_state}\t Token: {current_token}\t Stack: {self.stack}")
            valid_tokens, next_state, attr1, attr2, attr3, attr4 = state_data
            state_key = (attr1, attr2, attr3, attr4)
            self.current_state = self.state_map[state_key](
                self.current_state, current_token, next_state,
                self.lexer, self.stack, valid_tokens
            )
            current_token = self.lexer.get_current_token()
        print("Grammar is true")


df = pd.read_excel("predict_set.xlsx", index_col="№")
dictionary = {i: [df[j][i] for j in df.columns] for i in range(1, df.shape[0] + 1)}


input_code = "27 - 10 * ( 10 + 6 / 7 - ( 30 - 2 ) )"
lexer = Lexer(input_code)
tokens = lexer.tokens
ll1 = LL1Parser(dictionary)
print(f"\nINPUT: {input_code}")
print("----------------------------")
ll1.process(tokens)

input_code = "20 * 2 /"
lexer = Lexer(input_code)
tokens = lexer.tokens
ll1 = LL1Parser(dictionary)
print(f"\nINPUT: {input_code}")
print("----------------------------")
ll1.process(tokens)

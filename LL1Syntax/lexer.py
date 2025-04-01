import re

class Lexer:
    token_spec = [
        ('NUMBER', r'\d+'),
        ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('OP', r'[+\-*/]'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('BOOL', r'true|false'),
        ('SKIP', r'[ \t\n]+'),
        ('MISMATCH', r'.')
    ]
    patterns = [(name, re.compile(pattern)) for name, pattern in token_spec]
    
    def __init__(self, code):
        self.tokens = self.tokenize(code)
        self.index = 0

    def tokenize(self, code):
        tokens = []
        while code:
            for name, pattern in self.patterns:
                match = pattern.match(code)
                if match:
                    tokens += [] if name == 'SKIP' else [(name, match.group(0))]
                    code = code[match.end():]
                    break
        return tokens
    
    def next_token(self):
        self.index += 1
        return self.tokens[self.index - 1] if self.index <= len(self.tokens) else None

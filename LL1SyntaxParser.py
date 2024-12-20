import re

TOKEN_RE = [
    ('NUMBER', r'\d+'),
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('TIMES', r'\*'),
    ('DIVIDE', r'/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('TRUE', r'true'),
    ('FALSE', r'false'),
    ('SKIP', r'[ \t\n]+'),
    ('MISMATCH', r'.')
]

def tokenize(code):
    tokens = []
    while code:
        match = None
        for token_type, token_regex in TOKEN_RE:
            regex = re.compile(token_regex)
            match = regex.match(code)
            if match:
                tokens += [] if token_type == 'SKIP' else [(token_type, match.group(0))]
                code = code[match.end(0):]
                break
        if not match:
            raise SyntaxError(f'Неизвестный символ: {code[0]}')
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.next_token()

    def next_token(self):
        self.token_index += 1
        self.current_token = self.tokens[self.token_index] if self.token_index < len(self.tokens) else None

    def parse(self):
        return self.E()

    def E(self):
        node = self.T()
        while self.current_token and self.current_token[0] in ('PLUS', 'MINUS'):
            op = self.current_token
            self.next_token()
            node = (op, node, self.T())
        return node

    def T(self):
        node = self.F()
        while self.current_token and self.current_token[0] in ('TIMES', 'DIVIDE'):
            op = self.current_token
            self.next_token()
            node = (op, node, self.F())
        return node

    def F(self):
        token_cases = [
            (self.current_token[0] == 'LPAREN', lambda: (self.next_token(), self.E(), self.next_token())[1]),
            (self.current_token[0] == 'ID', lambda: (self.current_token, self.next_token())[0]),
            (self.current_token[0] == 'NUMBER', lambda: (self.current_token, self.next_token())[0]),
            (self.current_token[0] in ('TRUE', 'FALSE'), lambda: (self.current_token, self.next_token())[0])
        ]
        for condition, action in token_cases:
            if condition:
                return action()
        raise SyntaxError('Ожидался фактор')

def main():
    code = "a + b * 3 - true"
    tokens = tokenize(code)
    parser = Parser(tokens)
    parse_tree = parser.parse()
    print('Разобранное выражение:', parse_tree)

if __name__ == "__main__":
    main()

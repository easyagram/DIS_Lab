import pandas as pd

class LL1Parser:
    def __init__(self, table_file):
        self.transitions = pd.read_excel(table_file, index_col="№").to_dict(orient="index")
        self.stack = Stack()
    
    def parse(self, lexer):
        token = lexer.next_token()
        while token:
            self.stack.push(token)
            rule = self.transitions.get(token[0], {}).get(token[1])
            self.stack.pop() if rule else None
            token = lexer.next_token()
        return self.stack.is_empty()

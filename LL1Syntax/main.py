if __name__ == "__main__":
    lexer = Lexer("x + 42")
    parser = LL1Parser("predict_set.xlsx")
    print("Valid expression" if parser.parse(lexer) else "Invalid expression")

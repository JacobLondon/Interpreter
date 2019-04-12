"""
factor = NUMBER or LPAREN expr RPAREN
term   = factor((MUL or DIV) factor)
expr   = term((PLUS or MINUS) term)
"""

NUM, PLUS, MINUS, ASTRISK, FSLASH, DOT, LPAREN, RPAREN, EOF = (
    'NUM', 'PLUS', 'MINUS', 'ASTRISK', 'FSLASH', 'DOT', 'LPAREN', 'RPAREN', 'EOF'
)

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

class Lexer:
    
    def __init__(self, filename=None, text=None):
        if filename is not None:
            self.text = open(filename, 'r').read()
        elif text is not None:
            self.text = text
        else:
            raise "What no file or text?"
        self.index = 0
        self.current = self.text[self.index]

    def advance(self):
        self.index += 1
        if self.index >= len(self.text):
            self.current = None
        else:
            self.current = self.text[self.index]

    def skip_whitespace(self):
        while self.current is not None and self.current.isspace():
            self.advance()

    # variable length number
    def number(self):
        number = []
        while self.current is not None and (self.current.isdigit() or self.current == '.'):
            number.append(self.current)
            self.advance()

        result = ''.join(number)
        return float(result)

    def next_token(self):

        while self.current is not None:

            if self.current.isspace():
                self.skip_whitespace()
                continue

            if self.current.isdigit():
                return Token(NUM, self.number())

            if self.current == '*':
                self.advance()
                return Token(ASTRISK, '*')
            if self.current == '/':
                self.advance()
                return Token(FSLASH, '/')
            if self.current == '+':
                self.advance()
                return Token(PLUS, '+')
            if self.current == '-':
                self.advance()
                return Token(MINUS, '-')
            if self.current == '(':
                self.advance()
                return Token(LPAREN, '(')
            if self.current == ')':
                self.advance()
                return Token(RPAREN, ')')

            raise "Invalid token"
        
        return Token(EOF, None)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.next_token()
        else:
            raise "Invalid syntax"

    def factor(self):
        token = self.current_token

        if token.type == NUM:
            self.eat(NUM)
            return token.value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result

    def term(self):
        result = self.factor()

        while self.current_token.type in (ASTRISK, FSLASH):
            token = self.current_token
            if token.type == ASTRISK:
                self.eat(ASTRISK)
                result *= self.factor()
            elif token.type == FSLASH:
                self.eat(FSLASH)
                result /= self.factor()
        return result

    def expr(self):
        result = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result += self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result -= self.term()
        return result

    def read(self):
        return self.expr()

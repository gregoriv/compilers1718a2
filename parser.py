"""
Grammar:
Stmt_list   -> Stmt Stmt_list
              |.
Stmt        -> id assign Expr
              |print Expr.
Expr -> Term Term_tail.
Term_tail   -> Orop Term Term_tail
              |.
Term        -> Factor Factor_tail.
Factor_tail -> Andop Factor Factor_tail
              |.
Factor      -> Notop FNotop.
FNotop      -> (Expr) 
              |id
              |Boolean.
Boolean     -> true
              |false
              |t
              |f
              |0
              |1.
Orop        -> or.
Andop       -> and.
Notop       -> not.
"""
import plex

class ParseError(Exception):
    pass


class MyParser():

    def create_scanner(self, fp):
        letter = plex.Range("azAZ")
        digit = plex.Range("09")

        keywords = plex.Str("print", "not", "and", "or")
        true_keyword = plex.NoCase(plex.Str("true", "t", "1"))
        false_keyword = plex.NoCase(plex.Str("false", "f", "0"))
        identifier = letter + plex.Rep(letter | digit)
        assign = plex.Str("=")
        parenthesis = plex.Str("(", ")")
        space = plex.Rep1(plex.Any(" \n\t"))

        lexicon = plex.Lexicon([
            (keywords, plex.TEXT),
            (true_keyword, "True"),
            (false_keyword, "False"),
            (identifier, "IDENTIFIER"),
            (assign, "="),
            (parenthesis, plex.TEXT),
            (space, plex.IGNORE)
        ])

        self.scanner = plex.Scanner(lexicon, fp)
        self.la, self.val = self.next_token()

    def next_token(self):
        return self.scanner.read()

    def match(self, token):
        if self.la == token:
            self.la, self.val = self.next_token()
        else:
            raise ParseError("Excpected: ", self.la)

    def parse(self, fp):
        self.create_scanner(fp)
        self.stmt_list()

    def stmt_list(self):
        # print("stmt_list: ", self.la)
        if self.la in ["IDENTIFIER", "print"]:
            self.stmt()
            self.stmt_list()
        elif self.la is None:
            return
        else:
            raise ParseError("Excpected: identifier or print")

    def stmt(self):
        # print("stmt: ", self.la)
        if self.la == "IDENTIFIER":
            self.match("IDENTIFIER")
            self.match("=")
            self.expr()
        elif self.la == "print":
            self.match("print")
            self.expr()
        else:
            raise ParseError("Excpected: identifier or print")

    def expr(self):
        # print("expr: ", self.la)
        if self.la in ["(", "not", "IDENTIFIER", "True", "False"]:
            self.term()
            self.term_tail()
        else:
            raise ParseError("Excpected: '(' or IDENTIFIER or boool value")

    def term_tail(self):
        # print("term_tail: ", self.la)
        if self.la == "or":
            self.orop()
            self.term()
            self.term_tail()
            return
        elif self.la in ["IDENTIFIER", "print", ")"] or self.la is None:
            return
        else:
            raise ParseError("Excpected: 'or'")

    def term(self):
        # print("term: ", self.la)
        if self.la in ["(", "not", "IDENTIFIER", "True", "False"]:
            self.factor_and_fnotop()
            self.factor_tail()
            return
        else:
            raise ParseError("Excpected: '(' or IDENTIFIER or boool value")

    def factor_tail(self):
        # print("factor_tail: ", self.la)
        if self.la == "and":
            self.andop()
            self.factor_and_fnotop()
            self.factor_tail()
            return
        elif self.la in ["or", "print", "IDENTIFIER", ")"] or self.la is None:
            return
        else:
            raise ParseError("Excpected: 'and'")

    def factor_and_fnotop(self):
        # print("factor_and_fnotop: ", self.la)
        self.notop()
        if self.la == '(':
            self.match('(')
            self.expr()
            self.match(')')
            return
        elif self.la == "IDENTIFIER":
            self.match(self.la)
        elif self.la in ["True", "False"]:
            self.match(self.la)
        else:
            raise ParseError("Excpected: id, (expr), values")

    def orop(self):
        # print("orop: ", self.la)
        if self.la == "or":
            self.match("or")
        else:
            raise ParseError("Excpected: 'or'")

    def andop(self):
        # print("andop: ", self.la)
        if self.la == "and":
            self.match("and")
        else:
            raise ParseError("Excpected: 'and'")

    def notop(self):
        # print("notop: ", self.la)
        if self.la == "not":
            self.match("not")
        else:
            return

parser = MyParser()
fp = open("input.txt", "r")
try:
    parser.parse(fp)
except ParseError as perr:
    print(str(perr))
fp.close()

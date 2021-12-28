from scanner import *
import os


class node:
    def __init__(self, token=None) -> None:
        self.children = []
        if token is not None:
            self.num_childern = 0
            self.string_operation=""
            self.is_root = False
            self.is_first_statement = True
            self.is_repeat = False
            self.is_if = False
            self.right_node = None
            self.is_statement = False
            self.is_else_part = False
            self.nodeToken = token
        else:
            self.num_childern = 0
            self.string_operation = ""
            self.is_root = False
            self.is_first_statement = True
            self.is_repeat = False
            self.is_if = False
            self.right_node = None
            self.is_else_part = False
            self.is_statement = False
            self.nodeToken = None

    def addChild(self, child):
        self.children.append(child)
        self.num_childern += 1

    def getChild(self):
        return self.children


class Tree:
    def __init__(self, path) -> None:
        self.root = None
        file = open(path, "r")
        str = file.read()+" "
        self.scanner = Scanner(str)
        print(self.scanner.get_all_tokens())
        self.parse()

    def parse(self):
        self.root = node()
        self.root.is_root = True
        self.statement_sequance(self.root)
        x = None

    def setRoot(self, ptr):
        self.root = ptr

    def getRoot(self):
        return self.root

    def statement_sequance(self, parent):
        n = self.statement(parent)
        if parent.is_root:
            parent.addChild(n)
        elif ((parent.is_repeat or parent.is_if) and parent.is_first_statement) or parent.is_else_part:
            parent.is_first_statement = False
            parent.addChild(n)
        else:
            parent.right_node = n
        token = self.scanner.get_token(True)
        if token.tokenType == 'SEMICOLON':
            self.scanner.match(token)
            self.statement_sequance(n)

    def statement(self, parent):
        token = self.scanner.get_token(False)
        n = node(token)
        n.is_statement = True
        if token.tokenType == 'IF':
            n.is_if = True
            self.if_statement(n)
        elif token.tokenType == 'REPEAT':
            n.is_repeat = True
            self.repeat_statement(n)
        elif token.tokenType == 'READ':
            token = self.scanner.get_token(False)
            if token.tokenType == 'IDENTIFIER':
                n.string_operation = "READ\n"+str(token.tokenValue)
                #n.addChild(node(token))
        elif token.tokenType == 'WRITE':
            self.exp(n)
        elif token.tokenType == 'IDENTIFIER':
            token = self.scanner.get_token(False)
            n.string_operation = "ASSIGN"
            if token.tokenType != "Assign":
                pass
            self.exp(n)
        return n

    def factor(self, parent):
        token = self.scanner.get_token(False)
        n=node(token)
        if token.tokenType == "IDENTIFIER" or token.tokenType == "number":
            parent.addChild(n)
            n.string_operation=token.tokenType
        elif token.tokenType == "OPEN_PARENTHESIS":
            self.exp(parent)
            token = self.scanner.get_token(False)
            if token.tokenType != "CLOSE_PARENTHESIS":
                pass
        else:
            pass

    def trem(self, parent):
        n = node()
        self.factor(n)
        token = self.scanner.get_token(True)
        if token.tokenType == "MULTIPLY" or token.tokenType == "DIVISION":
            self.scanner.match(token)
            n.nodeToken = token
            n.string_operation = "OP"
            parent.addChild(n)
            self.trem(n)
        else:
            parent.addChild(n.children[0])
            del n

    def simple_exp(self, parent):
        n = node()
        self.trem(n)
        token = self.scanner.get_token(True)
        if token.tokenType == "PLUS" or token.tokenType == "MINUS":
            self.scanner.match(token)
            n.nodeToken = token
            n.string_operation = "OP"
            parent.addChild(n)
            self.simple_exp(n)
        else:
            parent.addChild(n.children[0])
            del n

    def exp(self, parent):
        n = node()
        self.simple_exp(n)
        token = self.scanner.get_token(True)
        if token.tokenType == "SMALLER" or token.tokenType == "EQUAL":
            self.scanner.match(token)
            n.nodeToken = token
            parent.addChild(n)
            n.string_operation="OP"
            self.simple_exp(n)
            y = None
        else:
            parent.addChild(n.children[0])
            del n

    def repeat_statement(self, parent):
        self.statement_sequance(parent)
        x=1
        token = self.scanner.get_token(False)
        if token.tokenType != "UNTIL":
            # ERROR UNTIL IS MISSING
            pass
        self.exp(parent)

    def if_statement(self, parent):
        self.exp(parent)
        token = self.scanner.get_token(False)
        if token.tokenType == "THEN":
            self.statement_sequance(parent)
        else:
            # ERROR missing then
            pass
        token = self.scanner.get_token(False)
        if token.tokenType == "ELSE":
            parent.is_else_part = True
            self.statement_sequance(parent)
            token = self.scanner.get_token(False)
            ####################################################################
            if token.tokenType != "END":
                # end of else is missing
                pass
            #####################################################################
        elif token.tokenType != "END":
            # error code end missing
            pass

    def print(self, root):
        global tree
        tree.append(root)
        if len(root.children) > 0:
            for i in root.children:
                self.print(i)
            if root.right_node is not None:
                self.print(root.right_node)
        else:
            if root.right_node is not None:
                self.print(root.right_node)
            else:
                return


tree = []

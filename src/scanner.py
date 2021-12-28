class Token:
    def __init__(self) -> None:
        self.tokenValue = ""
        self.tokenType = ""
        self.tokenLength = 0


class Scanner:
    def __init__(self, text):
        self.last_token=Token()
        self.text = text
        self.index = 0
        self.len = len(self.text)
        self.state = {
            'START': 0,
            'INNUM': 1,
            'INID': 2,
            'INASSIGN': 3,
            'INCOMMENT': 4
        }
        self.symbol_name = {
            '+': 'PLUS',
            '-': 'MINUS',
            '*': 'MULTIPLY',
            '/': 'DIVISION',
            '=': 'EQUAL',
            '<': 'SMALLER',
            '(': 'OPEN_PARENTHESIS',
            ')': 'CLOSE_PARENTHESIS',
            ';': 'SEMICOLON',
        }
        self.loops_name = {
            'if': 'IF',
            'then': 'THEN',
            'else': 'ELSE',
            'end': 'END',
            'repeat': 'REPEAT',
            'until': 'UNTIL',
            'read': 'READ',
            'write': 'WRITE'
        }
        self.symbols = ['+', '-', '*', '/', ';', '<', '=', '(', ')']

    def is_symbol(self, input):
        return True if input in self.symbols else False

    def is_letter(self, input):
        return (input >= 'A' and input <= 'z')

    def is_digit(self, input):
        return (input >= '0' and input <= '9')

    def is_space(self, input):
        return (input == ' ' or input == '\n' or input == '\t')

    def symbol(self, input):
        token = Token()
        token.tokenValue = input
        token.tokenType = self.symbol_name[input] if self.symbol_name.get(
            input) else "ERROR"
        return token

    def reserved(self, input):
        token = Token()
        token.tokenValue = input
        token.tokenType = self.loops_name[input] if self.loops_name.get(
            input) else "IDENTIFIER"
        return token

    def get_token(self, look_ahead):
        currToken = Token()
        state = self.state['START']
        temp = self.index
        for i in range(self.index, self.len):
            curr_char = self.text[i]
            if state == self.state['START']:
                if self.is_space(curr_char):
                    continue
                if self.is_symbol(curr_char):
                    if (curr_char=='-' or curr_char=='+')and(self.last_token.tokenType != "number" and self.last_token.tokenType != "IDENTIFIER"):
                        currToken.tokenValue += curr_char
                        state= self.state['INNUM']
                        continue
                    currToken = self.symbol(curr_char)
                    self.index = i + 1
                    currToken.tokenLength = self.index - temp
                    if look_ahead == True:
                        self.index = temp
                    else:
                        self.last_token=currToken
                    return currToken
                elif curr_char == '{':
                    state = self.state['INCOMMENT']
                    continue
                elif curr_char == ':':
                    currToken.tokenValue += curr_char
                    state = self.state['INASSIGN']
                    continue
                elif self.is_digit(curr_char):
                    currToken.tokenValue += curr_char
                    state = self.state['INNUM']
                    continue
                elif self.is_letter(curr_char):
                    currToken.tokenValue += curr_char
                    state = self.state['INID']
                    continue
            elif state == self.state['INNUM']:
                if self.is_digit(curr_char):
                    currToken.tokenValue += curr_char
                    continue
                else:
                    self.index = i
                    currToken.tokenType = "number"
                    currToken.tokenLength = self.index - temp
                    if look_ahead == True:
                        self.index = temp
                    else:
                        self.last_token = currToken
                    return currToken
            elif state == self.state['INID']:
                if self.is_letter(curr_char):
                    currToken.tokenValue += curr_char
                    continue
                else:
                    self.index = i
                    currToken = self.reserved(currToken.tokenValue)
                    currToken.tokenLength = self.index - temp
                    if look_ahead == True:
                        self.index = temp
                    else:
                        self.last_token = currToken
                    return currToken
            elif state == self.state['INASSIGN']:
                if curr_char == '=':
                    currToken.tokenValue += curr_char
                    self.index = i+1
                    currToken.tokenType = "Assign"
                    currToken.tokenLength = self.index - temp
                    if look_ahead == True:
                        self.index = temp
                    else:
                        self.last_token = currToken
                    return currToken
                else:
                    self.index = i
                    currToken.tokenType = "Error"
                    currToken.tokenLength = self.index - temp
                    if look_ahead == True:
                        self.index = temp
                    else:
                        self.last_token = currToken
                    return currToken
            elif state == self.state['INCOMMENT']:
                if curr_char == '}':
                    state = self.state['START']
                    continue
                else:
                    continue
        currToken.tokenLength = self.index - temp
        if look_ahead == True:
            self.index = temp
        else:
            self.last_token = currToken
        return currToken

    def match(self, token):
        self.index += token.tokenLength

    def get_all_tokens(self):
        tokens = ""
        while self.index != (self.len-1):
            t = self.get_token(False)
            tokens += ('<' + t.tokenValue + ',' + t.tokenType + '>\n')
        self.index = 0
        return tokens


# my_str = '''{ Sample program in TINY language – computes factorial}
# 	read x; {input an integer }
# 	if  0 < x   then{ don’t compute if x <= 0 }
# 	fact:= 1;
# 	repeat "
# 	fact := fact * x;
# 	x:= x - 1
# 	until  x = -5;
# 	write  fact{ output  factorial of x }
# 	end '''
# sca = Scanner(my_str)
# print(sca.get_all_tokens())

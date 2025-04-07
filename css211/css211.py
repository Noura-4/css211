# front.py - a lexical analyzer system for simple arithmetic expressions

# Character classes
LETTER = 0
DIGIT = 1
UNKNOWN = 99

# Token codes
INT_LIT = 10
IDENT = 11
ASSIGN_OP = 20
ADD_OP = 21
SUB_OP = 22
MULT_OP = 23
DIV_OP = 24
LEFT_PAREN = 25
RIGHT_PAREN = 26

# Globals
charClass = None
lexeme = ''
nextChar = ''
lexLen = 0
nextToken = None
in_fp = None

def addChar():
    global lexeme, lexLen
    if lexLen <= 98:
        lexeme += nextChar
        lexLen += 1
    else:
        print("Error - lexeme is too long")

def getChar():
    global nextChar, charClass
    nextChar = in_fp.read(1)
    if nextChar:
        if nextChar.isalpha():
            charClass = LETTER
        elif nextChar.isdigit():
            charClass = DIGIT
        else:
            charClass = UNKNOWN
    else:
        charClass = EOF

def getNonBlank():
    global nextChar
    while nextChar.isspace():
        getChar()

def lookup(ch):
    global nextToken
    lookup_table = {
        '(': LEFT_PAREN,
        ')': RIGHT_PAREN,
        '+': ADD_OP,
        '-': SUB_OP,
        '*': MULT_OP,
        '/': DIV_OP
    }
    addChar()
    nextToken = lookup_table.get(ch, EOF)
    return nextToken

def lex():
    global lexeme, lexLen, nextToken
    lexeme = ''
    lexLen = 0
    getNonBlank()
    
    if charClass == LETTER:
        addChar()
        getChar()
        while charClass in (LETTER, DIGIT):
            addChar()
            getChar()
        nextToken = IDENT

    elif charClass == DIGIT:
        addChar()
        getChar()
        while charClass == DIGIT:
            addChar()
            getChar()
        nextToken = INT_LIT

    elif charClass == UNKNOWN:
        lookup(nextChar)
        getChar()

    elif charClass == EOF:
        nextToken = EOF
        lexeme = 'EOF'

    print(f"Next token is: {nextToken}, Next lexeme is {lexeme}")
    return nextToken

# Custom EOF constant
EOF = -1

# Main driver
def main():
    global in_fp
    try:
        with open("front.in", "r") as in_fp_obj:
            global in_fp
            in_fp = in_fp_obj
            getChar()
            while True:
                if lex() == EOF:
                    break
    except FileNotFoundError:
        print("ERROR - cannot open front.in")

if __name__ == "__main__":
    main()


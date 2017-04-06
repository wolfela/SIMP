import re
import operator

operators = { "+": operator.add, "-": operator.sub, "/": operator.truediv, "*": operator.mul}

control = []
results = []
memory = dict()


def push(array, x):
    return array.insert(0, x)


def pop(array):
    return array.pop(0)


def evaluate(op, num1, num2):
    return operators[op](int(num1), int(num2))


def checkFront():
    current = control.pop()

    if type(current) is str:
        patternAll = re.compile('\d* \* \d*|\d* / \d*|\d* \+ \d*|\d* - \d*')
        patternSign = re.compile('\*|\+|-|/')
        patternDigit = re.compile('[\d]*')
        patternValue = re.compile('!')

        if patternAll.match(current):
            digits = list(filter(None, patternDigit.findall(current)))
            sign = list(filter(None, patternSign.findall(current)))
            push(control, sign[0])
            push(control, digits[1])
            push(control, digits[0])

        elif patternSign.match(current):
            push(results, str(evaluate(current, pop(control), pop(control))))

        elif patternValue.match(current):
            push(results, memory.get(current))
            
        elif patternDigit.match(current):
            push(results, current)

    if (len(control) is not 0):
        checkFront()

push(control, '9 + 9')
checkFront()
print(results)

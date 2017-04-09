import operator

operators = {"+": operator.add, "-": operator.sub, "/": operator.truediv, "*": operator.mul}
boperators = {">": operator.ge, "<": operator.le, "=": operator.eq}

control = []
results = []
memory = []


class Expr:
    num = None

    def __init__(self, num):
        self.num = num


class ExprOpExpr(Expr):
    left = None
    right = None

    def __init__(self, expr1, op, expr2):
        self.left = expr1
        self.right = expr2
        self.op = op


class Op:
    op = None

    def __init__(self, opr):
        self.op = opr

    def eval(self, num1, num2):
        return operators[self.op](int(num1), int(num2))


class Bool:
    value = None

    def __init__(self, val):
        self.value = val


class Bop:
    bop = None

    def __init__(self, op):
        self.bop = op

    def eval(self, num1, num2):
        return boperators[self.bop](int(num1), int(num2))


class NotExpr(Bool):
    value = None

    def __init__(self, val):
        self.value = val


class AndExpr(Bool):
    right = None
    left = None

    def __init__(self, bool1, bool2):
        self.left = bool1
        self.right = bool2


class And:

    def eval(self, left, right):
        return left.value and right.value


class Not:

    def eval(self, expr):
        return not expr.value



class ExprBopExpr(Bool):
    left = None
    right = None

    def __init__(self, op, expr1, expr2):
        self.left = expr1
        self.right = expr2
        self.bop = op


class Var:
    location = None
    value = None

    def __init__(self, val, loc):
        self.value = val
        self.location = "!" + loc


def run():
    exp = control.pop()
    if type(exp) is ExprOpExpr:
        control.append(exp.op)
        control.append(exp.left)
        control.append(exp.right)

    elif type(exp) is ExprBopExpr:
        control.append(exp.bop)
        control.append(exp.left)
        control.append(exp.right)

    elif type(exp) is AndExpr:
        control.append(And())
        control.append(exp.left)
        control.append(exp.right)

    elif type(exp) is NotExpr:
        control.append(Not())
        control.append(exp.value)

    elif type(exp) is And:
        results.append(Bool(And.eval(exp, Bool(results.pop().value), Bool(results.pop().value))))

    elif type(exp) is Not:
        results.append(Bool(Not.eval(exp, Bool(results.pop().value))))

    elif type(exp) is Bop:
        results.append(Bool(Bop.eval(exp, int(results.pop().num), int(results.pop().num))))

    elif type(exp) is Op:
        results.append(Expr(Op.eval(exp, int(results.pop().num), int(results.pop().num))))

    elif type(exp) is Expr:
        results.append(exp)

    elif type(exp) is Bool:
        results.append(exp)

    elif type(exp) is str:
        for var in memory:
            if var.location == exp:
                results.append(var.value)

    if len(control) > 0:
        run()


# Tests

bool1 = Bool(True)
bool2 = Bool(True)
expr1 = Expr(1)
expr2 = Expr(2)
bop1 = Bop("<")
comp1 = ExprBopExpr(bop1, expr1, expr2)
and1 = AndExpr(bool1, bool2)
not1 = NotExpr(bool1)

control.append(comp1)
control.append(and1)
control.append(not1)

run()

for result in results:
    if type(result) is Expr:
        print(result.num)
    elif type(result) is Bool:
        print(result.value)
    else:
        print(result)


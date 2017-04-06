import operator

operators = {"+": operator.add, "-": operator.sub, "/": operator.truediv, "*": operator.mul}

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

    elif type(exp) is Op:
        results.append(Expr(Op.eval(exp, int(results.pop().num), int(results.pop().num))))

    elif type(exp) is Expr:
        results.append(exp)

    elif type(exp) is str:
        for var in memory:
            if var.location == exp:
                results.append(var.value)

    if len(control) > 0:
        run()


# Tests

exp1 = Expr(12)
exp2 = Expr(13)
op1 = Op("+")
expr1 = ExprOpExpr(exp1, op1, exp2)

exp3 = Expr(8)
exp4 = Expr(9)
op2 = Op("*")
exp5 = Expr(7)
exp6 = Expr(6)
exprsub1 = ExprOpExpr(exp5, op2, exp6)
exprsub2 = ExprOpExpr(exp3, op2, exp4)
expr2 = ExprOpExpr(exprsub1, op2, exp3)

kurwa = Var("kurwidol", "kurwa")

memory.append(kurwa)

control.append("!kurwa")
control.append(expr2)

run()

for result in results:
    if (type(result) is Expr):
        print(result.num)
    else:
        print (result)
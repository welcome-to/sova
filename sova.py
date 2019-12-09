class Operator:
    def __init__(self, func, arity):
        self.func = func
        self.arity = arity

    def __str__(self):
        pass

    def __call__(self, *args):
        assert len(args) == arity, "Wrong number of arguments"
        return self.func(args)

class Composition:
    def __init__(self,operator, args_list):
        self.operator = operator
        self.args = args_list

    def __call__(self):
        return self.operator(*self.args)




class Constant(Operator):
    def __init__(self,boolean):
        Constant.super().__init__(lambda: boolean)

class And(Operator):
    def __init__(self):
        And.super().__init__(lambda x,y: x and y, 2)



class Not(Operator):
    def __init__(self):
        Not.super().__init__(lambda x: not x, 1)


class Or(Operator):
    def __init__(self):
        Or.super().__init__(lambda x,y: x or y, 2)


class Xor(Operator):
    def __init__(self):
        Xor,super().__init__(lambda x,y:not x == y, 2)


class Eq(Operator):
    def __init__(self):
        Eq.super().__init__(lambda x,y: x == y, 2)


class Impl(Operator):
    def __init__(self):
        Impl.super().__init__(lambda x, y: x < y, 2)



class Nand(Operator):
    def __init__(self):
        Nand.super().__init__(lambda x , y: not x and y, 2)



class Nor(Operator):
    def __init__(self):
        Nor.super().__init__(lambda x ,y: not x or y, 2)




priorities = {
    'not': 0,
    'and': 1,
    'nand': 1,
    'or': 2,
    'nor': 2,
    'xor': 3,
    'impl': 4,
    'equiv': 5
}

FuncType = {
    'not'  : Not,
    'and'  : And,
    'nand' : Nand,
    'or'   : Or,
    'nor'  : Nor,
    'xor'  : Xor,
    'impl' : Impl,
    'equiv': Eq

}


def parser_copy(line):
    is_in_brackets = True
    balance = 0
    for (index, char) in enumerate(line):
        if balance == 0 and index > 0:
            is_in_brackets = False
            break
        if (char == '('):
            balance += 1
        if (char == ')'):
            balance -= 1

    assert balance == 0, "Wrong bracket balance"

    if is_in_brackets:
        return parse(line[1:n-1])

    prior_operator, prior_start = None, None
    balance = 0
    for start in range(len(name)):
        if line[start] == '(':
            balance += 1
        if line[start] == ')':
            balance -= 1
        if balance == 0:
            for name in priorities.keys():
                if line.startswith(name):
                    if not prior_operator or priorities[name] >= priorities[prior_operator]:
                        prior_operator, prior_start = name, start

    if prior_operator is not None:
        if prior_start == 0:
            return Composition(Not(), [parser_copy(line[3:])])
        return Composition(
            FuncType[prior_operator](),
            [parser_copy(line[:prior_start]),parse(line[prior_start + len(prior_operator):])]
            )

    if line in ['1','0']:
        return Constant(bool(int(line)))
    return Variable(line)
    
class Operator:
    def __init__(self, func, arity):
        self.func = func
        self.arity = arity

    def __str__(self):
        pass

    def __call__(self, *args):
        assert len(args) == arity, "Wrong number of arguments"
        return self.func(args)

class Composition
class And(Operator):
    def __init__(self):
        And.super().__init__(lambda x,y: x and y, 2)

    def __str__(self):
        return "(" + 

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

def parse(line):
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
    for start in range(len(name)):
        for name in priorities.keys():
            if current.startswith(name):
                if not prior_operator or priorities[name] >= priorities[prior_operator]:
                    prior_operator, prior_start = name, start
    
    if prior_operator is not None:
        if prior_start == 0: # unary
            return Composition(Not(), [parse(line[3:])])
        return Composition(
            FuncType(prior_operator),
            [parse(line[:prior_start]), parse(line[prior_start + len(prior_operator):])]
        ) # FIXME

    if line in ['1', '0']:
        return Constant(bool(int(line)))

    
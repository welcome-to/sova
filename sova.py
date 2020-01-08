from itertools import product





class Operator:
    def __init__(self, func, arity):
        self.func = func
        self.arity = arity

    def __str__(self):
        pass

    def __call__(self, *args):
        assert len(args) == self.arity, "Wrong number of arguments"
        return self.func(*args)
    def depth(self):
        return 1

class Composition:
    def __init__(self,operator, args_list):
        self.operator = operator
        self.args = args_list

    def __call__(self):
        reargs =[i() for i in self.args]
        return self.operator(*reargs)

    def __str__(self):
        if len(self.args) == 2:
            return '('+str(self.args[0])+' '+str(self.operator)+' '+str(self.args[1])+')'
        elif len(self.args)  == 1:
            return '('+str(self.operator)+' '+str(self.args[0])+')'
        else:
            return str(self.operator)

    def depth(self):
        if self.args:
            return max([i.depth() for i in self.args])+1
        else:
            return 1


    def sdnf(self):
        list_of_variables = self.list_of_variables()
        print(list_of_variables)
        print(self)

        for var in product('10',repeat=len(list_of_variables)):
            dick = dict(zip(list_of_variables, [bool(int(i)) for i in var]))
            global Variable_list_of_means
            Variable_list_of_means = dick
            c = list(dick.values())
            c.append(self())
            print(c)
        return list_of_variables
    def list_of_variables(self):
        add = []
        for i in self.args:
            if type(i) == type(Variable('')):
                add.append(i.const_name)
            else:
                add.extend(i.list_of_variables())
        return list(set(add))

    def prednf(self):
        for i in range(len(self.args)):
            self.args[i] = self.args[i].prednf()
        return self.operator.prednf(*self.args)
    def first_iter(self):
        if str(self.operator)=='not':
            if str(self.args[0].operator) == 'or':
                self.operator == And()
                self.args = [Composition(Not(),[self.args[0].args[0]]),Composition(Not(),[self.args[0].args[1]])]
        if str(self.operator)=='or':
            if str(self.args[0].operator) == 'not' and str(self.args[1].operator) == 'not':
                self.operator = And()
                self.args = [self.args[0].args[0],self.args[1].args[0]]
        for arg in self.args:
            arg.first_iter()

    def todnf(self):
        self = self.prednf()
        for i in range(self.depth()*5):
            self.first_iter()
        return self


class Variable(Operator):
    def __init__(self,const_name):
        self.const_name = const_name
        Operator.__init__(self,lambda: Variable_list_of_means[const_name],0)
    def __str__(self):
        return '('+self.const_name+')'

    def prednf(self,*args):
        return Composition(Variable(self.const_name),[])
    def list_of_variables(self):
        return [self.const_name]


class Constant(Operator):
    def __init__(self,boolean):
        self.boolean = boolean
        Operator.__init__(self,lambda : boolean,0)

    def __str__(self):
        return str(int(self.boolean))

    def prednf(self,*args):
        return Composition(Constant(self.boolean),[])
    def list_of_variables(self):
        return []

class And(Operator):
    def __init__(self):
        Operator.__init__(self,lambda x,y: x and y, 2)

    def __str__(self):
        return 'and'

    def prednf(self,*args):
        return Composition(self,args)





class Not(Operator):
    def __init__(self):
        Operator.__init__(self,lambda x: not x, 1)

    def __str__(self):
        return 'not'

    def prednf(self,*args):
        return Composition(self,args)


class Or(Operator):
    def __init__(self):
        Operator.__init__(self,lambda x,y: x or y, 2)
    
    def __str__(self):
        return 'or'

    def prednf(self,*args):
        return Composition(self,args)


class Xor(Operator):
    def __init__(self):
        Operator.__init__(self,lambda x,y:not x == y, 2)

    def __str__(self):
        return 'xor'

    def prednf(self,*args):
        return Composition(Or(),[Composition(And(),[args[0],Composition(Not(),[args[1]])]),Composition(And(),[args[1],Composition(Not(),[args[0]])])])

class Eq(Operator):
    def __init__(self):
        Operator.__init__(self,lambda x,y: x == y, 2)

    def __str__(self):
        return 'eq'

    def prednf(self,*args):
        return Composition(Or(),[Composition(And(),[args[0],args[1]]),Composition(And(),[Composition(Not(),[args[1]]),Composition(Not(),[args[0]])])])


class Impl(Operator):
    def __init__(self):
        Operator.__init__(self,lambda x, y: x <= y, 2)

    def __str__(self):
        return 'impl'

    def prednf(self,*args):
        return Composition(Or(),[args[1],Composition(Not(),[args[0]])])



class Nand(Operator):
    def __init__(self):
        Operator.__init__(self,lambda x , y: not x and y, 2)

    def __str__(self):
        return 'nand'

    def prednf(self,*args):
        return Composition(Or(),[Composition(Not(),[args[1]]),Composition(Not(),[args[0]])])


class Nor(Operator):
    def __init__(self):
        Operator.__init__(self,lambda x ,y: not x or y, 2)

    def __str__(self):
        return 'nor'

    def prednf(self):
        return Composition(And(),[Composition(Not(),[args[1]]),Composition(Not(),[args[0]])])




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
    is_in_brackets = 2
    balance = 0
    for (index, char) in enumerate(line):
        if balance == 0 and index > 0:
            is_in_brackets = 1
            break 
        if (char == '('):
            balance += 1
        if (char == ')'):
            balance -= 1

    if is_in_brackets == 2 and line[0]=='(' and line[-1]==')':
        is_in_brackets = 0

    assert balance == 0, "Wrong bracket balance"

    if is_in_brackets==0:
        return parser_copy(line[1:-1])

    prior_operator, prior_start = None, None
    balance = 0
    part = line
    for start in range(len(line)):
        if line[start] == '(':
            balance += 1
        if line[start] == ')':
            balance -= 1
        if balance == 0:
            for name in priorities.keys():
                if part.startswith(name):
                    if not prior_operator or priorities[name] >= priorities[prior_operator]:
                        prior_operator, prior_start = name, start
        part = part[1:]

    if prior_operator is not None:
        if prior_start == 0:
            return Composition(Not(), [parser_copy(line[3:])])
        return Composition(
            FuncType[prior_operator](),
            [parser_copy(line[:prior_start]),parser_copy(line[prior_start + len(prior_operator):])]
            )

    if line in ['1','0']:
        return Constant(bool(int(line)))
    return Variable(line)
    


Variable_list_of_means = {'a':False,
                          'b':True}



print(parser_copy(input()).sdnf())

from logic import *

"""
[문제 01]: 각각 주어진 sentence를 Propositional logic으로 변경한 것을 return 하시오.(10점)
HINT: sentences.py 내의 rainWet()을 참고할 것.
"""
X = '$x'
Y = '$y'
Z = '$z'
## Sentence 01: "If it's summer and we're in California, then it doesn't rain."
def logic01_01():
    # Predicates to use:
    Summer = Atom('Summer')               # whether it's summer
    California = Atom('California')       # whether we're in California
    Rain = Atom('Rain')                   # whether it's raining
    ################# Write Your Code Here #########################
    SummerAndCalifornia = And(Summer, California)
    NotRain = Not(Rain)
    # (Summer ^ California) -> ¬ Rain
    return Implies(SummerAndCalifornia, NotRain)
    ################################################################

## Sentence 02: "It's wet if and only if it is raining or the sprinklers are on."
def logic01_02():
    # Predicates to use:
    Rain = Atom('Rain')              # whether it is raining
    Wet = Atom('Wet')                # whether it it wet
    Sprinklers = Atom('Sprinklers')  # whether the sprinklers are on
    ################# Write Your Code Here #########################
    # (Rain v Sprinklers) <-> Wet 
    return Equiv(Or(Rain,Sprinklers),Wet)
    ################################################################

## Sentence 03: "Either it's day or night (but not both)."
def logic01_03():
    # Predicates to use:
    Day = Atom('Day')     # whether it's day
    Night = Atom('Night') # whether it's night
    ################# Write Your Code Here #########################
    # Day ⊕ Night
    return Xor(Day, Night)
    ################################################################

"""
[문제 02]: 각각 주어진 sentence를 First-order logic으로 변경한 것을 return 하시오.(15점)
02-01 HINT: Mother를 "person"이라고 강요할 필요는 없다. 
02-02 HINT: Child를 "person"이라고 강요할 필요는 없다.
02-03 HINT: sentences.py 내의 parentChild()을 참고할 것
02-04 HINT: It is ok for a person to be her own parent.
"""

## Sentence 01: "Every person has a mother."
def logic02_01():
    # Predicates to use:
    def Person(x): return Atom('Person', x)        # whether x is a person
    def Mother(x, y): return Atom('Mother', x, y)  # whether x's mother is y

    ################# Write Your Code Here #########################
    # ∀x∃y(Person(x)->Mother(x,y))
    def HasMother(x,y): return Implies(Person(x),Mother(x,y))
    return Forall(X,Exists(Y,HasMother(X,Y)))
    ################################################################

## Sentence 02: "At least one person has no children."
def logic02_02():
    # Predicates to use:
    def Person(x): return Atom('Person', x)        # whether x is a person
    def Child(x, y): return Atom('Child', x, y)    # whether x has a child y

    ################# Write Your Code Here #########################
    # ∃x∀y¬(Person(x)->Child(x,y))
    return Exists(X,Forall(Y,Not(Implies(Person(X),Child(X,Y)))))
    ################################################################

## Return a formula which defines Daughter in terms of Female and Child.
def logic02_03():
    # Predicates to use:
    def Female(x): return Atom('Female', x)            # whether x is female
    def Child(x, y): return Atom('Child', x, y)        # whether x has a child y
    def Daughter(x, y): return Atom('Daughter', x, y)  # whether x has a daughter y
    ################# Write Your Code Here #########################
    # ∀x∀y(Daughter(x,y) <-> (Child(x,y) ^ Female(y)))
    def DaughterIffFemaleAndChild(x,y) : return Equiv(And(Child(x,y),Female(y)),Daughter(x,y))
    return Forall(X,Forall(Y,DaughterIffFemaleAndChild(X,Y)))
    ################################################################

## Return a formula which defines Grandmother in terms of Female and Parent.
def logic02_04():
    # Predicates to use:
    def Female(x): return Atom('Female', x)                  # whether x is female
    def Parent(x, y): return Atom('Parent', x, y)            # whether x has a parent y
    def Grandmother(x, y): return Atom('Grandmother', x, y)  # whether x has a grandmother y
    ################# Write Your Code Here #########################
    # ∀x∀yGrandmother(x,y) <-> Female(y) and ∃z(Parent(x,z) and Parent(z,y))
    def GrandmotherEquiv(X,Y,Z) : return And(Female(Y),Exists(Z,And(Parent(X,Z),Parent(Z,Y))))
    return Forall(X,Forall(Y,Equiv(Grandmother(X,Y),GrandmotherEquiv(X,Y,Z))))
    ################################################################


"""
[문제 03]: 문제 설명 파일에서 설명한 4개의 증언과 2개의 사실을 First-Order Logic으로 변경하여,차례대로 formula 리스트에 추가하시오.(25점)
HINT01: logic.py에서 정의된 Equals predicate를 사용할 수 있다. 참고로 Equals predicate는 두 개의 object가 같다고 주장할때 사용된다.
"""

def suspect():
    def TellTruth(x): return Atom('TellTruth', x)
    def CrashedServer(x): return Atom('CrashedServer', x)
    john = Constant('john')
    susan = Constant('susan')
    nicole = Constant('nicole')
    mark = Constant('mark')
    formulas = []
    ## HINT02: 첫번째 증언 구현 예시 John: "it wasn't me!"
    formulas.append(Equiv(TellTruth(john), Not(CrashedServer(john))))
    """
    증언 (1)을 제외한 (2),(3),(4),(5),(6)을 구현하시오.
    """
    ################# Write Your Code Here #########################
    formulas.append(Equiv(TellTruth(susan),CrashedServer(nicole)))
    formulas.append(Equiv(TellTruth(mark),CrashedServer(susan)))
    formulas.append(Equiv(TellTruth(nicole),Not(TellTruth(susan))))
    
    # ∃!xP(x) <-> ∃x∀y(P(y)<->x=y)
    def ExactlyOne(P): return Exists(X,Forall(Y,Equiv(P(Y),Equals(X,Y))))

    # ∃!x(TellTruth(x))
    formulas.append(ExactlyOne(TellTruth))

    # ∃!x(CrashedServer(x))
    formulas.append(ExactlyOne(CrashedServer))
    ################################################################
    # Query: Who did it?
    query = CrashedServer('$x')
    return (formulas, query)


"""
[문제 04]: 문제 설명 파일에서 설명한 6개의 theorem을 First-Order Logic으로 변경하여,차례대로 formula 리스트에 추가하시오.(30점)
HINT01: logic.py에서 정의된 Equals predicate를 사용할 수 있다. 참고로 Equals predicate는 두 개의 object가 같다고 주장할때 사용된다.
HINT02: 모든 object는 숫자이므로 숫자를 predicate로 정의할 필요가 없다. 
"""

def number_theorem():
    def Even(x): return Atom('Even', x)                  # whether x is even
    def Odd(x): return Atom('Odd', x)                    # whether x is odd
    def Successor(x, y): return Atom('Successor', x, y)  # whether x's successor is y
    def Larger(x, y): return Atom('Larger', x, y)        # whether x is larger than y

    formulas = []
    query = None
    ################# Write Your Code Here #########################
    # ∀x∃y(∀z(Successor(x,z)<->(z==y)) ^ ¬(x==y)))
    def ExactlyOne(P): return Forall(Z,Equiv(P(X,Z),Equals(Z,Y)))
    formulas.append(Forall(X,Exists(Y,And(ExactlyOne(Successor),Not(Equals(X,Y))))))

    # ∀x(Even(x) ⊕ Odd(x))
    formulas.append(Forall(X,Xor(Even(X),Odd(X))))

    # ∀x∀y(Even(x)->(Successor(x,y)->Odd(y)))
    formulas.append(Forall(X,Forall(Y,Implies(Even(X),Implies(Successor(X,Y),Odd(Y))))))
    
    # ∀x∀y(Odd(x)->(Successor(x,y)->Even(y)))
    formulas.append(Forall(X,Forall(Y,Implies(Odd(X),Implies(Successor(X,Y),Even(Y))))))

    # ∀x∀y(Successor(x,y)->Larger(y,x))
    formulas.append(Forall(X,Forall(Y,Implies(Successor(X,Y),Larger(Y,X)))))
    
    # ∀x∀y∀z(L(x,y)^L(y,z) -> L(x,z))
    formulas.append(Forall(X,Forall(Y,Forall(Z,Implies(And(Larger(X,Y),Larger(Y,Z)),Larger(X,Z))))))

    ################################################################
    # Query: For each number, there exists an even number larger than it.
    query = Forall('$x', Exists('$y', And(Even('$y'), Larger('$y', '$x'))))
    return (formulas, query)


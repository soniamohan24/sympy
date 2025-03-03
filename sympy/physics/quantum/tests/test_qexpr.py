from sympy.core.numbers import Integer
from sympy.core.symbol import Symbol
from sympy.concrete import Sum
from sympy.physics.quantum.qexpr import QExpr, _qsympify_sequence
from sympy.physics.quantum.hilbert import HilbertSpace
from sympy.core.containers import Tuple

x = Symbol('x')
y = Symbol('y')
n = Symbol('n', integer=True)
m = Symbol('m', integer=True)


def test_qexpr_new():
    q = QExpr(0)
    assert q.label == (0,)
    assert q.hilbert_space == HilbertSpace()
    assert q.is_commutative is False

    q = QExpr(0, 1)
    assert q.label == (Integer(0), Integer(1))

    q = QExpr._new_rawargs(HilbertSpace(), Integer(0), Integer(1))
    assert q.label == (Integer(0), Integer(1))
    assert q.hilbert_space == HilbertSpace()


def test_qexpr_commutative():
    q1 = QExpr(x)
    q2 = QExpr(y)
    assert q1.is_commutative is False
    assert q2.is_commutative is False
    assert q1*q2 != q2*q1

    q = QExpr._new_rawargs(Integer(0), Integer(1), HilbertSpace())
    assert q.is_commutative is False


def test_qexpr_free_symbols():
    q1 = QExpr(x, y)
    assert q1.free_symbols == {x, y}


def test_qexpr_sum():
    q1 = Sum(QExpr(n), (n,0,2))
    assert q1.doit() == QExpr(0) + QExpr(1) + QExpr(2)

    q2 = Sum(QExpr(n, m), (n, 0, 2), (m, 0, 2))
    assert q2.doit() == QExpr(0, 0) + QExpr(0, 1) + QExpr(0, 2) + \
        QExpr(1, 0) + QExpr(1, 1) + QExpr(1, 2) + \
        QExpr(2, 0) + QExpr(2, 1) + QExpr(2, 2)


def test_qexpr_subs():
    q1 = QExpr(x, y)
    assert q1.subs(x, y) == QExpr(y, y)
    assert q1.subs({x: 1, y: 2}) == QExpr(1, 2)


def test_qsympify():
    assert _qsympify_sequence([[1, 2], [1, 3]]) == (Tuple(1, 2), Tuple(1, 3))
    assert _qsympify_sequence(([1, 2, [3, 4, [2, ]], 1], 3)) == \
        (Tuple(1, 2, Tuple(3, 4, Tuple(2,)), 1), 3)
    assert _qsympify_sequence((1,)) == (1,)

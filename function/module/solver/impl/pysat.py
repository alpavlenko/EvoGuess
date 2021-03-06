import numpy as np

from ..solver import *

from pysat import solvers
from threading import Timer
from time import time as now

saved_stats = {}
saved_solvers = {}


class PySat(Solver):
    constructor = None
    slug = 'solver:pysat'
    name = 'Solver: PySat'

    def solve(self, clauses, assumptions, limit=0, key=None):
        solver = self.constructor(bootstrap_with=clauses, use_timer=True)

        if limit > 0:
            timer = Timer(limit, solver.interrupt, ())
            timer.start()

            timestamp = now()
            status = solver.solve_limited(assumptions=assumptions, expect_interrupt=True)
            full_time, time = now() - timestamp, solver.time()

            if timer.is_alive():
                timer.cancel()
            else:
                solver.clear_interrupt()
        else:
            timestamp = now()
            status = solver.solve(assumptions=assumptions)
            full_time, time = now() - timestamp, solver.time()

        solution = solver.get_model() if status else None
        statistics = solver.accum_stats()
        statistics['time'] = time
        solver.delete()

        return status, statistics, solution


#
# ----------------------------------------------------------------
#


class Cadical(PySat):
    slug = 'solver:pysat:cd'
    name = 'Solver: Cadical'
    constructor = solvers.Cadical


class Glucose3(PySat):
    slug = 'solver:pysat:g3'
    name = 'Solver: Glucose3'
    constructor = solvers.Glucose3


class Glucose4(PySat):
    slug = 'solver:pysat:g4'
    name = 'Solver: Glucose4'
    constructor = solvers.Glucose4


class Lingeling(PySat):
    slug = 'solver:pysat:lgl'
    name = 'Solver: Lingeling'
    constructor = solvers.Lingeling


class MapleChrono(PySat):
    slug = 'solver:pysat:mcb'
    name = 'Solver: MapleChrono'
    constructor = solvers.MapleChrono


class MapleCM(PySat):
    slug = 'solver:pysat:mcm'
    name = 'Solver: MapleCM'
    constructor = solvers.MapleCM


class MapleSAT(PySat):
    slug = 'solver:pysat:mpl'
    name = 'Solver: MapleSAT'
    constructor = solvers.Maplesat


class Minicard(PySat):
    slug = 'solver:pysat:mc'
    name = 'Solver: Minicard'
    constructor = solvers.Minicard


class Minisat22(PySat):
    slug = 'solver:pysat:m22'
    name = 'Solver: Minisat22'
    constructor = solvers.Minisat22


class MinisatGH(PySat):
    slug = 'solver:pysat:mgh'
    name = 'Solver: MinisatGH'
    constructor = solvers.MinisatGH


__all__ = [
    'Cadical',
    'Glucose3',
    'Glucose4',
    'Lingeling',
    'MapleChrono',
    'MapleCM',
    'MapleSAT',
    'Minicard',
    'Minisat22',
    'MinisatGH'
]

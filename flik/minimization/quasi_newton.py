# An experimental local optimization package
# Copyright (C) 2018 Ayers Lab <ayers@mcmaster.ca>.
#
# This file is part of Flik.
#
# Flik is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# Flik is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>


# API: method_name_B(B, secant, step): -> new_B
# or method_name_H(H, secant, step): -> new_H
# testfilename should be test_method_name.py in minimization/test


from numbers import Integral
from numbers import Real
import numpy as np

CONV = 10E-06
NUM_ITERS = 100

def quasi_newtons_opt(function, gradient, hessian, val, update=None,
                convergence=CONV, num_iterations=NUM_ITERS):
    """Quasi-Newton method for approximate hessians.

    Parameters
    ----------
    function : Callable
        The function for which the minimum will
        be computed.
        returns np.array((1))
    gradient: Callable
        The gradientient of the given function.
        (1st derivative)
        returns np.array((N,))
    hessian : Callable
        The approximation to hessian of the given function.
        (2nd derivative)
        returns np.array((N,N))
    val : numpy.ndarray((N,))
        An initial guess for the function's
        minimum value.
    update : Callable
        Hessian approximation method.
        If none just newtons method.
        returns np.array((N,N))
    convergence : float
        The condition for convergence (acceptable
        error margin from zero for the returned
        minimum).
    num_iterations : int
        The maximum number of iterations to do
        in order to reach convergence.

    """
    #TODO: correct docs

    # Check input
    if not callable(function):
        raise TypeError('Fucntion should be callable')
    if not callable(gradient):
        raise TypeError('gradientient should be callable')
    if not callable(hessian):
        raise TypeError('gradientient should be callable')
    #if not (isinstance(val, np.ndarray) and val.ndim == 1):
    #    raise TypeError("Argument val should be a 1-dimensional numpy array")
    if not isinstance(convergence, Real):
        raise TypeError("Argument convergence should be a real number")
    if not isinstance(num_iterations, Integral):
        raise TypeError("Argument num_iterations should be an integer number")
    if convergence < 0.0:
        raise ValueError("Argument convergence should be >= 0.0")
    if num_iterations <= 0:
        raise ValueError("Argument num_iterations should be >= 1")

    # choose initial guess and non-singular hessian approximation
    point = val
    hess = hessian(point)

    # non-optimized step length
    step_length = 1

    for i in range(1, num_iterations+1):
        if not update:
            hess = hessian(point)
        
        if len(point) > 1:
            step_direction = -gradient(point).dot(
                    np.linalg.inv(hess))
        else:
            step_direction = -np.dot(gradient(point), 1/hess)

        # new x
        point1 = point + step_length * step_direction
        # new hessian callable
        if update:
            hess = update(hess, gradient, point, point1)
        # update x
        point = point1
        # stop when minimum
        if np.allclose(gradient(point), 0, atol=convergence):
            return function(point), point, gradient(point), i

def update_hessian_bfgs(hessian, gradient, pointk, pointkp1):
    """BFGs update for quasi-newton.
    
    Equation 6.19 from numerical optimisation book.
    """
    sk = pointkp1 - pointk
    yk = gradient(pointk) - gradient(pointk)
    newhess = hessian
    # part one
    one = np.dot(np.dot(np.dot(sk, sk.T), newhess), newhess)
    one /= np.dot(np.dot(sk.T,newhess), sk)
    newhess -= one
    # part two
    newhess += np.dot(yk, yk.T)/np.dot(yk.T, sk)
    return newhess

def update_hessian_broyden(hessian, gradient, point, point1):
    """
    Approximate Hessian with new x
    Good Broyden style

    Parameters
    ----------
    hessian : np.ndarray((N,N))
    gradient : Callable
    point : np.array((N,))
    point1 : np.array((N,))
    
    Returns
    -------
    hessian : np.ndarray((N,N))
    """
    sk = point1 - point
    yk = gradient(point1) - gradient(point)
    yk -= np.dot(hessian, sk)
    yk /= np.dot(sk, sk)
    hessian += np.outer(yk, sk.T)
    return hessian


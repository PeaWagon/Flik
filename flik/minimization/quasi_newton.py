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


def quasi_newtons_opt(function, gradient, approx_hessian, val,
                convergence=CONV, num_iterations=NUM_ITERS):
    """Quasi-Newton method for approximate hessians.

    Parameters
    ----------
    function : Callable
        The function for which the minimum will
        be computed.
    gradient : Callable
        The gradient of the given function.
        (1st derivative)
    approx_hessian : Callable
        The approximation to hessian of the given function.
        (2nd derivative)
    val : numpy.ndarray
        An initial guess for the function's
        minimum value.
    convergence : float
        The condition for convergence (acceptable
        error margin from zero for the returned
        minimum).
    num_iterations : int
        The maximum number of iterations to do
        in order to reach convergence.

    """
    # Check input
    if not callable(function):
        raise TypeError('Fucntion should be callable')
    if not callable(gradient):
        raise TypeError('Gradient should be callable')
    if not (isinstance(val, np.ndarray) and val.ndim == 1):
        raise TypeError("Argument val should be a 1-dimensional numpy array")
    if not isinstance(onvergence, Real):
        raise TypeError("Argument convergence should be a real number")
    if not isinstance(num_iterations, Integral):
        raise TypeError("Argument num_iterations should be an integer number")
    if convergence < 0.0:
        raise ValueError("Argument convergence should be >= 0.0")
    if num_iterations <= 0:
        raise ValueError("Argument num_iterations should be >= 1")

    # choose initial guess and non-singular hessian approximation
    min_point = val
    hessian = approx_hessian()
    # non-optimized step length
    step_length = 0.5

    for i in range(1, num_iterations+1):
        if len(initial_point) > 1:
            direction =  -np.dot(gradient(min_point), np.linalg.inv(hessian))
        else:
            direction =  -np.dot(gradient(min_point), 1/hessian)

        # update x
        new_min_point = min_point + step_length * direction
        #TODO: find a way to update hessian


        # stop when minimum
        if np.allclose(gradient(min_point), 0, atol=convergence):
            return function(min_point), min_point, gradient(min_point), i

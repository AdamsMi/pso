import pso
import de
import config
import problem
from problem import StoppingCriterion
from copy import copy


def minimize(obj_function, method,
             population_size=config.population_size,
             stopping_criterion=StoppingCriterion.default(),
             interval=(config.coord_min, config.coord_max),
             params=None):
    """
    Minimize the given function.
    Minimization uses metaheuristics like Particle Swarm Optimization and Differential Evolution,
    utilizing swarm intelligence to come up with a (nearly) optimal solution.
    :param obj_function: Function to minimize. This has to be an instance of `problem.ObjFunc`.
    :param method: Method to use during optimization. Right now this can be either PSO or DE.
    :param population_size: Size of the population to use for the algorithm.
    :param stopping_criterion: Stopping criterion for the algorithm,
    this has to be an instance of `problem.StoppingCriterion`.
    :param interval: interval on which the function should be optimized will be a square:
    interval^dim (^ meaning the power using cartesian product).
    :param params: method-specific parameters in form of a dictionary.
    See the documentation for `de.run_de` and `pso.run_pso` for more detailed explanation.
    :return: Depending on the stopping criterion this can be either the best solution achieved by the method
    or number of steps required to get to this solution.
    """
    if method == 'pso':
        return pso.run_pso(fit_func=obj_function.func,
                           dimensionality=obj_function.dim,
                           population_size=population_size,
                           interval=interval,
                           stopping_criterion=stopping_criterion,
                           method_params=params,
                           chart=False)

    if method == 'de':
        return de.run_de(fit_func=obj_function.func,
                         dimensionality=obj_function.dim,
                         population_size=population_size,
                         interval=interval,
                         stopping_criterion=stopping_criterion,
                         method_params=params,
                         chart=False)

    print 'Method "{0}" currently not supported, sorry.'.format(method)


def maximize(obj_function, method,
             population_size=config.population_size,
             stopping_criterion=StoppingCriterion.default(),
             interval=(config.coord_min, config.coord_max),
             params=None):
    """
        Maximize the given function.
        Maximization is actually implemented as a minimalization of the objective function
        with its sign reversed, so it uses exactly the same methods.
        :param obj_function: Function to minimize. This has to be an instance of `problem.ObjFunc`.
        :param method: Method to use during optimization. Right now this can be either PSO or DE.
        :param population_size: Size of the population to use for the algorithm.
        :param stopping_criterion: Stopping criterion for the algorithm,
        this has to be an instance of `problem.StoppingCriterion`.
        :param interval: interval on which the function should be optimized will be a square:
        interval^dim (^ meaning the power using cartesian product).
        :param params: method-specific parameters in form of a dictionary.
        See the documentation for `de.run_de` and `pso.run_pso` for more detailed explanation.
        :return: Depending on the stopping criterion this can be either the best solution achieved by the method
        or number of steps required to get to this solution.
        """
    obj_function_rev = problem.reverse_sign(obj_function)
    return minimize(obj_function_rev, method, population_size, stopping_criterion, interval, params)

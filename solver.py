import pso
import de
import config
import problem


def minimize(obj_function, method,
             population_size=config.population_size,
             nr_steps=config.nr_steps,
             interval=(config.coord_min, config.coord_max),
             params=None):
    if method == 'pso':
        return pso.run_pso(fit_func=obj_function.func,
                           dimensionality=obj_function.dim,
                           population_size=population_size,
                           interval=interval,
                           nr_steps=nr_steps,
                           method_params=params,
                           chart=False)

    if method == 'de':
        return de.run_de(fit_func=obj_function.func,
                         dimensionality=obj_function.dim,
                         population_size=population_size,
                         interval=interval,
                         nr_steps=nr_steps,
                         method_params=params,
                         chart=False)

    print 'Method "{0}" currently not supported, sorry.'.format(method)


def maximize(obj_function, method,
             population_size=config.population_size,
             nr_steps=config.nr_steps,
             interval=(config.coord_min, config.coord_max),
             params=None):
    obj_function_rev = problem.reverse_sign(obj_function)
    return minimize(obj_function_rev, method, population_size, nr_steps, interval, params)
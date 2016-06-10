import solver
import problem
import matplotlib.pyplot as plt
import de, pso

obj_func = problem.ObjFunc(10, problem.rastrigin_func)
pop_size = 50

pso_params = {'inertia': 0.7, 'cognitive': 1.5, 'social': 1.5}


def iterations_test(start=700, end=1500, step=10, smoothing=3):
    """
    Test runs the solver using each method for a given number of steps repeatedly,
    as indicated by the start, end and step parameters
    :param start: Smallest number of iterations to test
    :param end: Highest number of iterations to test
    :param step: Increment of iteration count
    :param smoothing: the number of runs with identical parameters,
    from which a simple mean is taken as a result
    :return: None, the method draws charts as its result
    """
    global obj_func, pop_size

    iter_counts = range(start, end, step)
    results_pso = []
    results_de = []
    for iterations in iter_counts:
        result_pso = 0
        result_de = 0

        stopping_criterion = problem.StoppingCriterion('nr_steps', iterations)

        for i in xrange(smoothing):
            result_pso += obj_func.func(solver.minimize(obj_func,
                                                        method='pso',
                                                        stopping_criterion=stopping_criterion,
                                                        population_size=pop_size))

            result_de += obj_func.func(solver.minimize(obj_func,
                                                       method='de',
                                                       stopping_criterion=stopping_criterion,
                                                       population_size=pop_size))
        result_pso /= float(smoothing)
        result_de /= float(smoothing)

        results_pso.append(result_pso)
        results_de.append(result_de)

    # scale iter counts:
    iter_counts = [pop_size * ic for ic in iter_counts]

    plt.plot(iter_counts, results_pso, 'bo-', label='pso')
    plt.plot(iter_counts, results_de, 'r^-', label='de')
    plt.legend()
    plt.title('Comparison of pso and de methods using a fixed amount of iterations.')
    plt.xlabel('Iteration counts')
    plt.ylabel('Best fitness acheived.')
    plt.show()


def target_fit_test(fitnesses, smoothing=3):
    """
    Test runs the solver for each method until it reaches a target fitness. Repeated for all fitnesses.
    :param fitnesses: Sequence of target fitnesses for the solvers
    :param smoothing: the number of runs with identical parameters,
    from which a simple mean is taken as a result
    :return: None, the method draws charts as its result
    """
    global obj_func, pop_size

    results_pso = []
    results_de = []
    for fitness in fitnesses:
        print "Fitness: ", fitness

        result_pso = 0
        result_de = 0

        stopping_criterion = problem.StoppingCriterion('target_fitness', fitness)

        for i in xrange(smoothing):
            result_pso += solver.minimize(obj_func, method='pso',
                                          stopping_criterion=stopping_criterion,
                                          population_size=pop_size, params=pso_params)

            result_de += solver.minimize(obj_func, method='de',
                                         stopping_criterion=stopping_criterion,
                                         population_size=pop_size)

            print "Calculated de"

        result_pso /= float(smoothing)
        result_de /= float(smoothing)

        results_pso.append(result_pso)
        results_de.append(result_de)

    plt.plot(fitnesses, results_pso, 'bo-', label='pso')
    plt.plot(fitnesses, results_de, 'r^-', label='de')
    plt.gca().invert_xaxis()
    plt.legend()
    plt.title('Comparison of pso and de methods using a target fitness')
    plt.xlabel('Target fitness')
    plt.ylabel('Iterations required to acheive that fitness')
    plt.show()


DE = {'CR': 0.75, 'F': 0.3}
PSO = {'cognitive': 1.2, 'inertia': 0.53, 'social': 1.2}

if __name__ == '__main__':
    print "Iterations test..."
    iterations_test(250, 500, 5, 3)

    print "Target fitness test"
    fits = [100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10]
    target_fit_test(fits)

    print "Fitting DE params:"
    print de.param_fit(obj_func)
    print 'Fitting PSO params:'
    print pso.param_fit(obj_func)

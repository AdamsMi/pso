import solver
import problem
import matplotlib.pyplot as plt

obj_func = problem.ObjFunc(3, problem.rastrigin_func)


def iterations_test(start=100, end=1000, step=10, smoothing=1):
    global obj_func

    iter_counts = range(start, end, step)
    results_pso = []
    results_de = []
    for iterations in iter_counts:
        result_pso = 0
        result_de = 0
        for i in xrange(smoothing):
            result_pso += obj_func.func(solver.minimize(obj_func, method='pso', nr_steps=iterations))
            result_de += obj_func.func(solver.minimize(obj_func, method='de', nr_steps=iterations))
        result_pso /= float(smoothing)
        result_de /= float(smoothing)

        results_pso.append(result_pso)
        results_de.append(result_de)

    plt.plot(iter_counts, results_pso, label='pso')
    plt.plot(iter_counts, results_de, label='de')
    plt.legend()
    plt.title('Comparison of pso and de methods using a fixed amount of iterations.')
    plt.xlabel('Iteration counts')
    plt.ylabel('Best fitness acheived.')
    plt.show()


print "Iterations test..."
iterations_test(100, 1000, 10, 2)

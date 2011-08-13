def worker_function(originalFunction):
    def decorated():

        originalFunction()

    return decorated
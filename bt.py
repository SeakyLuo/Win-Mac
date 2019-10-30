def getSolution(target):
    options = list(filter(lambda n: n <= target, reversed([6, 68, 88, 208, 388, 998])))
    solutions = []
    d = { opt: 0 for opt in options }
    def recursive(Sum, opts):
        for i, num in enumerate(opts):
            d[num] += 1
            if Sum + num >= target:
                solutions.append(d.copy())
            else:
                recursive(Sum + num, opts[i:])
            d[num] -= 1

    recursive(0, options)
    cost = lambda d: sum(k * v for k, v in d.items())
    print(solution := min(solutions, key=lambda d: (cost(d), sum(d.values()))))
    print(cost(solution))

getSolution(189)

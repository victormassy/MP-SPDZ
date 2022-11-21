def batcherSort(a, sorted_length=1, n_parallel=32,
                              n_threads=None):
    steps = {}
    l = sorted_length
    while l < len(a):
        l *= 2
        k = 1
        while k < l:
            k *= 2
            n_innermost = 1 if k == 2 else k // 2 - 1
            key = k
            if key not in steps:
                @function_block
                def step(l):
                    l = MemValue(l)
                    m = 2 ** int(math.ceil(math.log(len(a), 2)))
                    @for_range_opt_multithread(n_threads, m // k)
                    def _(i):
                        n_inner = l // k
                        j = i % n_inner
                        i //= n_inner
                        base = i*l + j
                        step = l//k
                        def swap(base, step):
                            if m == len(a):
                                a[base], a[base + step] = \
                                    cond_swap(a[base], a[base + step])
                            else:
                                # ignore values outside range
                                go = base + step < len(a)
                                x = a.maybe_get(go, base)
                                y = a.maybe_get(go, base + step)
                                tmp = cond_swap(x, y)
                                for i, idx in enumerate((base, base + step)):
                                    a.maybe_set(go, idx, tmp[i])
                        if k == 2:
                            swap(base, step)
                        else:
                            @for_range_opt(n_innermost)
                            def f(i):
                                m1 = step + i * 2 * step
                                m2 = m1 + base
                                swap(m2, step)
                steps[key] = step
            steps[key](l)

from Compiler.library import *
from Compiler.types import *


def outputSwap(base, step, output):
    print_ln('swap %s %s', base, base+step.reveal())
    temp = output[base]
    output[base] = output[base+step.reveal()]
    output[base+step.reveal()] = temp
    output.print_reveal_nested()

def batcherSort(a, sorted_length=1, n_parallel=32,
                 n_threads=None):
    output = Array(len(a), sint)
    for i in range(len(a)):
            output[i] = i
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
                            temp = a[base]
                            swap(base, step)
                            break_point()
                            swapHappened = (a[base] != temp)
                            print_ln('swap happened %s', swapHappened.reveal())
                            outputSwap(base, step*swapHappened, output)
                            a.print_reveal_nested()
                        else:
                            @for_range_opt(n_innermost)
                            def f(i):
                                m1 = step + i * 2 * step
                                m2 = m1 + base
                                temp = a[m2]
                                swap(m2, step)
                                break_point()
                                swapHappened = (a[m2] != temp)
                                print_ln('swap happened %s', swapHappened.reveal())
                                outputSwap(base, step*swapHappened, output)
                                a.print_reveal_nested()
                steps[key] = step
            steps[key](l)
    return output.get_reverse_vector()

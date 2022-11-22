from Compiler.library import *
from Compiler.types import *


def output_swap(base, step,swapHappened, output):
    #print_ln('swap %s %s %s %s %s %s ',swapHappened.reveal(), base, base+step.reveal(), base * swapHappened.reveal(),(base+step.reveal()) * swapHappened.reveal(),(base+step.reveal()) * swapHappened.reveal())
    #swapHappened = swapHappened.if_else(0,1)
    temp = output[base * swapHappened.reveal()]
    output[base * swapHappened.reveal()] = output[(base+step.reveal()) * swapHappened.reveal()]
    output[(base+step.reveal()) * swapHappened.reveal()] = temp
    
    #output.print_reveal_nested()

def batcher_sort(a, sorted_length=1, n_parallel=32,
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
                                x = a[base]
                                tmp = cond_swap(a[base], a[base + step])
                                a[base], a[base + step] = \
                                    tmp
                                return x != tmp[0]
                            else:
                                #temp = a[base]
                                # ignore values outside range
                                go = base + step < len(a)
                                x = a.maybe_get(go, base)
                                y = a.maybe_get(go, base + step)
                                tmp = cond_swap(x, y)
                                for i, idx in enumerate((base, base + step)):
                                    a.maybe_set(go, idx, tmp[i]) 
                                return x != tmp[0]
                        if k == 2:
                            #newidx = (base < len(a)).if_else(base, 0)
                            #temp = a[newidx] 
                            swap_happened = swap(base, step)
                            #swapHappened = (a[newidx] != temp)
                            #print_ln('newidx %s', newidx.reveal())
                            #print_ln('swap happened %s', swapHappened.reveal())
                            output_swap(base, step, swap_happened, output)
                            #a.print_reveal_nested()
                        else:
                            @for_range_opt(n_innermost)
                            def f(i):
                                m1 = step + i * 2 * step
                                m2 = m1 + base
                                #newidx = (m2 < len(a)).if_else(m2, 0)
                                #temp = a[newidx]
                                swap_happened = swap(m2, step)
                                #swapHappened = (a[newidx] != temp)
                                #print_ln('newidx %s', newidx.reveal())
                                #print_ln('swap happened %s', swapHappened.reveal())
                                output_swap(m2, step, swap_happened, output)
                                #a.print_reveal_nested()
                steps[key] = step
            steps[key](l)
    return output



def batcher_sort_matrix(matrix,match_keys):
    permutation = batcher_sort(match_keys) 
    res = Matrix(len(match_keys), len(matrix[0]), sint)
    permutation.print_reveal_nested()
    for i in range(len(match_keys)):
        for j in range(len(matrix[0])):
            #print_ln('%s', permutation.reveal()[i])
            res[i][j] = matrix[permutation.reveal()[i]][j]
    return res
        


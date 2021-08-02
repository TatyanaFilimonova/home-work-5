import time
from multiprocessing import Pool, freeze_support, Queue, Process
import os

def f(number, queue):
    f_res = [1]
    for i in range(2,int(number/2)+1):
        if number % i == 0:
            f_res.append(i)
    f_res.append(number)
    queue.put({number:f_res})
    


def factorize_pool(number, queue):
    res_dict = {}    
    for n in number: res_dict[n] = []
    results = []
    for n in sorted(number, reverse = True):
        p = Process(target=f, args=(n, queue))
        results.append(p)
        p.start()
    for r in results:
             r.join()
    while not queue.empty():
        res = queue.get()
        res_dict[list(res.keys())[0]] = list(res.values())[0]
    res_lst = list(res_dict.values())
    return res_lst

def factorize(*number):
    res_lst = []
    for n in number:
        iter_lst = [1]
        for i in range(2,int(n/2)+1):
            if n % i == 0:
                iter_lst.append(i)
        iter_lst.append(n)
        res_lst.append(iter_lst)
    return res_lst

if __name__ == '__main__':
    queue = Queue()    
    freeze_support()    
    t = time.time()
    a, b, c, d  = factorize(123456780, 123456781, 123456782, 123456783)
    print("Factorize is done using one workflow in {:.3f} sec."
         .format(time.time() - t))
    print(d)
    t = time.time()
    n_workflow = 5
    a, b, c, d,  = factorize_pool((123456780, 123456781, 123456782,
                                   123456783), queue)
    print(d)
    print("Factorize is done using processes in {:.3f} sec."
             .format(time.time() - t))
    

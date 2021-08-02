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
    a, b, c, d, e  = factorize(128, 255, 99999, 10651060, 489848951)
    print("Factorize is done using one workflow in {:.3f} sec."
         .format(time.time() - t))
    

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 
                 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 
                 2662765, 5325530, 10651060]

    t = time.time()
    a, b, c, d, e  = factorize_pool((128, 255, 99999, 10651060, 489848951), queue)
    print("Factorize is done using 5 workflow in {:.3f} sec."
             .format(time.time() - t))
    
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 
                 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 
                 2662765, 5325530, 10651060]

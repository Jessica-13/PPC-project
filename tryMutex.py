#!/usr/bin/env python3

# MultiProcessing using Mutex example       


import time        
from multiprocessing import Process, Lock, Array, Value
           
          
def task(index, result): 
    result[index.value] = index.value ** 2
             
def run(n):   
          
    mutex = Lock()
    
    start = time.time()  
          
    result = Array('i', range(n), lock=mutex)
           
    for k in range(n):  
        value = Value('i', k)
        process = Process(
            target=task,
            args=(value, result)
          
        )
        
        process.start()
        process.join()       
          
    print(list(result))           
    print("Finished in: ", time.time() - start)


if __name__ == '__main__':
    
    run(10)
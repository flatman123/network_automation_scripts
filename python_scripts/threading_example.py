import time
import threading
import concurrent.futures

start = time.perf_counter()

def do_something(seconds):
    print(f'Sleeping 1 {seconds}...')
    time.sleep(seconds)
    return f'Done sleeping...{seconds}'

# t1 = threading.Thread(target=do_something)
# t2 = threading.Thread(target=do_something)
# t3 = threading.Thread(target=do_something)
# t4 = threading.Thread(target=do_something)


# t1.start()
# t2.start()
# t3.start()
# t4.start()
# The join method forces the script to wait for the threads
    # to finish before continuing with the rest of the script.
# t1.join()
# t2.join()
# t3.join()
# t4.join()

# using a loop

#with a list-comprehension
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     secs = [5,4,3,2,1]
#     results = [executor.submit(do_something, sec) for sec in secs]
#     for f in concurrent.futures.as_completed(results):
#         print(f.result())

#witih the map keyword
with concurrent.futures.ThreadPoolExecutor() as executor:
    secs = [2,4,6,8,10]
    results =  executor.map(do_something, secs)

#
# threads = []
# for _ in range(10):
#     th = threading.Thread(target=do_something, args=[1.5])
#     th.start()
#     threads.append(th)
#
# for thread in threads:
#     thread.join()
#


# here is the new way to of setting up threads.
    # its easier and more efficient its call a threadpool executer
finish = time.perf_counter()
print(f'Finished in {round(finish-start, 2)} seconds(s)')
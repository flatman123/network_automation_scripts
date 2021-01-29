import datetime
import paramiko
import threading
import time
import concurrent.futures

start_time = time.perf_counter()

def myFunction(t):
    print(f'RUNNING WITH {t} seconds...')
    time.sleep(t)
    return f'FUNCTION RAN FOR {t} seconds...'


with concurrent.futures.ThreadPoolExecutor() as executor:
    seconds = [5,4,3,2,1]
    #The submit method is submiting each function one at a time.
    # f1 = [executor.submit(myFunction, sec) for sec in seconds]

    # will print them out only as they're completed.
    # for thread in concurrent.futures.as_completed(f1):
    #     print(thread.result())
    # #

    #For the blow, they return the results in the order
        # that they were stareted
    results = executor.map(myFunction,seconds)
    # for result in results:
    #     print(result)


# threads = []
# for time_ in range(10):
#     t = threading.Thread(target=f1, args=[1])
#     t.start()
#     threads.append(t)
#
# for thread in threads:
#     thread.join()

end_time = time.perf_counter()

print(f'Script completed in {round(end_time -start_time,2)} seconds...')
print()
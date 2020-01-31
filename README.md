## Introduction
This program given a list of configured urls and one or more regular expressions to be checked in the url performs it asynchronously.

#### Files:
1. dataset_generator.py : Used to make the dataset to test the final_program.
2. test_final.py: Contains simple unit test for the final_program.
3. final_program.py: Contains code using asyncio, aiohttp, aiofiles for performing the task given in introduction.
4. 'ae.csv': Contains a list of url that is used by dataset generator to make the dataset.

#### Installation Instructions:
1. Clone the repository or download the zip file and go inside the directory.
2. Make a python3 virtual environment.
```python
python3 -m venv .cgi-env
```
3. Activate the virtual environment.
```python
source .cgi-env/bin/activate
```
4. Install the requirements.
```python
pip install -r requirements.txt
```
5. Run dataset_generator.py to generate the dataset.
```python
python dataset_generator.py
```
6. Run test_final.py to perform unit tests.
```python
python test_final.py
```
7. Run final program to start performing the checks!!
```python
python final_program.py
```

#### Design Decisions:
1. Initially, it seemed that the question asked for a crawler but after reading that the urls needs to be checked periodically, I decided against it. As the url frontier would increase drastically and thought to stick to what's clearly been asked.
2. URL normalization is not performed because aiohttp performs it automatically.
3. I tried using the semaphore to control the number of requests but it was resulting in too many open files exception. So, in order to control the throughput, I went with a Queue. The delay makes sures that not all the urls are in queue at once and the number of requests controls the number of GET requests. To increase throughput, reduce delay and add more requests and to decrease throughput vice versa.
4. Using aiofiles, aiohttp and asyncio is used to implement asynchronous execution.
5. To test cleanup using the signal, just comment the latter part.

#### Things that could have been improved:
1. Especially the unit tests!
2. Implement priority queue and using freshness to decide which pages to fetch. Also needs to decide freshness criterion. But, this goal is again not mentioned.
3. Can add random user agents to requests to not get blocked by the server.
4. If the url list contains domains from same sites, then politeness needs to be implemented. If t is the response time, the next page from the domain can be fetched after 5t. In this program, we can implement somewhat of politness by increasing the delay of producer.
5. Working on graceful cleanup. Maybe need to look into aiohttp more in depth.
6. Can add logging.

#### References
1.<https://realpython.com/async-io-python/> 

2.<https://www.roguelynn.com/words/asyncio-graceful-shutdowns/>

from itertools import cycle
import asyncio
import aiohttp
from aiohttp import ClientSession
import aiofiles
import pickle
import time
from datetime import datetime
import re
import signal

# filename to be used for storing the result of checking
filename = 'checkedurls.csv'

def load_dataset():
	""" Loads the dataset generated using dataset_generator.py """
	with open('dataset.pickle','rb') as f:
		dataset = pickle.load(f)
	return dataset

async def producer(delay, dataset):
	"""
	Producer is used to keep cycling through the urls so that the
	queue is never empty

	Parameters
	__________

	delay : float
		a decimal number to delay adding all urls at once in queue
	dataset: iterable
		calling next() on dataset gives a tuple(url,[regex])

	"""

	while True:
		await queue.put(next(dataset))
		await asyncio.sleep(delay)

async def check(url_with_regex, session):
	"""
	check is used to fetch the url and check whether each regular expression from
	the list of regular expressions is present in the content or not. The url, time
	of check, response time (elapsed_time), result of checks(found) and a message is
	returned as a tuple object called result.
	
	Parameters
	__________

	url_with_regex : tuple
		a tuple object containing url and list of regular expressions for that url
	session: ClientSession()
		a aiohttp session object for making asynchronus requests

	Raises
	______

	Exception
		Used to capture all types of HTTP and non HTTP exception. In case of error,
		time_elapsed is set as None, results is list of False boolean values and the
		corresponding error message is returned.

	"""

	url, regexes = url_with_regex
	time_of_check = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
	try:
		start = time.perf_counter()
		response = await session.get(url)
		time_elapsed = time.perf_counter() - start
		content = await response.text()
		found = []
		for regex in regexes:

			if(bool(re.search(regex,content))):
				found.append(True)
			else:
				found.append(False)
		message = 'Check OK!'
		result = (url, time_of_check, time_elapsed, found, message)
		return result
	except Exception as error_message:
		result = (url, time_of_check, None, [False]*len(regexes), error_message)
		return result


async def write_result(url_with_regex, session):
	"""
	write_result calls check to get the result and writes it to the file
	asynchronously. Before writing to the file, the result tuple is converted
	to string seperated by ',' .

	Parameters
	__________

	url_with_regex : tuple
		a tuple object containing url and list of regular expressions for that url
	session: ClientSession()
		a aiohttp session object for making asynchronus requests


	"""

	result = await check(url_with_regex, session)
	result = ", ".join(map(str,result))
	print(result)
	if result:
		async with aiofiles.open(filename,'a') as f:
			await f.write(result+"\n")

async def consumer():
	"""
	consumer is used to deque the url present in queue and calls write_result
	on url. consumer are basically worker couroutines that fetch url, check
	regex and write the result. Then, it deques the next url from queue.

	"""
	while True:
		url_with_regex = await queue.get()
		async with ClientSession() as session:
			await write_result(url_with_regex, session)

async def cleanup(signal, loop):
	"""
	cleanup is used to cancel all the pending tasks in the event loop. For
	running task we wait for them to finish and then stop the event loop.

	Parameters
	__________

	signal : signal handler
		a signal sent to process when trying to terminate the script
	loop: Current event loop from asyncio 
		event loop object to which the signal handler is attached


	"""
	tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
	[task.cancel() for task in tasks]
	await asyncio.gather(*tasks, return_exceptions=True)
	loop.stop()


if __name__ == "__main__":
	"""
	The core of the program.

	We load the dataset and create a queue as well as an event loop. We use
	delay as well as no_of_requests to control the throughput. To increase throughput,
	reduce delay and add more requests and to decrease throughput vice versa.

	producer tasks keeps adding url by cycling though it whereas consumer task keep fetching
	url from queue and process it. The event loop runs forever.

	I have commented the signal handler portion of the code as it's not working properly
	because aiohttp sessions are not closed properly. On using signal handling, it requires
	2-3 interuppts to exit gracefully. This will clean up resources.

	Instead, I am catching keyboard interuppt for now and cancelling the tasks. As, I do not
	wait for running couroutines to stop, loop.close() gives warning so I just stop the loop.
	This does not clean up resouces but fulfills the requirement of script terminating immediately.


	"""
	dataset = cycle(load_dataset())
	loop = asyncio.get_event_loop()
	queue = asyncio.Queue()

	delay = 0.1
	loop.create_task(producer(delay, dataset))
	no_of_requests = 10
	[loop.create_task(consumer()) for i in range(no_of_requests)]

	'''
	signals = [signal.SIGHUP, signal.SIGTERM, signal.SIGINT]
	for sig in signals:
		loop.add_signal_handler(sig, lambda sig=sig: asyncio.create_task(cleanup(sig, loop)))

	try:
		loop.run_forever()
	finally:
		loop.close()

	'''
	try:
		loop.run_forever()
	except KeyboardInterrupt:
		for task in asyncio.Task.all_tasks():
			task.cancel()
		time.sleep(0.1)
		loop.stop()


		



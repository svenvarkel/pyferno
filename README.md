# PyFerno - library for working with Python 3 async/await tasks

The idea of this library is to provide simple methods for working with Lists and Dicts in a simple
[async/await](https://docs.python.org/3/library/asyncio.html) way in Python. Very important feature is control over
concurrency that is implemented by using
[async Semaphores](https://docs.python.org/3/library/asyncio-sync.html?highlight=semaphore#asyncio.Semaphore).
Controlling concurrency is crucial in case of async tasks because it's easy to consume all available IO on your own
server or - even worse - on a remote API. It also provides optional progress bar so that user knows what's going on and
how long it takes.

The history behind creating this library is my background from Node.js development. Node.js has excellent support for
async/await because of its event-based nature.

There's a really great Javascript Promise library [Bluebird](https://github.com/petkaantonov/bluebird). It's been used
as source for inspiration.

The name "Promise" is also brought over from Javascript world, and it reflects pretty wall what async tasks are -
promises that may or may not fulfill.

For those who haven't used Javascript promises - you can think of these as "methods that may or may not finish its job
some time in the future. But until then lets (a)wait for it. And it doesn't block/mess with others in the same time" :)

Currently, this library exports 2 methods for working with lists and dicts in an async way:

- Promise.all() for working with Lists of tasks
- Promise.props() for working with Dicts of tasks

# Usage

## With a List of tasks

```
# this is a working example of await/async with progress bar and controlled concurrency
import random
import asyncio
from typing import List
from datetime import datetime
from pyferno.promise import Promise
 
async def fn() -> List: 
    _start = datetime.utcnow()
    async def _internal_worker(i:int) -> float:
        # do something asynchronously
        _delay = round(random.uniform(0.6, 6.6), 2)
        await asyncio.sleep(_delay)
        print(f"Hi, I'm task #{i} and I slept for {_delay} seconds.")
        # do some calculations here or whatever and return value ...
        # for now we just return random float
        return _delay
    
    # let's say there is a huge list with data that needs some work to be done
    some_list_with_data = range(66)
    tasks = list()
    for i in some_list_with_data:
        task = _internal_worker(i)
        tasks.append(task)
        
    out = await Promise.all(tasks, concurrency=8)
    # try what happens if all tasks are executed in parallel
    #out = await Promise.all(tasks, concurrency=len(tasks))
    _end = datetime.utcnow()
    print(f"All {len(tasks)} tasks done in {_end-_start}.")
    print(out)
    return out
    
asyncio.run(fn())
```

## With a Dict of tasks

```
from pyferno.promise import Promise

async def async_worker_fn():
    # do something asynchronously
    return something
    
tasks = {
    "task1": async_worker_fn(),
    "task2": async_worker_fn(),
    "task3": async_worker_fn()
}
out = await Promise.props(tasks, concurrency=2, progress="A nice progressbar")
print(out)
```

## With a bit more asyncio context

```
import asyncio
from pyferno.promise import Promise

async def async_worker_fn():
    # do something asynchronously
    return something
    
# this function wraps the main logic into async method   
async def main_async_wrapper():
    tasks = [
        async_worker_fn(),
        async_worker_fn(),
        async_worker_fn()
    ]
    out = await Promise.all(tasks, progress="A nice progressbar")
    return out

# note, this is "normal" synchronous function
def main():
    loop = asyncio.get_event_loop()
    out = loop.run_until_complete(main_async_wrapper())
    loop.close()
    print(out)
  
if __name__ == "__main__":
    main()  
```

# API

## Promise.all(_Promise__tasks: list, concurrency: Optional[int] = 10, progress: Optional[AnyStr] = None) -> List

Runs through the list of tasks asynchronously by limiting the concurrency by using a semaphore

    :param __tasks: List of tasks
    :param concurrency: Concurrency of running tasks, integer. Defaults to 10
    :param progress: Progress bar message or boolean True to display default progress bar
    :return: Returns list of finished tasks (fulfilled promises)

## Promise.props(_Promise__props: dict, concurrency: Optional[int] = 10, progress: Optional[AnyStr] = None) -> Dict

Runs through the dict of key,task asynchronously by limiting the concurrency b using a semaphore. Map results back to the
dictionary with same keys with all tasks fulfilled. It will fail if any task fails

    :param __props: Dict with name:task pairs. Task is an async function
    :param concurrency: Concurrency of running tasks, integer. Defaults to 10
    :param progress: Progress bar message or boolean True to display default progress bar
    :return: Returns dict with name:<finished task> pairs.


## Promise.generate(_Promise__tasks: list, concurrency: Optional[int] = 10, progress: Optional[AnyStr] = None) -> AsyncGenerator[List, None]

Returns AsyncGenerator that runs through the list of tasks asynchronously by limiting the concurrency by using a semaphore
and yields resolved "promises" (coroutines)

    :param __tasks: List of tasks
    :param concurrency: Concurrency of running tasks, integer. Defaults to 10
    :param progress: Progress bar message or boolean True to display default progress bar
    :return: AsyncGenerator


# License

This library is licensed with MIT license.

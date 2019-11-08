# PyFerno - an async/promise library for Python 3 async inferno

The idea of this library is to provide simple methods for working with [async/await](https://docs.python.org/3/library/asyncio.html) in Python.  
 
The history behind creating this library is my background from Node.js development. 
Node.js has excellent support for async/await because of its event-based nature.

There's an excellent Javascript Promise library [Bluebird][https://github.com/petkaantonov/bluebird].
It's been used as source for inspiration.

The name "Promise" is also brought over from Javascript world.

For those who haven't used Javascript promises - you can think of these as "methods that will or will not finish its job
some time in the future. But until then lets (a)wait for it. And it doesn't block/mess with others in the same time" :)

Right now this library exports 2 methods for working with lists and dicts in an async way.

# Usage

## With list of tasks

```
from pyferno.promise import Promise

async def async_worker_fn():
    # do something asynchronously
    return something
    
tasks = [
    async_worker_fn(),
    async_worker_fn(),
    async_worker_fn()
]
out = await Promise.all(tasks, progress="A nice progressbar")
print(out)
```

## With dict of tasks

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

## Promise.all(_Promise__tasks: list, concurrency: int = 10, progress: object = None) -> list

Runs thru the list of tasks asynchronously by limiting the concurrency by using a semaphore

    :param __tasks: List of tasks
    :param concurrency: Concurrency of running tasks, integer. Defaults to 10
    :param progress: Progress bar message or boolean True to display default progress bar
    :return: Returns list of finished tasks (fulfilled promises)


## Promise.props(_Promise__props: dict, concurrency: int = 10, progress: object = None) -> dict

Runs thru the dict of key,task asynchronously by limiting the concurrency b using a semaphore.
Maps results back to the dictionary with same keys with all tasks fulfilled.
It will fail if any task fails
    
    :param __tasks: Dict with name:task pairs. Task is an async function
    :param concurrency: Concurrency of running tasks, integer. Defaults to 10
    :param progress: Progress bar message or boolean True to display default progress bar
    :return: Returns dict with name:<finished task> pairs.


# License

This library is licensed with MIT license.

import pytest
import asyncio
import random
from pyferno.promise import Promise


async def dummy_fn(i: int = None):
    await asyncio.sleep(random.randint(0, 5))
    return i


@pytest.fixture(name="list_of_tasks")
def get_list_of_tasks():
    list_of_tasks = list()
    for i in range(0, 10):
        list_of_tasks.append(dummy_fn())

    return list_of_tasks


@pytest.fixture(name="dict_of_tasks")
def get_dict_of_tasks():
    dict_of_tasks = dict()
    for i in range(0, 10):
        key = f"key_{i}"
        dict_of_tasks[key] = dummy_fn(i)

    return dict_of_tasks


@pytest.mark.asyncio
async def test_standard_description(list_of_tasks):
    out = await Promise.all(list_of_tasks, progress=True)
    assert isinstance(out, list)
    return out


@pytest.mark.asyncio
async def test_custom_description(list_of_tasks):
    out = await Promise.all(list_of_tasks, progress="A nice progressbar")
    assert isinstance(out, list)
    return out


@pytest.mark.asyncio
async def test_no_progress(list_of_tasks):
    assert isinstance(list_of_tasks, list)
    print("no progress bar")
    out = await Promise.all(list_of_tasks)
    assert isinstance(out, list)


@pytest.mark.asyncio
async def test_dict_of_tasks(dict_of_tasks):
    assert isinstance(dict_of_tasks, dict)
    out = await Promise.props(dict_of_tasks)
    assert isinstance(out, dict)

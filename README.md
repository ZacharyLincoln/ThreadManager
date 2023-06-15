
<h1 align="center">
  <br>
  <img id="logo" src="readme_assets/logo.png" alt="Thread Manager Logo" width="200">
  <br>
  Thread Manager
  <br>
</h1>

<h4 align="center", id="desc">A simple solution for managing multiple threads</h4>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#license">License</a>
</p>


## Key Features

* Task Thread Manager: Manages multiple task thread
* Task Thread: Runs tasks (functions) in queue 

## How To Use

Install ThreadManager
```
pip install ThreadManager
```

Import ThreadManager
```
import ThreadManager
```

### Basic Usage

Creating a task thread manager
```
tm = TaskThreadManager(max_threads=1)
```

Adding tasks to task thread manager
```
tm.insert_to_que([function, param1, param2, ...])
```

```
def job(i, j):
    for kj in range(3):
        #print("working")
        sleep(1)
    return i + j
    
id1 = tm.insert_to_que([job, 3, 6])
id2 = tm.insert_to_que([job, 7, 5])
```

Start running tasks
```
tm.start()
```

Check if job is done
```
tm.is_job_done(id1)
```

Await the output of a task
```
output = await_get_output(id1)
```

Get the output of a task without awaiting for it to finish
```
output = get_output(id1)
```

## License

MIT

---
> [zlincoln.dev](https://www.zlincoln.dev) &nbsp;&middot;&nbsp;
> GitHub [@ZacharyLincoln](https://github.com/ZacharyLincoln)


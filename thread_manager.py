import threading
import time
from tqdm import tqdm
from time import sleep
import logging


class TaskThreadManager:

    def __init__(self, max_threads, delay_between_jobs=0, delay_between_blocks=1, progress_bar=None, progress_bar_pos_start=0):
        self.max_threads = max_threads
        self.task_threads = []
        for i in range(max_threads):
            pbar = None
            if progress_bar is not None:
                pbar = tqdm(desc=progress_bar.desc, position=i+progress_bar_pos_start, bar_format=progress_bar.bar_format)
            self.task_threads.append(TaskThread(delay_between_jobs=delay_between_jobs, delay_between_blocks=delay_between_blocks, progress_bar=pbar))

    def start(self):
        logging.info("Starting Task Thread Manager")
        for thr in self.task_threads:
            thr.start()

    """
        Stops all Task Threads
        Params
            None
        Output
            None
    """
    def stop(self):
        logging.info("Stopping Task Thread Manager")
        for thr in self.task_threads:
            thr.stop()

    """
    Inserts a new task in the que
    Params
        - task: A task is a function followed by arguments example [function_call_with_parenthesis, arg1, arg2, arg3, ..., argn]  
    Output
        - job_id: an integer that is used to see if the job is done and to get the output of the function call once it is done.    
    """
    def insert_to_que(self, task, index=None):
        min_amount = 9999999999999
        min_thr_id = -1

        if index is None:
            for id, thr in enumerate(self.task_threads):
                sum = 0
                sum += len(thr.running_queue)
                sum += len(thr.queue)
                if min_amount > sum:
                    min_amount = sum
                    min_thr_id = id
        else:
            min_thr_id = index

        job_id = self.task_threads[min_thr_id].insert_to_que(task)
        job_id = f"{min_thr_id}:{job_id}"

        return job_id

    """
        Checks to see if the job is done
        Params
            - job_id: The job id that was given from insert_to_que
        Output
            - is_job_done: True or False, depending on if the job is done or not
    """
    def is_job_done(self, job_id):

        thr_id, job_id = str(job_id).split(":")

        return self.task_threads[int(thr_id)].is_job_done(int(job_id))

    """
        Gets the output of the job
        Params
            - job_id: The job id that was given from insert_to_que
        Output
            - output: The output of the completed job.
    """
    def get_output(self, job_id):

        thr_id, job_id = str(job_id).split(":")

        return self.task_threads[int(thr_id)].get_output(int(job_id))


class TaskThread(threading.Thread):
    def __init__(self, delay_between_jobs=0, delay_between_blocks=1, progress_bar=None):
        super().__init__()
        self.queue = []
        self.stop_flag = threading.Event()
        self.pbar = None
        self.done = []
        self.job_num = 0
        self.progress_bar = progress_bar
        self.delay_between_jobs = delay_between_jobs
        self.delay_between_blocks = delay_between_blocks
        self.running_queue = []

    def run(self):
        while not self.stop_flag.is_set():
            sum = 0
            self.running_queue = []

            if self.progress_bar is not None:
                self.progress_bar.reset()

            try:
                for task_id, task in self.queue:
                    self.running_queue.append([task_id, task])
                    self.queue.remove([task_id, task])
                    sum += 1

                if self.progress_bar is not None:
                    self.progress_bar.total = sum

                for task_id, task in self.running_queue:
                    func = task[0]
                    args = task[1:]
                    output = func(*args)
                    self.done.append([task_id, output])

                    if self.progress_bar is not None:
                        self.progress_bar.update(1)
                    sleep(self.delay_between_jobs)
            except:
                pass

            time.sleep(self.delay_between_blocks)
        if self.progress_bar is not None:
            self.progress_bar.close()

    """
    Inserts a new task in the que
    Params
        - task: A task is a function followed by arguments example [function_call_with_parenthesis, arg1, arg2, arg3, ..., argn]  
    Output
        - job_id: an integer that is used to see if the job is done and to get the output of the function call once it is done.    
    """
    def insert_to_que(self, task):
        self.job_num += 1
        self.queue.append([self.job_num, task])
        return self.job_num

    """
        Checks to see if the job is done
        Params
            - job_id: The job id that was given from insert_to_que
        Output
            - is_job_done: True or False, depending on if the job is done or not
    """
    def is_job_done(self, job_id):
        for id, output in self.done:
            if id == job_id:
                return True
        return False

    """
        Gets the output of the job
        Params
            - job_id: The job id that was given from insert_to_que
        Output
            - output: The output of the completed job.
    """
    def get_output(self, job_id):
        for id, output in self.done:
            if id == job_id:
                return output
        return None

    """
        Stops the Task Thread
        Params
            None
        Output
            None
    """
    def stop(self):
        self.stop_flag.set()


def await_get_output(job_id, manager, sleep_time=0.05):
    while not manager.is_job_done(job_id):
        sleep(sleep_time)
    return manager.get_output(job_id)


if __name__ == "__main__":
        from time import sleep

        def job(i, j):
            for kj in range(3):
                #print("working")
                sleep(1)
            return i + j
        pbar = None
        pbar = tqdm(desc="Task Thread", total=0, bar_format="{desc:<30.30}{percentage:3.0f}%|{bar:20}{r_bar}")

        tm = TaskThreadManager(max_threads=1, progress_bar=pbar)
        id1 = tm.insert_to_que([job, 3, 6])
        id2 = tm.insert_to_que([job, 7, 5])

        print(id1)
        print(id2)

        tm.start()

        print(await_get_output(id1, tm))
        print(await_get_output(id2, tm))

        sleep(2)
        tm.stop()

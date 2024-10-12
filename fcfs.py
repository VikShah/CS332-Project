# Names: Vikas Shah, Priyansh Patel, Jonathan Martinez
# Project: CS332 - CPU Scheduling Simulator
# Description: This script implements the First-Come-First-Serve (FCFS) scheduling algorithm. 

import socket
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
MAX_BUFFER_SIZE = 1024

# Struct to represent a process
class Task:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time

# Queue data structure
class TaskQueue:
    def __init__(self, size):
        self.tasks = [None] * size
        self.head = 0
        self.tail = -1
        self.count = 0

    def add_task(self, task):
        if self.count < MAX_BUFFER_SIZE:
            self.tail = (self.tail + 1) % MAX_BUFFER_SIZE
            self.tasks[self.tail] = task
            self.count += 1

    def get_task(self):
        if self.count > 0:
            task = self.tasks[self.head]
            self.head = (self.head + 1) % MAX_BUFFER_SIZE
            self.count -= 1
            return task
        else:
            # when queue is empty, return a dummy task
            dummy_task = Task(-1, 0, 0)
            return dummy_task

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Create a socket
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
    except socket.error as e:
        print("Connection failed:", e)
        exit(1)
    
    print("Connected to the server")

    # implementing the FCFS algorithm here

    task_queue = TaskQueue(MAX_BUFFER_SIZE)
    current_time = 0

    while True:
        # get task data from server
        data = client_socket.recv(MAX_BUFFER_SIZE).decode('utf-8').strip()
        if not data:
            break
        
        # if the server sends "END", stop receiving
        if data == "END":
            print("End of process stream received.")
            break

        # split the task data (PID and Burst Time come as a space-separated string)
        pid, burst_time = map(int, data.split())

        # add the task to the queue with its arrival time
        task_queue.add_task(Task(pid, current_time, burst_time))
        print(f"Received process info: PID={pid} Burst Time={burst_time} Arrival Time={current_time}")
        
        # update the current time based on how long this task takes to run
        current_time += burst_time

    # Close the socket
    client_socket.close()

if __name__ == "__main__":
    main()

# system monitor tools , it includes CPU,Memory & Bandwidth
# it works as task manager
# with the help of youtube and chatgpt, i cretaed this


import time
import psutil
import tkinter as tk
from tkinter import ttk # provides themed widgets that offer a more modern look compared to the classic tkinter widgets.
from matplotlib.figure import Figure #represents a figure environment for plotting.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #tkinter applications for displaying matplotlib figures
#these are frameworks and libraries

class SystemMonitorApp: #system monitor er manin class
    def __init__(self, root): #Sets up the main tkinter window (root), sets its title and size,self is the instance of the class
        self.root = root #root is a tkinter Tk object representing the main window of the application
        self.root.title("System Monitor")
        self.root.geometry("800x800")
# are used to configure the main tkinter window (root) that is passed into the class constructor (__init__) 
# # when an instance of SystemMonitorApp

        # Create the frames for each section
        self.create_frames()
#The create_frames() method is called to create separate sections within the main window of the application. These sections (frames) will hold the widgets (labels, progress bars, and graphs) for CPU, memory, and network usage.

        # Create labels and progress bars for CPU, Memory, and Network
        self.create_widgets()

        # Initialize network data
        self.last_received = psutil.net_io_counters().bytes_recv ##gives the total number of bytes received by the network interfaces(prothom ta function, then attributes)
        self.last_sent = psutil.net_io_counters().bytes_sent ##gives the total number of bytes sent by the network interfaces
        self.last_total = self.last_received + self.last_sent ##(for sent , This variable stores the total number of bytes sent at the time of initialization)
                                                     

        # Initialize data for graphs
        self.cpu_data = [] #This list will store the CPU usage percentages over time. Each time the update_monitor method is called, the current CPU usage percentage is appended to this list.
        self.mem_data = [] #This list will store the memory usage percentages over time. Each time the update_monitor method is called, the current memory usage percentage is appended to this list.
        self.net_received_data = [] #This list will store the amount of data received over the network (in megabytes) over time. Each time the update_monitor method is called, the new amount of data received since the last update is appended to this list.
        self.net_sent_data = [] #This list will store the amount of data sent over the network (in megabytes) over time. Each time the update_monitor method is called, the new amount of data sent since the last update is appended to this list.

        # Create the graphs
        self.create_graphs() #graph reate korar jnno

        # Start the monitoring update loop
        self.update_monitor() #continuously data gulo update krche 

    def create_frames(self): ##upore bar er kajgulo
        self.cpu_frame = ttk.LabelFrame(self.root, text="CPU")
        self.cpu_frame.pack(fill="both", expand=True, padx=10, pady=5) ##filling 

        self.mem_frame = ttk.LabelFrame(self.root, text="Memory")
        self.mem_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.net_frame = ttk.LabelFrame(self.root, text="Network")
        self.net_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def create_widgets(self):
        # CPU Usage
        self.cpu_label = ttk.Label(self.cpu_frame, text="CPU Usage: ")
        self.cpu_label.pack(anchor="w", padx=5, pady=5) ##w dara left e allign howake bujhay

        self.cpu_usage = ttk.Progressbar(self.cpu_frame, orient='horizontal', length=400, mode='determinate')#green line er box r length 
        self.cpu_usage.pack(pady=5, padx=5)#graph and progress bar r majher distance 

        # Memory Usage
        self.mem_label = ttk.Label(self.mem_frame, text="Memory Usage: ")
        self.mem_label.pack(anchor="w", padx=5, pady=5)

        self.mem_usage = ttk.Progressbar(self.mem_frame, orient='horizontal', length=400, mode='determinate')
        self.mem_usage.pack(pady=5, padx=5)

        # Network Usage
        self.net_label = ttk.Label(self.net_frame, text="")
        self.net_label.pack(anchor="w", padx=5, pady=5)

    def create_graphs(self):
        # Create a figure for CPU usage
        self.cpu_fig = Figure(figsize=(5, 2), dpi=100) #graph r box r size 
        ##figsize=(5, 2): This sets the size of the figure to 5 inches wide and 2 inches tall.
        ##dpi=100: This sets the dots per inch (resolution) of the figure to 100.
        self.cpu_ax = self.cpu_fig.add_subplot(111)
        ##111 is a shorthand for a grid with 1 row and 1 column, and this is the first subplot in that grid.
        self.cpu_ax.set_title("CPU Usage Over Time")
        self.cpu_ax.set_xlabel("Time")
        self.cpu_ax.set_ylabel("Usage (%)")
        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, master=self.cpu_frame)
        self.cpu_canvas.get_tk_widget().pack(pady=5, padx=5)

        # Create a figure for Memory usage
        self.mem_fig = Figure(figsize=(5, 2), dpi=100)
        self.mem_ax = self.mem_fig.add_subplot(111)
        self.mem_ax.set_title("Memory Usage Over Time")
        self.mem_ax.set_xlabel("Time")
        self.mem_ax.set_ylabel("Usage (%)")
        self.mem_canvas = FigureCanvasTkAgg(self.mem_fig, master=self.mem_frame)
        self.mem_canvas.get_tk_widget().pack(pady=5, padx=5)

        # Create a figure for Network usage
        self.net_fig = Figure(figsize=(5, 2), dpi=100)
        self.net_ax = self.net_fig.add_subplot(111)
        self.net_ax.set_title("Network Usage Over Time")
        self.net_ax.set_xlabel("Time")
        self.net_ax.set_ylabel("MB")
        self.net_canvas = FigureCanvasTkAgg(self.net_fig, master=self.net_frame)
        self.net_canvas.get_tk_widget().pack(pady=5, padx=5)

    def update_monitor(self):
        # Update CPU and Memory usage
        # Retrieve the CPU usage percentage over a 1-second interval
        cpu_usage = psutil.cpu_percent(interval=1)
        # Retrieve the current memory usage percentage
        mem_usage = psutil.virtual_memory().percent

        # Update the CPU progress bar with the new CPU usage value
        self.cpu_usage['value'] = cpu_usage
        # Update the CPU usage label to display the current CPU usage percentage
        self.cpu_label.config(text=f"CPU Usage: {cpu_usage:.2f}%")

        self.mem_usage['value'] = mem_usage
        self.mem_label.config(text=f"Memory Usage: {mem_usage:.2f}%")

        # Update Network usage
        bytes_received = psutil.net_io_counters().bytes_recv
        bytes_sent = psutil.net_io_counters().bytes_sent
        bytes_total = bytes_received + bytes_sent

        new_received = bytes_received - self.last_received
        new_sent = bytes_sent - self.last_sent
        new_total = bytes_total - self.last_total

        mb_new_received = new_received / 1024 / 1024
        mb_new_sent = new_sent / 1024 / 1024

        self.net_label.config(text=f"Network: {mb_new_received:.2f} MB received, {mb_new_sent:.2f} MB sent")

        self.last_received = bytes_received
        self.last_sent = bytes_sent
        self.last_total = bytes_total

        # Update graph data
        self.cpu_data.append(cpu_usage)
        self.mem_data.append(mem_usage)
        self.net_received_data.append(mb_new_received)
        self.net_sent_data.append(mb_new_sent)

        if len(self.cpu_data) > 60: ##60 er beshi otikrom krle pichoner dike back kore
            self.cpu_data.pop(0)
        if len(self.mem_data) > 60:
            self.mem_data.pop(0)
        if len(self.net_received_data) > 60:
            self.net_received_data.pop(0)
        if len(self.net_sent_data) > 60:
            self.net_sent_data.pop(0)

        # Clear and redraw the graphs
        self.cpu_ax.clear()
        self.cpu_ax.plot(self.cpu_data, color='blue', label="CPU Usage (%)")
        self.cpu_ax.legend()
        self.cpu_canvas.draw()

        self.mem_ax.clear()
        self.mem_ax.plot(self.mem_data, color='green', label="Memory Usage (%)")
        self.mem_ax.legend()
        self.mem_canvas.draw()

        self.net_ax.clear()
        self.net_ax.plot(self.net_received_data, color='red', label="Received (MB)")
        self.net_ax.plot(self.net_sent_data, color='orange', label="Sent (MB)")
        self.net_ax.legend()
        self.net_canvas.draw()

        # Schedule the update every 1 second
        self.root.after(1000, self.update_monitor)

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()

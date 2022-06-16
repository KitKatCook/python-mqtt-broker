import asyncio
from threading import Thread
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Notebook
from interoperability.client.publisher.publisher import Publisher
from interoperability.client.consumer.consumer import Consumer
from .cluster_adapter import ClusterAdapter

class WindowViewer():
    def __init__(self):
        self.warden_address = self.warden_address
        self.warden_port = self.warden_port
        self.root = Tk()
        self.root.geometry("1920x1080")
        self.root.title("Test Application")
        self.root.configure(background='lightblue')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind('<Escape>', self.on_closing)
        self.cluster_adapter = ClusterAdapter()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

    def home(self):
        self.clear()
        Label(text="Welcome to message broker test application", width="300", height="2", font=("Calibri", 13)).pack() 
        self.default_blank_space()
        def __createMenuOption(text, callback):
            Button(self.root, text=text, width=20, height=5, command=callback).pack()
        def __go_stresser():
            self.stresser()
        def __go_settings():
            self.settings()
        def __check_cluster_status():
            msg = 'Cluster is running' if self.cluster_adapter.check_cluster_status() else 'Cluster is not running'
            messagebox.showinfo(title='Status', message=msg)
        __createMenuOption("Stress tool", __go_stresser)
        self.default_blank_space()
        __createMenuOption("Settings", __go_settings)
        self.default_blank_space()
        __createMenuOption("Check cluster", __check_cluster_status)
        self.default_blank_space()
        self.root.mainloop()
    
    def settings(self):
        self.clear()
        Label(text="Test app consumer settings", width="300", height="2", font=("Calibri", 13)).pack() 

        def __go_home():
            self.home()

        top_widget_frame = Frame(self.root)
        top_widget_frame.pack(side='left', anchor=NW)
        Button(top_widget_frame, text='Back', command=__go_home).pack()
        
        consumer_frame = Frame(self.root)
        consumer_frame.pack(side="top")
        self.default_blank_space()
        Label(consumer_frame,text="Add Consumer - ", width=20,font=("bold",10)).pack()
        Label(consumer_frame,text="Consumer group name", width=20,font=("bold",10)).pack()
        consumer_group_name_entry=Entry(consumer_frame)
        consumer_group_name_entry.pack()
        
        
        self.default_blank_space()
        consumer_frame_list = Frame(self.root)
        consumer_frame_list.pack(side="top")
        Label(consumer_frame_list,text="Consumers - ", width=20,font=("bold",10)).pack()
        consumers_listbox = Listbox(consumer_frame_list)
        consumers_listbox.insert(1, "Python")
        consumers_listbox.pack()

        self.default_blank_space()
        self.root.mainloop()
    
    def stresser(self):
        self.clear()
        Label(text="Test app stresser tool", width="300", height="2", font=("Calibri", 13)).pack() 

        def __go_home():
            self.home()

        top_widget_frame = Frame(self.root)
        top_widget_frame.pack(side='left', anchor=NW)
        Button(top_widget_frame, text='Back', command=__go_home).pack()
        
        self.default_blank_space()

        frame = Frame(self.root)
        frame.pack(side="top")
        topics = self.get_topics(self.cluster_adapter.get_cluster_info())
        Label(frame,text="Topic",width=20,font=("bold",10)).pack()
        topic_list=[]
        for topic in topics:
            topic_list.append(topic["topic"])
        c=StringVar()
        droplist=OptionMenu(frame,c, *topic_list)
        droplist.config(width=15)
        c.set('Choose a topic...')
        droplist.pack()
        Label(frame,text="Message", width=20,font=("bold",10)).pack()
        message_entry=Entry(frame)
        message_entry.pack()
        Label(frame,text="Amount to send", width=20,font=("bold",10)).pack()
        amount_to_send_entry=Entry(frame)
        amount_to_send_entry.pack()

        def send_messages():
            topic_id = [x for x in topics if x["topic"] == c.get()][0]["topic_id"]
            message = message_entry.get()
            amount_to_send = int(amount_to_send_entry.get())
            consumer1 = Consumer(self.warden_address, self.warden_port, "cg1")
            consumer1.subscribe([topic_id], addMessageCg1)
            consumer1_thread = Thread(target=asyncio.run, args=(consumer1.subscribe([topic_id], addMessageCg1),))
            consumer1_thread.start()
            consumer2 = Consumer(self.warden_address, self.warden_port, "cg2")
            consumer2_thread = Thread(target=asyncio.run, args=(consumer2.subscribe([topic_id], addMessageCg2),))
            consumer2_thread.start()
            self.publish_messages(topic_id, message, amount_to_send)

        Button(frame, text='Run test' , width=20,bg="black",fg='white',command=send_messages).pack()
        self.default_blank_space()
        
        def addMessageCg1(messages):
            for message in messages:
                cg1Output.insert(1.0, message + "\n" )

        def addMessageCg2(messages):
            for message in messages:
                cg2Output.insert(1.0, message + "\n" )

        tabparent = Notebook(self.root)

        cg1 = Frame(tabparent)
        tabparent.add(cg1, text="Consumer group 1")
        
        cg2 = Frame(tabparent)
        tabparent.add(cg2, text="Consumer group 2")

        tabparent.pack(expand=1, fill='both')

        cg1OutputScrollBar = Scrollbar(cg1, orient='vertical')
        cg2OutputScrollBar = Scrollbar(cg2, orient='vertical')


        cg1Output = Text(cg1, height = 30, width = 25, yscrollcommand=cg1OutputScrollBar.set)
        cg1Output.pack(fill='both', expand=True, side=LEFT)
        cg1Output.insert(1.0, "No Messages.")


        cg2Output = Text(cg2, height = 30, width = 25, yscrollcommand=cg2OutputScrollBar.set)
        cg2Output.pack(fill='both', expand=True, side=LEFT)
        cg2Output.insert(1.0, "No Messages.")


        cg1OutputScrollBar.pack(side=RIGHT, fill='y')
        cg1OutputScrollBar.config(command=cg1Output.yview)


        cg2OutputScrollBar.pack(side=RIGHT, fill='y')
        cg2OutputScrollBar.config(command=cg2Output.yview)

        timeResults = Entry(self.root, )

        self.root.mainloop() 

    def default_blank_space(self):
        Label(self.root, text="", background='lightblue').pack()

    def clear(self):
        _list = self.root.winfo_children()
        for item in _list:
            if item.winfo_children():
                _list.extend(item.winfo_children())
        for item in _list:
            item.pack_forget()
        self.reset()

    def reset(self):
        self.root.configure(background='lightblue')

    def get_topics(self, cluster_info):
        topics = [x["topic_id"] for x in cluster_info]
        unique_topics = []
        for topic in list(set(topics)):
            unique_topics.append([x for x in cluster_info if x["topic_id"] == topic][0])
        return unique_topics

    def publish_messages(self, topic_id, message, number_of_times):
        publisher: Publisher = Publisher(self.warden_address, self.warden_port)
        publisher.publish(topic_id, message, number_of_times)
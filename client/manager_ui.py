import tkinter as tk
from tkinter.constants import NONE
from mysocket import MySocket
class Manager(tk.Frame):
    def __init__(self,master=None,sk=None):
        
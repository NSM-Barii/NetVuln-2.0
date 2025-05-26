# NETVULN 2.0 // THIS MODULE WILL HOLD THE LOGIC FOR STORING SCAN RESULTS ALONG WITH MUCH MORE AND SETTINGS LOGIC


# UI IMPORTS
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
import pyfiglet


# NETWORK IMPORTS
import socket, ipaddress, dns.resolver, openai


# ETC IMPORTS
import threading, time, random, requests, os
from concurrent.futures import ThreadPoolExecutor
import pyttsx3
from plyer import notification



# CONSTANTS & GLOBALS
console = Console()
terminal_width = console.size.width


# FILE HANDLING
from pathlib import Path
import json


    # BASE DIR
base_dir = Path.home() / "Documents" / "NSM Tools" / ".data" / "NetVuln 2.0"
base_dir.mkdir(parents=True, exist_ok=True)




# SCAN TREE
#
#  .data
#     Netvuln 2
#       scan_results
#         raw_nmap_save
#         raw_ffuf_save
#         raw_
#
#




class File_Saving():
    """This method will be responsible for saving and storing scan results"""


    def __init__(self):
        pass


    def push_info():
        """This is where info will be pushed to then be stored"""


        path = base_dir / "scan_results" / ""
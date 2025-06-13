# NETVULN 2.0 // THIS MODULE WILL BE RESPONSIBLE FOR MAKING SURE THE USER HAS ALL NECESSARY DEPENDENCIES AND PERFORM MULTI-MODULE LOGIC




class  Import_Handler():
    """This class will be responsible for making sure the user has all the necessary dependencies installed"""



    def __init__(self):
        pass


    @staticmethod
    def Import_checker():
        """This will try to import all needed libaries"""

        
        try:

            # UI IMPORTS
            print("ui")
            from rich.panel import Panel
            from rich.table import Table
            from rich.live import Live
            from rich.console import Console
            import pyfiglet


            # NETWORK IMPORTS
            print("network")
            import socket, ipaddress, dns


            # ETC IMPORTS
            print("etc")
            import threading, time, random, requests, os
            from concurrent.futures import ThreadPoolExecutor
            import pyttsx3
            from plyer import notification




            # NSM IMPORTS




            # FILE HANDLING
            print("file handling")
            from pathlib import Path
            import json


            # GIVE THE GO AHEAD
            return True
        


        except ImportError as e:
            print("\nFailed to import Modules\n")

            # GIVE THE FALSE AHEAD
            return False
    

    
    @staticmethod
    def import_installer():
        """This method will be responsible for installing dependencies"""


        choice = "yes" #input("If you want to automatically install libaries type yes: ").strip().lower()

        if choice == "yes" or choice == "y" or choice == "1":
            print("Bet now downloading Dependencies")

            
            # BASE LIBARIES
            import os, json
            from pathlib import Path

            # GET REQ FILE
            #path = Path.home() / "Documents" / "NSM Tools" / "Network Tools" / "NetVuln 2" / "requirements.json"

            path = Path('/app/requirements.json')
            with open(path, "r") as file:
                libaries = json.load(file)
            

            # LOOP FOR EXCEPTIONS
            while True:

                try:

                    for key, value in libaries.items():
                        print(f"Now trying to install: {value}   #{key}/20")
                        os.system(f"pip install {value}")

                    

                    # NOW IMPORT LIBARIES
                    from rich.console import Console
                    import time
                    console = Console()

                    # NOW PRINT SOME CODE
                    console.print("Dependencies Successfully installed.", style="bold blue")
                    console.print("Now Restarting cmd instance", style="bold green")
                    time.sleep(3)


                    # GIVE THE GO AHEAD
                    return True


                    # NOW TO BRING BACK TO MAIN MENU 
                    #from nsm_ui import MainUI
                    #MainUI.main()
                
                except KeyboardInterrupt as e:
                    break
    

                except Exception as e:
                    print(f"Got a Exception error will, continue: {e}")
                        


    @staticmethod
    def main():
        """This will be responsible for checking if the user has all the libaries if not they will be installed"""
        
        go = True
        while go:

            # IF LIBARIES ARE INSTALLED PROCCED
            if Import_Handler.Import_checker():
                

                # REDIRECT TO THE UI MODULE, GO FROM THERE
                from nsm_ui import MainUI
                MainUI.main()
                
                go = False

            # ELSE INSTALL THEM
            else:
                Import_Handler.import_installer()
                import os, sys

                #os.execv(sys.executable, ['python'] + sys.argv)



# RUN MULTI MODULE LOGIC FROM HERE
if __name__ == "__main__":
    Import_Handler.main()
import threading
import schedule
import time
import importlib
import os

class Record:
    def __init__(self):
        self.book = ""
        self.author = ""
        self.year = ""
        self.link = ""
        self.publisher = ""
        self.price = ""

    def __str__(self):
        return f"{self.author} - {self.book}: {self.price}"
    
    def __str__(self):
        return f"{self.author} - {self.book}: {self.price}!"

def run_scripts():
    records = []
    scripts_dir = 'scripts'
    for filename in os.listdir(scripts_dir):
        if filename.endswith('.py'):
            module_name = filename[:-3]

            try:
                module = importlib.import_module(f"{scripts_dir}.{module_name}")
            except ImportError as e:
                print(f"Error during importing {module_name} script: {e}")
            else:
                if hasattr(module, 'main'):
                    results = module.main(Record)
                    if results:
                        for res in results:
                            records.append(res)
                    
                else:
                    print(f"Module {module_name} has no main")

    for rec in records:
        print(rec)

def threaded_run(fc):
     fc_thread = threading.Thread(target=fc)
     fc_thread.start()

def main():
    schedule.every().day.at("06:00", "Europe/Prague").do(threaded_run, run_scripts)
    schedule.every(30).seconds.do(threaded_run, run_scripts) # this option is for debugging, later will be deleted

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
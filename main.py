import threading
import schedule
import time
import importlib
import os

def run_scripts():
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
                    message = module.main("arthur clarke")
                    print(message)
                else:
                    print(f"Module {module_name} has no main")

def threaded_run(fc):
     fc_thread = threading.Thread(target=fc)
     fc_thread.start()

def main():
    schedule.every().day.at("06:00", "Europe/Prague").do(threaded_run, run_scripts)
    schedule.every(3).seconds.do(threaded_run, run_scripts)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
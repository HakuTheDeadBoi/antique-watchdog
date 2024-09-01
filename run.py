from aw.config import Config
from aw.querymanager import QueryManager
from aw.configeditor import ConfigEditor
from aw.antiquewatchdog import AntiqueWatchdog

from os import system

def main():
    # init everything
    c = Config()
    qm = QueryManager()

    # run config editor
    ConfigEditor(c).run()

    # run query editor - still not implemented yet

    # run antique watchdog in another thread
    app = AntiqueWatchdog(c, qm)
    scheduler, _, _ = app.run()


    # REPL
    while True:
        try:
            user_input = input(">>> ")

            match user_input.lower():
                case "config":
                    ConfigEditor(c).run()
                case "query":
                    pass
                case "exit":
                    exit()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
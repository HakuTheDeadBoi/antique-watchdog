from aw.config import Config
from aw.querymanager import QueryManager
from aw.configeditor import ConfigEditor
from aw.antiquewatchdog import AntiqueWatchdog

from os import system

def main():
    """
    Main function to initialize and run the application.

    This function performs the following tasks:
    1. Initializes the configuration and query manager.
    2. Launches the ConfigEditor for user configuration.
    3. (Placeholder) Runs the query editor, which is not yet implemented.
    4. Starts the AntiqueWatchdog application in a separate thread.
    5. Provides a REPL (Read-Eval-Print Loop) for user commands.

    Commands in the REPL:
    - "config": Launches the ConfigEditor again.
    - "query": Placeholder for future query editor functionality.
    - "exit": Exits the application.

    The REPL continues to run until the user inputs "exit". Any exceptions are caught
    and printed to the console.
    """
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
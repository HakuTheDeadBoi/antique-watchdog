import tkinter as tk
from tkinter import ttk
from time import sleep

from aw import CE_WIDTH, CE_HEIGHT, CE_TITLE
from aw import LOGIN, PASSWORD, RECIPIENT, SERVER, PORT, TIME, PERIOD, WEEKDAY
from aw import DAY_TO_INT_MAP, INT_TO_DAY_MAP
from aw.config import Config
from aw.validator import Validator

class ConfigEditor:
    """
    A graphical user interface (GUI) for editing configuration settings.

    This class provides a Tkinter-based interface to load, modify, and save
    configuration settings related to mailer and scheduler configurations.
    
    Attributes:
        _aw_config (Config): The configuration handler instance.
        _window (tk.Tk): The main Tkinter window.
        _left_column (tk.LabelFrame): Frame for mailer configuration widgets.
        _right_column (tk.LabelFrame): Frame for scheduler configuration widgets.
        _lower_text_area (tk.LabelFrame): Frame for displaying messages.
        _login_entry (tk.Entry): Entry widget for the login field.
        _password_entry (tk.Entry): Entry widget for the password field.
        _recipient_entry (tk.Entry): Entry widget for the recipient field.
        _server_entry (tk.Entry): Entry widget for the server field.
        _port_entry (tk.Entry): Entry widget for the port field.
        _time_entry (tk.Entry): Entry widget for the time field.
        _weekday_cbox (ttk.Combobox): Combo box for selecting the weekday.
        _period_cbox (ttk.Combobox): Combo box for selecting the period.
        _submit_button (tk.Button): Button to save the configuration.
        _exit_button (tk.Button): Button to exit the application.
        _messages_text_area (tk.Text): Text area for displaying messages.
    """
    def __init__(self, config: Config = None) -> None:
        """
        Initializes the ConfigEditor with the provided configuration.

        Args:
            config (Config, optional): An instance of the Config class to load initial values from.
        
        Sets up the main window, frames, widgets, and loads configuration values into the widgets.
        """

        # reference to config handler
        self._aw_config = config
        # main window
        self._window = tk.Tk()
        self._window.title(CE_TITLE)
        self._window.geometry(f"{CE_WIDTH}x{CE_HEIGHT}")
        self._window.columnconfigure(0, weight=1)
        self._window.columnconfigure(1, weight=1)

        # FRAMES
        # left column
        self._left_column = tk.LabelFrame(
            master=self._window,
            text="mailer configuration"
        )
        self._left_column.grid(
            column=0,
            row=0,
            sticky="nswe",
            padx=5,
            pady=5
        )

        # right column
        self._right_column = tk.LabelFrame(
            master=self._window,
            text="scheduler configuration"
        )
        self._right_column.grid(
            column=1,
            row=0,
            sticky="nswe",
            padx=5,
            pady=5
        )

        # lower text area
        self._lower_text_area = tk.LabelFrame(
            master=self._window,
            text="messages"
        )
        self._lower_text_area.grid(
            column=0,
            row=1,
            columnspan=2,
            sticky="nswe",
        )

        # left column widgets
        tk.Label(self._left_column, text="login:").grid(
            column=0,
            row=0,
            sticky="w",
            pady=10
        )
        self._login_entry = tk.Entry(self._left_column)
        self._login_entry.grid(column=1, row=0, pady=5)
        self._load_value(self._login_entry, LOGIN)

        tk.Label(self._left_column, text="password:").grid(
            column=0,
            row=1,
            sticky="w",
            pady=10
        )
        self._password_entry = tk.Entry(self._left_column, show="*")
        self._password_entry.grid(column=1, row=1, pady=5)
        self._load_value(self._password_entry, PASSWORD)

        tk.Label(self._left_column, text="recipient:").grid(
            column=0,
            row=2,
            sticky="w",
            pady=10
        )
        self._recipient_entry = tk.Entry(self._left_column)
        self._recipient_entry.grid(column=1, row=2, pady=5)
        self._load_value(self._recipient_entry, RECIPIENT)

        tk.Label(self._left_column, text="server:").grid(
            column=0,
            row=3,
            sticky="w",
            pady=10
        )
        self._server_entry = tk.Entry(self._left_column)
        self._server_entry.grid(column=1, row=3, pady=5)
        self._load_value(self._server_entry, SERVER)

        tk.Label(self._left_column, text="port:").grid(
            column=0,
            row=4,
            sticky="w",
            pady=10
        )
        self._port_entry = tk.Entry(self._left_column)
        self._port_entry.grid(column=1, row=4, pady=5)
        self._load_value(self._port_entry, PORT)

        # right column widgets
        tk.Label(self._right_column, text="time: (format: HH:MM)").grid(
            column=0,
            row=0,
            sticky="w",
            pady=10
        )
        self._time_entry = tk.Entry(self._right_column)
        self._time_entry.grid(column=1, row=0, pady=5)
        self._load_value(self._time_entry, TIME)

        tk.Label(self._right_column, text="weekday:").grid(
            column=0,
            row=1,
            sticky="w",
            pady=10
        )
        self._weekday_cbox = ttk.Combobox(
            master=self._right_column,
            values=[
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday"    
            ],
            state="readonly"
        )
        self._weekday_cbox.grid(column=1, row=1, pady=5)
        self._load_value(self._weekday_cbox, WEEKDAY)

        tk.Label(self._right_column, text="period:").grid(
            column=0,
            row=2,
            sticky="w",
            pady=10
        )
        self._period_cbox = ttk.Combobox(
            master=self._right_column,
            values=[
                "hourly",
                "daily",
                "weekly"
            ],
            state="readonly"
        )
        self._period_cbox.grid(column=1, row=2, pady=5)
        self._load_value(self._period_cbox, PERIOD)

        self._submit_button = tk.Button(
            master=self._right_column,
            text="SAVE",
            command=self._submit
        )
        self._submit_button.grid(column=0, row=4, padx=10, pady=10)

        self._exit_button = tk.Button(
            master=self._right_column,
            text="EXIT",
            command=self._exit
        )
        self._exit_button.grid(column=1, row=4, padx=10, pady=10)

        # lower text area
        self._messages_text_area = tk.Text(
            master=self._lower_text_area,
            height=8
        )
        self._messages_text_area.pack()

    def run(self):
        """
        Starts the Tkinter event loop to display the GUI and handle user interactions.

        This method enters the Tkinter main loop, making the window visible and responsive.
        """
        self._window.mainloop()

    def _load_value(self, widget: tk.Widget, key: str):
        """
        Loads and sets the value of a widget based on the provided configuration key.

        Args:
            widget (tk.Widget): The widget to update with the configuration value.
            key (str): The key to retrieve the value from the configuration.
        
        If the key is not found in the configuration, no changes are made to the widget.
        """
        try:
            widget.insert(0, self._aw_config.get_key(key))
        except KeyError:
            pass

    def _all_entries_valid(self) -> tuple[bool, str]:
        """
        Validates all entry fields in the GUI.

        Returns:
            tuple[bool, str]: A tuple where the first element is a boolean indicating if all entries are valid,
                              and the second element is a message describing any validation errors.
        
        This method checks the validity of each input field using the Validator class and constructs an error message if any field is invalid.
        """
        is_valid = True
        message = ""

        if not Validator.validate_email(self._login_entry.get()):
            is_valid = False
            message += "Login is invalid" if not message else "\nLogin is invalid."

        if not Validator.validate_email(self._recipient_entry.get()):
            is_valid = False
            message += "Recipient is invalid" if not message else "\nRecipient is invalid."

        if not Validator.validate_server(self._server_entry.get()):
            is_valid = False
            message += "Server is invalid" if not message else "\nServer is invalid."

        if not Validator.validate_port(self._port_entry.get()):
            is_valid = False
            message += "Port has to be number." if not message else "\nPort has to be number."

        if not Validator.validate_time(self._time_entry.get()):
            is_valid = False
            message += "Time has to be in HH:DD format." if not message else "\nTime has to be in HH:DD format."

        return (is_valid, message)

    def _submit(self):
        """
        Handles the submission of the configuration form.

        Validates the entries, saves the configuration if all entries are valid, and displays a status message.

        The method updates the configuration with the values from the widgets and displays a success or error message in the text area.
        """
        is_valid, status = self._all_entries_valid()

        if is_valid:
            self._aw_config.set_multiple_keys({
                LOGIN: self._login_entry.get(),
                PASSWORD: self._password_entry.get(),
                RECIPIENT: self._recipient_entry.get(),
                SERVER: self._server_entry.get(),
                PORT: self._port_entry.get(),
                TIME: self._time_entry.get(),
                PERIOD: self._period_cbox.get(),
                WEEKDAY: DAY_TO_INT_MAP[self._weekday_cbox.get()]
            })
            status = "Everything is okay, saved into file."

        self._messages_text_area.delete(1.0, tk.END)
        self._messages_text_area.insert(tk.END, status)

    def _exit(self):
        """
        Handles the exit action for the application.

        If the configuration is valid, the window is closed. If the configuration is not valid, an error message is displayed and the window remains open.
        
        This method checks the validity of the current configuration and determines whether to exit the application or prompt the user to correct the configuration.
        """
        if self._aw_config.is_valid():
            self._window.destroy()
        else:
            self._messages_text_area.delete(1.0, tk.END)
            self._messages_text_area.insert(tk.END, "Exiting aborted, please save valid config.")


if __name__ == '__main__':
    cf = Config()
    ce = ConfigEditor(cf)
    ce.run()
import tkinter as tk
from tkinter import ttk

from aw import CE_WIDTH, CE_HEIGHT, CE_TITLE
from aw import LOGIN, PASSWORD, RECIPIENT, SERVER, PORT, TIME, PERIOD, WEEKDAY
from aw.config import Config
from aw.validator import Validator

class ConfigEditor:
    def __init__(self, config: Config = None) -> None:
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

        tk.Label(self._left_column, text="password:").grid(
            column=0,
            row=1,
            sticky="w",
            pady=10
        )
        self._password_entry = tk.Entry(self._left_column, show="*")
        self._password_entry.grid(column=1, row=1, pady=5)

        tk.Label(self._left_column, text="recipient:").grid(
            column=0,
            row=2,
            sticky="w",
            pady=10
        )
        self._recipient_entry = tk.Entry(self._left_column)
        self._recipient_entry.grid(column=1, row=2, pady=5)

        tk.Label(self._left_column, text="server:").grid(
            column=0,
            row=3,
            sticky="w",
            pady=10
        )
        self._server_entry = tk.Entry(self._left_column)
        self._server_entry.grid(column=1, row=3, pady=5)

        tk.Label(self._left_column, text="port:").grid(
            column=0,
            row=4,
            sticky="w",
            pady=10
        )
        self._port_entry = tk.Entry(self._left_column)
        self._port_entry.grid(column=1, row=4, pady=5)

        # right column widgets
        tk.Label(self._right_column, text="time: (format: HH:MM)").grid(
            column=0,
            row=0,
            sticky="w",
            pady=10
        )
        self._time_entry = tk.Entry(self._right_column)
        self._time_entry.grid(column=1, row=0, pady=5)

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

        self._submit_button = tk.Button(
            master=self._right_column,
            text="SAVE",
            command=self._submit
        )
        self._submit_button.grid(column=0, row=4, padx=10, pady=10)

        self._exit_button = tk.Button(
            master=self._right_column,
            text="EXIT"
        )
        self._exit_button.grid(column=1, row=4, padx=10, pady=10)

        # lower text area
        self._messages_text_area = tk.Text(
            master=self._lower_text_area,
            height=8
        )
        self._messages_text_area.pack()

    def run(self):
        self._window.mainloop()

    def _all_entries_valid(self) -> tuple[bool, str]:
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
        is_valid, status = self._all_entries_valid()

        if is_valid:
            self._aw_config.set_multiple_keys({
                LOGIN: self._login_entry.get(),
                PASSWORD: self._password_entry.get(),
                RECIPIENT: self._recipient_entry.get(),
                SERVER: self._recipient_entry.get(),
                PORT: self._port_entry.get(),
                TIME: self._time_entry.get(),
                PERIOD: self._period_cbox.get(),
                WEEKDAY: self._weekday_cbox.get()
            })
            status = "Everything is okay, saved into file."

        self._messages_text_area.delete(1.0, tk.END)
        self._messages_text_area.insert(tk.END, status)

if __name__ == '__main__':
    cf = Config()
    ce = ConfigEditor(cf)
    ce.run()
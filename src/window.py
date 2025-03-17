import threading, socket
import TKinterModernThemes as tkmt
from TKinterModernThemes.WidgetFrame import Widget
from PIL import ImageTk, Image
import tkinter as tk
import qrcode
from src.server import run_server

stop_event = threading.Event()
server_thread = threading.Thread(target=run_server, args=("0.0.0.0", "9999", stop_event))
is_server_running = False

host = socket.gethostbyname_ex(socket.getfqdn())[2][0]


class App(tkmt.ThemedTKinterFrame):
    def __init__(self):
        super().__init__("Remote Wheel Desktop", "azure")

        self.bind_port = tk.StringVar(value="9999")
        # self.bind_port.trace_add("write", self.change_host)
        self.bind_port_input = self.addLabelFrame("Port").Entry(textvariable=self.bind_port)
        # self.bind_port_input.bind("<Return>", self.change_port)
        # self.bind_port_input.insert(0, self.bind_port)

        self.run_btn = self.Button("Start server", self.toggle_server)

        self.host_label = self.Label("")

        self.qr_img: ImageTk.PhotoImage
        self.qr_label = self.Label("")

        self.run()

    def toggle_server(self):
        global is_server_running, server_thread
        if is_server_running:
            stop_event.set()
            server_thread.join()
            self.run_btn.config(text="Start server")
            is_server_running = False
        else:
            stop_event.clear()
            server_thread = threading.Thread(target=run_server, args=("0.0.0.0", int(self.bind_port.get()), stop_event))
            server_thread.start()
            self.run_btn.config(text="Stop server")
            is_server_running = True

            # change label and qr code
            bind_port = self.bind_port.get()
            qrcode.make(f"{host}:{bind_port}").save("qr.png")
            self.qr_img = ImageTk.PhotoImage(Image.open("qr.png").resize((200, 200)))
            self.qr_label.config(image=self.qr_img)
            self.host_label.config(text=f"{host}:{bind_port}")

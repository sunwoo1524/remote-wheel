import vgamepad as vg
import socket


def run_server(bind_ip: str, bind_port: int, stop_event):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)
    server.settimeout(1)

    print(f"TCP server has been started on {bind_port}!")

    gamepad = vg.VX360Gamepad()

    while True:
        try:
            client, addr = server.accept()
        except socket.timeout:
            if stop_event.is_set():
                print("Server stopping...")
                return
            continue

        try:
            print("New client")

            while True:
                if stop_event.is_set():
                    print("Server stopping...")
                    return

                data = client.recv(1024).decode("utf-8")

                if data: # emulate gamepad input
                    [steer, is_accel, is_break] = data.split("*")[0].split("r")
                    steer = float(steer); is_accel = int(is_accel); is_break = int(is_break)

                    gamepad.left_joystick(x_value=int(steer * 364.07), y_value=0)
                    gamepad.right_trigger_float(value_float=is_accel)
                    gamepad.left_trigger_float(value_float=is_break)

                    gamepad.update()
                if not data:
                    break
        finally:
            client.close()

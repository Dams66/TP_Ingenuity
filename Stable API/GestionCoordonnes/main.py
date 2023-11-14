#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  GestionCoordonnes version 1.0
#  Created by Ingenuity i/o on 2023/10/20
#

import sys
import ingescape as igs

image_width = 350.0
image_height = 350.0
tab_length = 1200.0
tab_height = 900.0
spacing_h = 10.0
spacing_v = 10.0

gestionTableau = []


def input_callback(iop_type, name, value_type, value, my_data):
    if value == "":
        gestionTableau.clear()

def service_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    url = arguments[0]
    x, y = coordLibres()
    gestionTableau.append((x, y))
    arguments_list = (url, x, y)
    igs.service_call("StableDiffusion", "send_x_y", arguments_list, "")

def coordLibres():
    global gestionTableau

    if not gestionTableau:
        x = 100.0
        y = 100.0
    else:
        last_x, last_y = gestionTableau[-1]
        x = last_x + spacing_h + image_width
        y = last_y
        if (x + image_width) > tab_length:
            x = 100.0
            y = y + spacing_v + image_height
            if (y + image_height) > tab_height:
                igs.service_call("Whiteboard", "clear", (), "")
                x = 100.0
                y = 100.0
    return x, y

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)

    igs.agent_set_name(sys.argv[1])
    igs.definition_set_version("1.0")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.service_init("placeLibre", service_callback, None)
    igs.service_arg_add("placeLibre", "url", igs.STRING_T)
    igs.input_create("lastAction", igs.STRING_T, None)
    igs.observe_input("lastAction", input_callback, None)
    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

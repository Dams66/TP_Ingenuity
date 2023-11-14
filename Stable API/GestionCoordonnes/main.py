#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  GestionCoordonnes version 1.0
#  Created by Ingenuity i/o on 2023/10/20
#

from Image import Image
from TabImages import TabImages
import sys
import time
import ingescape as igs

gestionTableau = TabImages()

def service_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    # Recup données
    url = arguments[0]
    x, y = coordLibres()
    # Création d'un objet image
    new_img = Image(x, y, url, time.time())
    # Ajout de l'image dans le tableau
    gestionTableau.addImgToList(new_img)
    # Renvoie les coordonées x, y et url
    arguments_list = (url, x, y)
    igs.service_call("StableDiffusion", "send_x_y", arguments_list, "")


def coordLibres():
    global gestionTableau

    if not gestionTableau:
        x = 100.0
        y = 100.0
    else:
        last_x, last_y, _ = gestionTableau[-1]
        x = last_x + gestionTableau.spacing_h + gestionTableau.image_width
        y = last_y
        if (x + gestionTableau.image_width) > gestionTableau.tab_length:
            x = 100.0
            y = y + gestionTableau.spacing_v + gestionTableau.image_height
            if (y + gestionTableau.image_height) > gestionTableau.tab_height:
                igs.service_call("Whiteboard", "clear", (), "")
                x = 100.0
                y = 100.0
    return x, y

def checkTimeout():
    listTimeOut = []
    for img in gestionTableau.listImages:
        if isinstance(img, Image):
            if time.time() - img.start_time > gestionTableau.timeout:
                listTimeOut.append(img)
        else:
            print("Error")
    return listTimeOut

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

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

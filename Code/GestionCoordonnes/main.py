#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  GestionCoordonnes version 1.0
#  Created by Ingenuity i/o on 2023/10/20
#

from Image import Image
from TabImages import TabImages
import time
import sys
import ingescape as igs

gestionTableau = TabImages(x_init=50.0, y_init=50.0, image_width=250.0, image_height=250.0, tab_width=1100.0,
                           tab_height=650.0, spacing_h=10.0, spacing_v=10.0, ordering=True, timeout=90.0)


def input_callback(iop_type, name, value_type, value, my_data):
    gestionTableau.ordering = value
def input_callback_2(iop_type, name, value_type, value, my_data):
    gestionTableau.timeout = value

def service_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    # Recup données
    url = arguments[0]
    x, y = gestionTableau.closerFree()
    # Création d'un objet image
    new_img = Image(x, y, url, time.time())
    # Ajout de l'image dans le tableau
    gestionTableau.addImgToList(new_img)


# Service pour afficher les images contenues dans la liste
def service_callback2(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    gestionTableau.deleteTimeout()
    igs.service_call("Whiteboard", "clear", (), "")
    gestionTableau.order()
    for img in gestionTableau.listImages:
        argument_list = (img.url, img.x, img.y)
        igs.service_call("Whiteboard", "addImageFromUrl", argument_list, "")
    igs.service_call("StableDiffusion", "ReFreshTab", (), "")


def service_callback3(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    return 1


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

    igs.input_create("Ordering", igs.BOOL_T, None)
    igs.input_create("Timeout_image", igs.INTEGER_T, None)

    igs.observe_input("Ordering", input_callback, None)
    igs.observe_input("Timeout_image", input_callback_2, None)

    igs.service_init("addImageToTab", service_callback, None)
    igs.service_arg_add("addImageToTab", "url", igs.STRING_T)

    igs.service_init("displayAll", service_callback2, None)

    igs.service_init("elementCreated", service_callback3, None)
    igs.service_arg_add("elementCreated", "elementID", igs.INTEGER_T)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

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

gestionTableau = TabImages()

def service_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    # Recup données
    url = arguments[0]
    x, y = gestionTableau.closerFree()
    # Création d'un objet image
    new_img = Image(x, y, url, time.time())
    # Ajout de l'image dans le tableau
    gestionTableau.addImgToList(new_img)

#Service pour afficher les images contenues dans la liste
def service_callback2(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    gestionTableau.deleteTimeout()
    igs.service_call("Whiteboard", "clear", (), "")
    for img in gestionTableau.listImages:
        argument_list = (img.url, img.x, img.y)
        igs.service_call("Whiteboard", "addImageFromUrl", argument_list, "")
    igs.service_call("GestionTemporelle", "refreshImg", (), "")


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

    igs.service_init("addImageToTab", service_callback, None)
    igs.service_arg_add("addImageToTab", "url", igs.STRING_T)

    igs.service_init("displayAll", service_callback2, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

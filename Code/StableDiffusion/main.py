#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  StableDiffusion version 1.0
#  Created by Ingenuity i/o on 2023/10/20
#

import random
import sys
import ingescape as igs
import time
import json
import requests

timeBetweenRefresh = 10  # 10 secondes
listRandomIMG = [
    "https://pub-3626123a908346a7a8be8d9295f44e26.r2.dev/generations/ba818405-efeb-473f-b2e1-3fd37f551ca5-0.png",
    "https://cdn2.stablediffusionapi.com/generations/f57c1d16-8d14-4dc1-a1b5-e8db5d8614b3-0.png",
    "https://pub-3626123a908346a7a8be8d9295f44e26.r2.dev/generations/94a92db0-97f4-4764-ab35-d938a06879dd-0.png"]
apiKey = None
first = True


# inputs
def input_callback(iop_type, name, value_type, value, my_data):
    global first
    if apiKey is not None:
        if value.lower() == "random":
            url = randomIMG()
        else:
            url = text2img(value, apiKey)
        igs.output_set_string("url-image", url)

        if url != "":
            # Récupération des coordonnées libres
            argument_list = (url,)
            igs.service_call("GestionCoordonnes", "addImageToTab", argument_list, "")
            if first:
                igs.service_call("GestionCoordonnes", "displayAll", (), "")
                first = False


def input_callback_2(iop_type, name, value_type, value, my_data):
    global apiKey
    apiKey = value

def input_callback_3(iop_type, name, value_type, value, my_data):
    global timeBetweenRefresh
    timeBetweenRefresh = value


def service_callback(sender_agent_name, sender_agent_uuid, service_name, arguments, token, my_data):
    time.sleep(timeBetweenRefresh)
    igs.service_call("GestionCoordonnes", "displayAll", (), "")


def randomIMG():
    return random.choice(listRandomIMG)


def text2img(prompt, cle):
    url = "https://stablediffusionapi.com/api/v3/text2img"
    payload = json.dumps({
        "key": cle,
        "prompt": prompt,
        "negative_prompt": None,
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "20",
        "seed": None,
        "guidance_scale": 7.5,
        "safety_checker": "yes",
        "multi_lingual": "no",
        "panorama": "no",
        "self_attention": "no",
        "upscale": "no",
        "embeddings_model": None,
        "webhook": None,
        "track_id": None
    })
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
        json_response = response.json()
        output_link = json_response.get("output", [])[0]
        return output_link
    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite lors de la requête : {e}")
        return ""

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

    igs.service_init("ReFreshTab", service_callback, None)

    igs.input_create("prompt", igs.STRING_T, None)
    igs.input_create("cle_API", igs.STRING_T, None)
    igs.input_create("Refresh_Rate", igs.INTEGER_T, None)

    igs.output_create("url-image", igs.STRING_T, None)

    igs.observe_input("prompt", input_callback, None)
    igs.observe_input("cle_API", input_callback_2, None)
    igs.observe_input("Refresh_Rate", input_callback_3, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

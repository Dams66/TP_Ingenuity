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
from PIL import Image
from io import BytesIO

clientID = "f5ba40718baa4ba"
timeBetweenRefresh = 10  # 10 secondes
listRandomIMG = ["https://i.imgur.com/6Pu4w3k.png",  # Elisabeth
                 "https://i.imgur.com/QnJitU0.png",  # Naruto
                 "https://i.imgur.com/hrEYqX5.png",  # Escanor
                 "https://i.imgur.com/fGS95C4.png",  # Chat + plats
                 "https://i.imgur.com/XBGVFR8.png",  # Lynx
                 "https://i.imgur.com/6OkEr9k.png",  # Satoru Gojo
                 "https://i.imgur.com/BDDVb2n.png",  # Paris
                 "https://i.imgur.com/UUjQV2M.png",  # Shibuya Ville
                 "https://i.imgur.com/yaDLxy5.png",  # Loup
                 "https://i.imgur.com/o6WF6Er.png",  # LasVegas
                 "https://i.imgur.com/KCgP4y5.png",  # MacDo
                 "https://i.imgur.com/eH46XVk.png"]  # Plat Gastronomique
apiKey = None
first = True


# inputs
def input_callback(iop_type, name, value_type, value, my_data):
    global first
    if apiKey is not None:
        if value.lower() == "random":
            urlResized = randomIMG()
        else:
            url = text2img(value, apiKey)
            urlResized = resizeAndUpload(200, 200, url, clientID)

        if (urlResized != "") and (urlResized is not None):
            igs.output_set_string("url-image", urlResized)
            # Récupération des coordonnées libres
            argument_list = (urlResized,)
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
        "width": "1024",
        "height": "1024",
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
        print(f"Une erreur s'est produite lors de la requête Stable Diffusion: {e}")
        return ""
    except IndexError:
        print("La réponse de StableDiffusion est vide. Cela peut etre dû au fait que la clé API n'est pas valide ou qu'il n'y ai plus de crédits.")
        return ""


def resizeAndUpload(largeur, hauteur, url, client_id):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        new_size = (largeur, hauteur)
        img_resized = img.resize(new_size)

        with BytesIO() as buffer:
            img_resized.save(buffer, format="PNG")
            image_data = buffer.getvalue()

        upload_url = "https://api.imgur.com/3/image"
        headers = {"Authorization": f"Client-ID {client_id}"}
        files = {"image": image_data}

        response = requests.post(upload_url, headers=headers, files=files)

        json_response = response.json()

        if response.status_code == 200 and json_response["success"]:
            print("Image téléversée avec succès !")
            print("URL de l'image sur Imgur:", json_response["data"]["link"])
            return json_response["data"]["link"]
        else:
            print("Échec du téléversement. Réponse Imgur:", json_response)

    except Exception as e:
        print(f"Une erreur s'est produite lors du resizeAndUpload: {e}")


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

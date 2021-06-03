import speech_recognition as sr
import pyttsx3
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import wikipedia
import webbrowser
import googleTasks
# import googleCalendar

listener = sr.Recognizer()
tenchaBot = pyttsx3.init()
voices = tenchaBot.getProperty("voices")


exceptionActive = True
close = False
device = ""
deviceNOTETrabajo = "eadee7bd33e90ea24b0173baef7140db2999ef6a"
deviceCeluNao = "add0b31febd5f331912ba458a79f7d1484694217"


def talkBot(text, language=3):
    tenchaBot.setProperty("voice", voices[language].id)
    tenchaBot.setProperty("rate", 150)
    tenchaBot.say(text)
    tenchaBot.runAndWait()


talkBot("Buenas noches Naoto. ¿Qué puedo hacer por ti?")
print("Running ...")


def exceptionAction(accion):
    global exceptionActive
    if accion:
        exceptionActive = True
    else:
        exceptionActive = False


def searchWikipedia(query):
    wikipedia.set_lang("es")
    info = wikipedia.summary(query, 1)
    talkBot("Esto fue lo que encontré en wikipedia")
    talkBot(info)


def openChrome(query):
    url = 'www.google.com'
    webbrowser.register('chrome',
                        None,
                        webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe"))
    webbrowser.get('chrome').open(url)


def spotifyAction(scopeAction, action, query=""):
    print("Entra la acción", scopeAction, action)
    global device
    cid = '8ac30afb6fe3457db697712e48804337'
    secret = '4c071e2c7179449b983882f6b0f69ae6'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid,
                                                   client_secret=secret,
                                                   redirect_uri="http://localhost:2020",
                                                   scope=scopeAction))
    query = query.lstrip().rstrip()
    if action == "start":
        sp.start_playback(device_id=device)
    elif action == "stop":
        sp.pause_playback(device_id=device)
    elif action == "next":
        sp.next_track(device_id=device)
    elif action == "search":
        spAux = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid,
                                                          client_secret=secret,
                                                          redirect_uri="http://localhost:2020",
                                                          scope="user-read-private"))
        search = spAux.search(q=query, type="playlist")
        idPlayList = search["playlists"]["items"][0]["id"]
        stringFullUri = "spotify:playlist:"+str(idPlayList)
        talkBot("Reproduciendo "+query)
        sp.start_playback(device_id=device, context_uri=stringFullUri)
    elif action == "devices":
        devices = sp.devices()
        print(devices)
    elif action == "change":
        sp.transfer_playback(device_id=device, force_play=True)


def generalConversation(command):
    file = open("generalAnswer.json", encoding='utf-8')
    #file = open("\generalAnswer.json", encoding='utf-8')
    data = json.load(file)
    communication = data["communication"]
    foundAnswer = False
    print(command)
    for i in communication:
        if i["k"].find(command) != -1 or command.find(i["k"]) != -1:
            talkBot(i["a"])
            # print(i["o"])
            # if i["o"] in vars(__builtins__)
            #     talkBot(i["o"])
            foundAnswer = True
    if not foundAnswer:
        talkBot("Aún no he sido programada para esa respuesta")


def getHumanExpression():
    try:
        with sr.Microphone() as source:
            print("Listening ...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language="es-ES")
            command = command.lower()
            return command
    except Exception as e:
        print(e)
        if exceptionActive:
            talkBot(e)


def run_tenchabot():
    try:
        command = getHumanExpression()
        # with sr.Microphone() as source:
        #     print("Listening ...")
        #     voice = listener.listen(source)
        #     command = listener.recognize_google(voice, language="es-ES")
        #     command = command.lower()
        #     print(command)
        try:
            if "spotify" in command:
                command = command.replace("spotify", "")
                print("ejecutando comando spotify if clause", command)
                if "iniciar" in command or "escuchar" in command:
                    command = command.replace("iniciar", "")
                    spotifyAction("user-modify-playback-state", "start")
                elif "pausar" in command:
                    command = command.replace("parar", "")
                    command = command.replace("pausar", "")
                    spotifyAction("user-modify-playback-state", "stop")
                elif "buscar" in command:
                    command = command.replace("buscar", "")
                    spotifyAction(
                        "user-modify-playback-state", "search", command)
                elif "siguiente" in command:
                    command = command.replace("siguiente", "")
                    spotifyAction("user-modify-playback-state", "next")
                elif "dispositivos" in command:
                    command = command.replace("dispositivos", "")
                    spotifyAction("user-read-playback-state", "devices")
                elif "cambiar" in command:
                    command = command.replace("escuchar", "")
                    global device
                    if "celular" in command:
                        command = command.replace("celular", "")
                        device = deviceCeluNao
                    else:
                        device = deviceNOTETrabajo
                    spotifyAction("user-modify-playback-state", "change")
                else:
                    talkBot(
                        "No he podido entender lo que necesitas en spotify. ¿Qué quieres hacer?")
            elif "mostrar errores" in command:
                talkBot("Los errores serán visibles")
                command = command.replace("mostrar errores", "")
                exceptionAction(True)
            elif "ocultar errores" in command:
                talkBot("Los errores serán ocultados")
                command = command.replace("ocultar errores", "")
                exceptionAction(False)
            elif "cerrar" in command:
                global close
                close = True
            elif "wikipedia" in command:
                command = command.replace("wikipedia", "")
                searchWikipedia(command)
            elif "abrir chrome" in command:
                talkBot("Abriendo google chrome")
                command = command.replace("abrir chrome", "")
                openChrome(command)
            elif "calendario" in command:
                googleCalendar.main()
            elif "tareas de google" in command:
                command = command.replace("tareas de google", "")
                lists = googleTasks.getLists()
                print(lists)
                if not lists:
                    talkBot("NO he encontrado lista de tareas")
                else:
                    talkBot("He encontrado las siguientes listas")
                    for l in lists:
                        talkBot(l["title"])
                    talkBot("¿Cuál deseas administrar?")
                    command2 = getHumanExpression()
                    print(command2)
                    listSelected = {}
                    for l2 in lists:
                        if l2["title"].lower() == command2:
                            listSelected = l2["id"]
                            break
                    if not listSelected:
                        talkBot("No he podido encontrar la lista")
                    else:
                        talkBot("El id de la lista encontrada es "+listSelected)
            else:
                generalConversation(command)
        except Exception as e:
            talkBot("Ha ocurido un error")
            if exceptionActive:
                talkBot(e, 1)
            print(e)
            print("comando caido")
            pass
    except Exception as e:
        if exceptionActive:
            talkBot(e, 1)
        print(e)
        print("app caida")
        pass


while not close:
    run_tenchabot()

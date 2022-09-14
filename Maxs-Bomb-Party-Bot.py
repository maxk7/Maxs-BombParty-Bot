# -*- coding: utf-8 -*-
# Author: Max Konzerowsky
# Date: 2022-09-14

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import ast
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.common
import re
import os
import shutil
import keyboard
import math
from sys import platform
###############
#  S E T U P  #
###############

word_file = open("words.txt", "r+")
word_list: list[str] = word_file.read().split("\n")
word_file.close()
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
            "v", "w", "x", "y", "z"]
shuffle_count = 0
chrm_options = Options()
chrm_caps = webdriver.DesiredCapabilities.CHROME.copy()

chrm_caps['goog:loggingPrefs'] = {'performance': 'ALL'}

if platform == "linux" or platform == "linux2" or platform == "darwin":
    driver = webdriver.Chrome(executable_path=f'{os.path.dirname(__file__)}/chromedriver', chrome_options=chrm_options,
                              desired_capabilities=chrm_caps)
elif platform == "win32":
    driver = webdriver.Chrome(executable_path=f'{os.path.dirname(__file__)}chromedriver.exe', chrome_options=chrm_options,
                              desired_capabilities=chrm_caps)

global nickname, played_words, text_area, last_word, peerId, acceptable_words, syllable


# Load and Connect Driver to JKLM
def connectDriver():
    url = f"https://jklm.fun"
    driver.get(url)


# We should only run the script when driver.current_url has a valid code

def determineAutomation():
    # Determine Bot Automation (Default False)
    if input("Automate? [y/n]: ").lower() == "y":
        shouldAutomate = True
        if input("Instaplay? [y/n]: ").lower() == "y":
            shouldInstaplay = True
        else:
            shouldInstaplay = False
    else:
        shouldAutomate = False
        shouldInstaplay = False

    return shouldAutomate, shouldInstaplay


def generateAcceptableWords(generateAcceptableWordsSyllable):
    start = time.time()
    acceptable_words_temp: list[str] = []

    for word in word_list:
        if generateAcceptableWordsSyllable in word:
            if word not in played_words:
                acceptable_words_temp.append(word)

    end = time.time()
    total_time_temp = end - start

    return acceptable_words_temp, total_time_temp


def typeSleep(letterID: int):
    """f letterID < 4:
        time.sleep(random.randrange(3, 9) / 100)
    elif letterID == 6:
        time.sleep(random.randrange(1, 3) / 10)
    elif letterID < 8:
        time.sleep(random.randrange(1, 2) / 10)
    elif letterID == 10:
        time.sleep(random.randrange(1, 3) / 10)
    else:
        time.sleep(random.randrange(3, 9) / 100)"""

    x = int(letterID)
    sleep_equation = (abs((1.6 * math.sin(0.8 * x + (math.pi - 2.4))) / 10) + 0.1)
    random_sleep = round(random.uniform(0.4 * sleep_equation, 0.7 * sleep_equation), 3)
    time.sleep(random_sleep)


def typeWord(word):
    if len(word) != 0:
        exit_typeword = False
        start = time.time()

        sleep_amount = len(word) ** (1 / 4.6) - 0.85

        sleep_amount += 0.033 * len(syllable)
        sleep_amount += 0.088 * word.count("j")
        sleep_amount += 0.088 * word.count("k")
        sleep_amount += 0.088 * word.count("q")
        sleep_amount += 0.088 * word.count("z")

        time.sleep(sleep_amount)
        wordLetter = 1

        # Typeing the letter
        for letter in word:
            random_temp = random.randrange(0, 1000)

            if random_temp < 9990:
                text_area.send_keys(letter)
                typeSleep(wordLetter)

            end = time.time()
            total_time_temp = end - start

            # Mistype letters
            if total_time_temp < 4.3:
                sleep_equation = 0.3 * math.sqrt(4.5 - total_time_temp)
                sleep_amount = random.uniform(0.5 * sleep_equation, sleep_equation)
                # Mistype 1 Letter 0.5% Chance
                if 9990 <= random_temp < 9995:
                    text_area.send_keys(random.choice(alphabet))
                    text_area.send_keys(Keys.BACKSPACE)

                    time.sleep(round(int(sleep_amount), 3))

                    text_area.send_keys(letter)
                    typeSleep(wordLetter)

                # Mistype 2 Letters 0.5% Chance
                elif 9995 <= random_temp < 1000:
                    text_area.send_keys(random.choice(alphabet))
                    typeSleep(wordLetter)
                    text_area.send_keys(random.choice(alphabet))
                    typeSleep(wordLetter + 1)

                    time.sleep(round(int(sleep_amount), 3))

                    text_area.send_keys(Keys.BACKSPACE)
                    time.sleep(0.1)
                    text_area.send_keys(Keys.BACKSPACE)

                    typeSleep(wordLetter)
                    text_area.send_keys(letter)

                    typeSleep(wordLetter)

                wordLetter += 1

            # Exit the program
            if keyboard.is_pressed("]"):
                time.sleep(0.25)
                exit_typeword = True
                break

        end = time.time()
        total_time_temp = end - start

        if not exit_typeword:
            random_temp = random.randrange(0, 10)
            if total_time_temp < 4.5:
                if random_temp < 2 and len(word) > 12:
                    time.sleep(0.2)
                    text_area.send_keys("?")

                    sleep_equation = (0.17 * math.sqrt(4.55 - total_time_temp)) ** (1 / 1.6)
                    sleep_amount = random.uniform(0.7 * sleep_equation, sleep_equation)
                    time.sleep(sleep_amount)
            elif total_time_temp < 4.55:
                sleep_equation = (0.17 * math.sqrt(4.55 - total_time_temp)) ** (1 / 1.6)
                sleep_amount = random.uniform(0.7 * sleep_equation, sleep_equation)
                time.sleep(sleep_amount)

            text_area.send_keys(Keys.ENTER)
            return True
        else:
            print(f"╘=> Autotype canceled.\n")
            return False


def addToDictionary(word):
    with open("words.txt", "a+") as file:
        file.write(word + "\n")

    word_list.append(word)


def handleCorrectWord(handle_correct_word_payload):
    if last_word != "":
        if peerId == handle_correct_word_payload["peerId"]:
            try:
                played_words.append(acceptable_words[0])

                if last_word not in word_list:
                    print(f"correctWordEvent")
                    addToDictionary(last_word)
                    print(f"╘=> [✅] Added {last_word} to dictionary!\n")

            except IndexError:
                pass

        else:
            random_temp = random.randrange(0, 10)
            if random_temp < 6:
                print(f"correctWordEvent")
                played_words.append(last_word)
                if random_temp < 3:
                    if last_word not in word_list:
                        print(f"╞=> Remembered {last_word} was played.")
                        addToDictionary(last_word)
                        print(f"╘=>  [✅] Added {last_word} to dictionary!\n")
                else:
                    print(f"╘=> Remembered {last_word} was played.\n")


def handleRoomEntry(handle_room_entry_payload):
    print(f"joinRoom")
    handle_room_entry_peerId = handle_room_entry_payload["selfPeerId"]
    room_code = handle_room_entry_payload["roomCode"]
    print(f"╘=> [✅] You joined {room_code} as {handle_room_entry_peerId}\n")
    return handle_room_entry_peerId


def handleFailWord(handle_fail_word_payload):
    print("failWordYourself")

    if not automate:
        if handle_fail_word_payload["reason"] == "mustContainSyllable":
            print(f"╞=> autotyping!")
            try:
                temp_result_2 = typeWord(acceptable_words[0])
                if temp_result_2:
                    print(f"╘=> [✅] Successfully autotyped {acceptable_words[0]}\n")
                else:
                    print(f"╘=> Autotype canceled.\n")
            except selenium.common.exceptions.ElementNotInteractableException:
                print(f"╘=> [❌] Failed to type {acceptable_words[0]}!\n")

    if handle_fail_word_payload["reason"] == "notInDictionary":
        if last_word in word_list:
            print(f"╞=> [/!\\] {last_word} not in dictionary!")
            word_list.remove(last_word)
            acceptable_words.remove(last_word)

            if last_word != "":
                with open("words.txt", "r") as temp_input:
                    with open("words_temp.txt", "w") as output:
                        for line in temp_input:
                            line = line.replace(last_word + "\n", "")
                            output.write(line)

                # replace file with original name
                os.replace('words_temp.txt', 'words.txt')

                print(f"╘=> Removed word from the dictionary!\n")

        else:
            print(f"╘=> [/!\\] {last_word} not in dictionary!\n")

    if handle_fail_word_payload["reason"] == "alreadyUsed":
        if automate:
            print(f"╞=> [/!\\] Word already used!")
            try:
                acceptable_words.remove(last_word)
                if len(acceptable_words) != 0:
                    temp_result_2 = typeWord(acceptable_words[0])
                    if temp_result_2:
                        print(f"╘=> Successfully played {acceptable_words[0]}!\n")
                    else:
                        print(f"╘=> Autotype canceled.\n")
                else:
                    print(f"╘=> [/!\\] Unable to play.\n")
            except:
                print(f"╘=> [/!\\] Failed to play.\n")


def checkGameUpdate(check_game_update_peerId):
    """
    (update, payload)

    Updates:
    syllable, {"syllable": syllable}
    add_player_peer, {"peerId": peerId, "nickname": nickname, "language", language, "auth": auth, "roles": roles}
    add_player_yourself, {"peerId": peerId, "nickname": nickname, "language", language, "auth": auth, "roles": roles}
    join, {"roomCode: roomCode, "userToken": userToken, "nickname": nickname, "language": language}
    :return:
    """

    ws_update = ""
    ws_payload = ""

    for wsData in driver.get_log('performance'):
        # print(wsData)
        wsJson = json.loads((wsData['message']))

        # RECIEVED
        if wsJson["message"]["method"] == "Network.webSocketFrameReceived":
            payload_data = wsJson["message"]["params"]["response"]["payloadData"]

            """print("Rx :" + str(wsJson["message"]["params"]["timestamp"]) +
                  wsJson["message"]["params"]["response"][
                      "payloadData"])"""

            # SET PLAYER WORD
            if "setPlayerWord" in payload_data:
                ws_update = "setPlayerWord"
                ws_payload = payload_data.split('"')[3]

            # SET NEW ROUND
            elif "setMilestone" in payload_data:
                print(ws_payload)

                if f'"currentPlayerPeerId":{check_game_update_peerId}' in payload_data:
                    ws_update = "setMilestone"
                    ws_payload = ast.literal_eval("{" + payload_data.split("{")[3].replace("}", "").replace(
                        ',"usedWordCount":0,"playerStatesByPeerId":', "}"))
                else:
                    ws_payload = ""

            # YOU JOINED A ROOM
            elif "roomEntry" in payload_data:
                ws_payload = ast.literal_eval(
                    "{" + payload_data.split("{")[2].replace("true", "True").replace("false", "False").replace("}", "")[
                          :-1] + "}")
                check_game_update_peerId = handleRoomEntry(ws_payload)
                ws_update = "roomEntry"  # Set to null, taken care of here
                ws_payload = ""

            # CORRECT WORD
            elif "correctWord" in payload_data:
                ws_payload = ast.literal_eval("{" + payload_data.split("{")[1].replace("playerP", "p")[:-1])
                handleCorrectWord(ws_payload)
                ws_update = ""  # Set to null, taken care of here
                ws_payload = ""

            # SYLLABLE UPDATE
            elif "nextTurn" in payload_data:
                ws_update = "syllable"
                ws_payload = {"syllable": payload_data.split(',')[2].replace('"', "")}
                if str(check_game_update_peerId) in payload_data.split("[")[1]:
                    ws_update = "syllableYourself"

            # PLAYER ADDED
            elif "addPlayer" in payload_data:
                ws_update = "addPlayerPeer"

                if automate:
                    try:
                        time.sleep(0.5)
                        driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[1]/div[1]/button').click()
                    except selenium.common.exceptions.ElementNotInteractableException:
                        pass
                    except selenium.common.exceptions.NoSuchElementException:
                        pass

                try:
                    ws_payload = ast.literal_eval(
                        "{" + payload_data.split("{")[2].replace("null", '""')[:-18].split(',"picture"')[0] + "}")
                    if int(peerId) == int(ws_payload["peerId"]):
                        ws_update = "addPlayerYourself"
                    else:
                        ws_payload = ""
                except SyntaxError:
                    ws_payload = ""

            # FAIL WORD
            elif "failWord" in payload_data:
                payload_data = payload_data.split(",")
                ws_payload = {"peerId": payload_data[1], "reason": payload_data[2][:-1].replace('"', "")}
                if automate:
                    if int(check_game_update_peerId) == int(ws_payload["peerId"]):
                        handleFailWord(ws_payload)

                ws_update = ""  # Set to null, taken care of here
                ws_payload = ""

        # SENT
        if wsJson["message"]["method"] == "Network.webSocketFrameSent":
            payload_data = wsJson["message"]["params"]["response"]["payloadData"]
            '''print("Tx :" + wsJson["message"]["params"]["response"]["payloadData"])'''

            # JOINED ROUND
            '''if "joinRoom" in payload_data:
                ws_update = "join"
                print(payload_data)
                print("{" + payload_data.split("{")[1][:-1])
                ws_payload = ast.literal_eval("{" + payload_data.split("{")[1][:-1].split(',"picture"')[0] + "}")'''

            # LEFT ROUND
            if "leaveRound" in payload_data:
                ws_update = "leave"
                ws_payload = "leave"
                print("You left the round!")

    return ws_update, ws_payload, check_game_update_peerId


# BACKUP DICTIONARY
src_file = "words.txt"
dest_file = "Dictionary Backup//words.txt"

if dest_file == "":
    dest_file = src_file
shutil.copy2(os.path.join(src_file), os.path.join(dest_file))

connectDriver()

profile_settings_file = open("profileSettings.txt", "r")
profile_settings = profile_settings_file.read()
profile_settings_file.close()

print(profile_settings)

while True:
    if len(profile_settings) != 0:
        try:
            scriptArray = """localStorage.setItem("jklmSettings", '""" + profile_settings + """');
                            localStorage.setItem("jklmUserToken", 'Wz6vj8FYneZ8Z2hR');
                            return Array.apply(0, new Array(localStorage.length)).map(function (o, i) { return localStorage.getItem(localStorage.key(i)); }
                            )"""

            result = driver.execute_script(scriptArray)
            driver.refresh()
            print("Loaded Profile!")
            break
        except:
            pass
    else:
        print("No Profile Loaded")
        break

print("trying to connect to text_area")

random.shuffle(word_list)
automate, instaplay = determineAutomation()
played_words = []
last_word = ""
peerId = "default"

while True:
    update, payload, peerId = checkGameUpdate(peerId)

    if update != "":
        if update == "setPlayerWord":
            last_word = re.sub(r'[^a-zA-Z]', '', payload.replace(" ", "").replace("-", "ABCHYPHENXYZ"))
            last_word = last_word.replace("ABCHYPHENXYZ", "-")
        else:
            print(f"{update}")

    if update == "roomEntry":
        time.sleep(0.5)
        while True:
            try:
                driver.switch_to.frame(0)
                text_area = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[2]/form/input')
                print("Connected Successfully")
                break
            except:
                pass

    if "syllable" in update or update == "setMilestone":
        syllable = payload["syllable"]
        acceptable_words, total_time = generateAcceptableWords(syllable)
        print(f"╞=> [✅] Found {len(acceptable_words)} playable answers in {round(total_time, 3)}s!")

        if update == "syllableYourself" or update == "setMilestone":
            print(f"╞=> {acceptable_words[:3]}")

            if automate:
                print("╞=> [!] It's now you're turn!")
                if len(acceptable_words) != 0:
                    if instaplay:
                        text_area.send_keys(acceptable_words[0])
                        time.sleep(random.randrange(10, 30) / 10)
                        text_area.send_keys(Keys.ENTER)
                        print(f"╘=> [✅] Successfully played {acceptable_words[0]}\n")
                    elif not instaplay:
                        temp_result = typeWord(acceptable_words[0])
                        if temp_result:
                            if shuffle_count < 15:
                                random.shuffle(word_list)
                                shuffle_count = 0
                            else:
                                shuffle_count += 1
                            print(f"╘=> [✅] Successfully played {acceptable_words[0]}\n")
                        else:
                            print(f"╘=> Autotype canceled.\n")
                else:
                    print(f"╘=> [!] I'm unable to play on {syllable}\n")
            else:
                print("╘=> [!] It's now you're turn!\n")
        else:
            print(f"╘=> {acceptable_words[:3]}\n")

    elif update == "addPlayer":
        pass

    elif update == "addPlayerYourself":
        print("╞=> You joined the game!")
        played_words = []

        # Reload the dictionarya
        word_file = open("words.txt", "r+")
        word_list: list[str] = word_file.read().split("\n")
        word_file.close()
        print(f"╘=> [✅] Loaded {len(word_list)} words!\n")

    elif update == "removePlayer":
        pass

    elif update == "leave":
        print("╘=> You left the game!\n")

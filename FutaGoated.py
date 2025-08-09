Fimport os
import time
import pymem
import pymem.process
import keyboard
from random import uniform
from pynput.mouse import Controller, Button
from win32gui import GetWindowText, GetForegroundWindow
from offsets import *


colors = [
    "\033[91m",    
    "\033[31m",   
    "\033[91;1m",  
    "\033[31;1m",  
    "\033[91m",
]

RESET = "\033[0m"

def colorful_text(text):
    colored = ""
    for i, char in enumerate(text):
        if char == " ":
            colored += char
        else:
            colored += colors[i % len(colors)] + char
    colored += RESET
    return colored

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

mouse = Controller()

client = Client()
dwEntityList = client.offset('dwEntityList')
dwLocalPlayerPawn = client.offset('dwLocalPlayerPawn')
m_iIDEntIndex = client.get('C_CSPlayerPawnBase', 'm_iIDEntIndex')
m_iTeamNum = client.get('C_BaseEntity', 'm_iTeamNum')
m_iHealth = client.get('C_BaseEntity', 'm_iHealth')

TRIGGER_TOGGLE_KEY = "shift"

def print_colorful_banner(enabled):
    clear_console() 
    print(colorful_text(title))
    status = "ON" if enabled else "OFF"
    print(f"TriggerBot Status: {status}")
    print(f"Press {TRIGGER_TOGGLE_KEY.upper()} to toggle trigger ON/OFF")
    print("Press CTRL+C to exit.\n")

def main():
    try:
        pm = pymem.Pymem("cs2.exe")
        client_base = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
        print("[+] Attached to Counter-Strike 2.")
    except Exception:
        print("[!] Please open Counter-Strike 2 before running this script.")
        exit()

    trigger_enabled = False
    print_colorful_banner(trigger_enabled)

    while True:
        try:

            if keyboard.is_pressed(TRIGGER_TOGGLE_KEY):
                trigger_enabled = not trigger_enabled
                print_colorful_banner(trigger_enabled)
             
                while keyboard.is_pressed(TRIGGER_TOGGLE_KEY):
                    time.sleep(0.1)

            if not trigger_enabled:
                time.sleep(0.1)
                continue

            if GetWindowText(GetForegroundWindow()) != "Counter-Strike 2":
                time.sleep(0.1)
                continue

           
            player = pm.read_longlong(client_base + dwLocalPlayerPawn)
            entity_id = pm.read_int(player + m_iIDEntIndex)

            if entity_id > 0:
                entity_list = pm.read_longlong(client_base + dwEntityList)
                ent_entry = pm.read_longlong(entity_list + 0x8 * (entity_id >> 9) + 0x10)
                entity = pm.read_longlong(ent_entry + 120 * (entity_id & 0x1FF))

                entity_team = pm.read_int(entity + m_iTeamNum)
                player_team = pm.read_int(player + m_iTeamNum)

                if entity_team != player_team:
                    entity_hp = pm.read_int(entity + m_iHealth)
                    if entity_hp > 0:
                        time.sleep(uniform(0.07, 0.12))
                        mouse.press(Button.left)
                        time.sleep(uniform(0.03, 0.06))
                        mouse.release(Button.left)
                        time.sleep(uniform(0.15, 0.25))
            else:
                time.sleep(0.05)

        except KeyboardInterrupt:
            print("\nTriggerBot stopped.")
            break
        except:
            pass

if __name__ == '__main__':
    main()

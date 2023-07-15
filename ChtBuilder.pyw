'''
Dreamcast Cht Builder
By VincentNL 14/07/2023

In order to create a .cht file, this program does examine byte arrays differences
between the original game executable and a modified one.

It has been tested with Retroarch (Flycast core), for any bug reports
feel free to contact me on patreon/VincentNL
'''

import tkinter as tk
from tkinter import filedialog

debug = False

def analyze_files():
    dc = 0x10000   # Dreamcast executable align memory
    root = tk.Tk()
    root.withdraw()

    source_file = filedialog.askopenfilename(title="Select original game executable - i.e. 1ST_READ.bin")
    if not source_file:
        if debug:print("No source file selected.")
        return

    target_file = filedialog.askopenfilename(title="Select patched executable with changes")
    if not target_file:
        if debug:print("No target file selected.")
        return

    log_file = filedialog.asksaveasfilename(title="Save cheat file (.cht)", defaultextension=".cht", filetypes=[("*.cht", "*.cht")])
    if not log_file:
        if debug:print("No log file selected.")
        return

    with open(source_file, 'rb') as source, open(target_file, 'rb') as target, open(log_file, 'w') as log:
        source_data = source.read()
        target_data = target.read()

        differences = 0
        offset = 0
        memory_off = 0

        while offset < len(source_data) and offset < len(target_data):
            source_byte = source_data[offset]
            target_byte = target_data[offset]

            if source_byte != target_byte:
                differences += 1
                value = None
                memory_search_size = None

                if offset + 3 < len(source_data) and offset + 3 < len(target_data):
                    value = int.from_bytes(target_data[offset:offset+4], byteorder='little', signed=False)
                    memory_search_size = 5
                    memory_off = offset
                    offset += 3
                elif offset + 1 < len(source_data) and offset + 1 < len(target_data):
                    value = int.from_bytes(target_data[offset:offset+2], byteorder='little', signed=False)
                    memory_search_size = 4
                    offset += 1
                    memory_off = offset
                else:
                    value = target_byte
                    memory_search_size = 3
                    memory_off = offset

                log.write(f'cheat{differences-1}_address = "{memory_off+dc}"\n'
                          f'cheat{differences-1}_address_bit_position = "0"\n'
                          f'cheat{differences - 1}_big_endian = "false"\n'
                          f'cheat{differences - 1}_cheat_type = "1"\n'
                          f'cheat{differences - 1}_code = "cheat"\n'
                          f'cheat{differences - 1}_desc = "cheat"\n'
                          f'cheat{differences - 1}_enable = "true"\n'
                          f'cheat{differences - 1}_handler = "1"\n'
                          f'cheat{differences - 1}_memory_search_size = "{memory_search_size}"\n'
                          f'cheat{differences - 1}_repeat_add_to_address = "0"\n'
                          f'cheat{differences - 1}_repeat_add_to_value = "0"\n'
                          f'cheat{differences - 1}_repeat_count = "1"\n'
                          f'cheat{differences - 1}_value = "{value}"\n')

            offset += 1

        if differences > 0:
            log.write(f'cheats = "{differences}"')

analyze_files()

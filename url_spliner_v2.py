# -*- coding: utf-8 -*-
import os
import sys
import time
import itertools
import codecs
from colorama import init, Fore, Style

init(autoreset=True)

def print_banner():
    banner = """
           [#] Create By :: nullBr@!N
    
           - FILE SPLITTER & JOINER (UTF-8 Safe) -
             
            """
    print(banner)

def animated_message(message, duration=1):
    symbols = itertools.cycle(["|", "/", "-", "\\", "*"])
    end_time = time.time() + duration
    while time.time() < end_time:
        sys.stdout.write("\r{0}{1} {2}".format(Fore.CYAN, message, next(symbols)))
        sys.stdout.flush()
        time.sleep(0.07)
    print("\n")

def split_file(filename, num_splits, output_directory):
    try:
        if not os.path.isfile(filename):
            print(f"{Fore.RED}Error: The file '{filename}' does not exist.")
            return

        # Count total lines using UTF-8 reading
        total_lines = 0
        with codecs.open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                total_lines += 1

        if num_splits <= 0 or num_splits > total_lines:
            print(f"{Fore.YELLOW}Invalid number of splits. Choose between 1 and {total_lines}.")
            return

        lines_per_file = total_lines // num_splits
        remainder = total_lines % num_splits

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        current_index = 1
        current_count = 0
        lines_this_file = lines_per_file + (1 if current_index <= remainder else 0)
        output_path = os.path.join(output_directory, f"{current_index}.txt")
        out_file = codecs.open(output_path, 'w', encoding='utf-8')

        with codecs.open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                out_file.write(line)
                current_count += 1

                if current_count >= lines_this_file:
                    out_file.close()
                    animated_message(f"Created: {output_path}", 1.0)
                    print(f"{Fore.GREEN}Done: {output_path}")

                    current_index += 1
                    if current_index > num_splits:
                        break

                    lines_this_file = lines_per_file + (1 if current_index <= remainder else 0)
                    output_path = os.path.join(output_directory, f"{current_index}.txt")
                    out_file = codecs.open(output_path, 'w', encoding='utf-8')
                    current_count = 0

        if out_file:
            out_file.close()

    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")

def join_files(input_directory, output_filename):
    try:
        if not os.path.isdir(input_directory):
            print(f"{Fore.RED}Error: The directory '{input_directory}' does not exist.")
            return

        files = sorted(f for f in os.listdir(input_directory) if f.endswith(".txt"))
        if not files:
            print(f"{Fore.YELLOW}No .txt files found in '{input_directory}'.")
            return

        with codecs.open(output_filename, 'w', encoding='utf-8') as outfile:
            for i, file in enumerate(files):
                file_path = os.path.join(input_directory, file)
                with codecs.open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                    lines = infile.readlines()

                    # Filter out blank lines
                    non_blank_lines = [line for line in lines if line.strip()]

                    # Write filtered lines
                    for line in non_blank_lines:
                        outfile.write(line.rstrip() + "\n")  # Ensure single newline per line

                animated_message(f"Merged: {file}", 0.5)
                print(f"{Fore.GREEN}Merged: {file}")

        print(f"\n{Fore.CYAN}✔ Done! All files merged into: {output_filename} (blank lines removed)")

    except Exception as e:
        print(f"{Fore.RED}Error during merge: {str(e)}")


def main():
    print_banner()

    try:
        choice = input(f"{Fore.YELLOW}Do you want to [S]plit or [J]oin files? (S/J): {Fore.RESET}").strip().lower()

        if choice == 's':
            filename = "combo.txt" #input(f"{Fore.CYAN}Enter file to split: {Fore.RESET}").strip()
            output_directory = "report" # input(f"{Fore.CYAN}Enter output folder name: {Fore.RESET}").strip()
            num_splits = input(f"{Fore.CYAN}Enter number of splits: {Fore.RESET}").strip()

            if not num_splits.isdigit():
                print(f"{Fore.RED}Error: Please enter a valid number.")
                return

            num_splits = int(num_splits)
            animated_message("Starting split", 2.0)
            split_file(filename, num_splits, output_directory)

        elif choice == 'j':
            input_directory = "report" #input(f"{Fore.CYAN}Enter folder with split files: {Fore.RESET}").strip()
            output_filename = "list_new.txt" #input(f"{Fore.CYAN}Enter output filename (e.g., file.txt): {Fore.RESET}").strip()
            animated_message("Joining files", 2.0)
            join_files(input_directory, output_filename)

        else:
            print(f"{Fore.RED}Invalid option selected.")

    except Exception as e:
        print(f"{Fore.RED}Unexpected Error: {str(e)}")

    input(f"{Fore.MAGENTA}\nPress Enter to exit...{Fore.RESET}")

if __name__ == "__main__":
    main()

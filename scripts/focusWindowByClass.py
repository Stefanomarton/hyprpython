import pickle
from pathlib import Path
import sys
import argparse

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

# Import the module from the parent directory
import hyprpython.hyprpyton as hp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("window_class", help="cycle focus to windows with window_class")
    args = parser.parse_args()

    client = hp.Clients.get()
    client_ordered = client.byFocusID()
    current_window = client.focused()

    emacs_windows = [
        windows
        for windows in client_ordered.list
        if windows.wm_class == args.window_class
    ]

    focus_list = [w for w in emacs_windows if w.workspace.id > 0]

    if current_window.wm_class != args.window_class:
        with open(f"/tmp/{args.window_class}.pkl", "w") as file:
            pass
        hp.Hyprctl.focus_window(focus_list[0].address)

        # Serialize and write the list of objects to a file
        with open(f"/tmp/{args.window_class}.pkl", "wb") as file:
            pickle.dump(focus_list, file)
    else:
        # Read the list of objects from the file
        with open(f"/tmp/{args.window_class}.pkl", "rb") as file:
            loaded_items = pickle.load(file)

            index = next(
                (
                    i
                    for i, item in enumerate(loaded_items)
                    if item.address == current_window.address
                ),
                0,
            )

        if index == len(loaded_items) - 1:
            hp.Hyprctl.focus_window(loaded_items[0].address)
            with open(f"/tmp/{args.window_class}.pkl", "w") as file:
                pass

            # Serialize and write the list of objects to a file
            with open(f"/tmp/{args.window_class}.pkl", "wb") as file:
                pickle.dump(focus_list, file)

        if loaded_items[index].address == current_window.address:

            hp.Hyprctl.focus_window(loaded_items[index + 1].address)


if __name__ == "__main__":
    main()

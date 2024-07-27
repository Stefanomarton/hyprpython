import pickle

from hyprpython import Clients, Monitors, Workspaces, Hyprctl

client = Clients.get()
client_ordered = client.byFocusID()
monitor = Monitors.get()
current_workspace_id = Workspaces.current()
current_window = client.focused()

emacs_windows = [
    windows for windows in client_ordered.list if windows.wm_class == "emacs"
]


focus_list = [w for w in emacs_windows if w.workspace.id > 0]

if current_window.wm_class != "emacs":
    with open("/tmp/emacs.pkl", "w") as file:
        pass
    Hyprctl.focus_window(focus_list[0].address)

    # Serialize and write the list of objects to a file
    with open("/tmp/emacs.pkl", "wb") as file:
        pickle.dump(focus_list, file)
else:
    # Read the list of objects from the file
    with open("/tmp/emacs.pkl", "rb") as file:
        loaded_items = pickle.load(file)

        index: int = next(
            (
                i
                for i, item in enumerate(loaded_items)
                if item.address == current_window.address
            ),
            0,
        )

    if index == len(loaded_items) - 1:
        Hyprctl.focus_window(loaded_items[0].address)
        with open("/tmp/emacs.pkl", "w") as file:
            pass

        # Serialize and write the list of objects to a file
        with open("/tmp/emacs.pkl", "wb") as file:
            pickle.dump(focus_list, file)

    if loaded_items[index].address == current_window.address:

        Hyprctl.focus_window(loaded_items[index + 1].address)

from dataclasses import dataclass
import subprocess
import json
import operator


@dataclass
class wWorkspace:
    id: int
    name: str


@dataclass
class Client:
    address: int
    mapped: bool
    hidden: bool
    at: tuple
    size: tuple
    workspace: wWorkspace
    floating: bool
    pseudo: bool
    monitor: int
    wm_class: str
    title: str
    initialClass: str
    initialTitle: str
    pid: int
    xwayland: bool
    pinned: bool
    fullscreen: bool
    fullscreenMode: int
    fakeFullscreen: bool
    grouped: list
    tags: list
    swallowing: str
    focusHistoryID: int

    @classmethod
    def from_dict(cls, data: dict):
        return Client(
            address=data["address"],
            mapped=data["mapped"],
            hidden=data["hidden"],
            at=data["at"],
            size=data["size"],
            workspace=wWorkspace(**data["workspace"]),
            floating=data["floating"],
            pseudo=data["pseudo"],
            monitor=data["monitor"],
            wm_class=data["class"],
            title=data["title"],
            initialClass=data["initialClass"],
            initialTitle=data["initialTitle"],
            pid=data["pid"],
            xwayland=data["xwayland"],
            pinned=data["pinned"],
            fullscreen=data["fullscreen"],
            fullscreenMode=data["fullscreenMode"],
            fakeFullscreen=data["fakeFullscreen"],
            grouped=data["grouped"],
            tags=data["tags"],
            swallowing=data["swallowing"],
            focusHistoryID=data["focusHistoryID"],
        )


@dataclass
class Clients:
    @classmethod
    def get(cls):
        command = "hyprctl -j clients"
        output = subprocess.check_output(command.split())
        data = json.loads(output)
        clients = [Client.from_dict(client) for client in data]
        return clients

    @classmethod
    def byFocusID(cls):
        clients = cls.get()
        sorted_clients = sorted(clients, key=operator.attrgetter("focusHistoryID"))
        return sorted_clients

    @classmethod
    def focused(cls):
        clients = cls.get()  # Get the list of clients
        for client in clients:
            if client.focusHistoryID == 0:
                return client  # Return the focused Client object directly
        return None  # Return None if no focused client is found


@dataclass
class ActiveWorkspace:
    id: int
    name: str


@dataclass
class SpecialWorkspace:
    id: int
    name: str


@dataclass
class Monitor:
    id: int
    name: str
    description: str
    make: str
    model: str
    serial: str
    width: int
    height: int
    refreshRate: float
    x: int
    y: int
    activeWorkspace: ActiveWorkspace
    specialWorkspace: SpecialWorkspace
    reserved: list
    scale: float
    transform: int
    focused: bool
    dpmsStatus: bool
    vrr: bool
    activelyTearing: bool
    disabled: bool
    currentFormat: str
    availableModes: list

    @classmethod
    def from_dict(cls, data: dict):
        return Monitor(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            make=data["make"],
            model=data["model"],
            serial=data["serial"],
            width=data["width"],
            height=data["height"],
            refreshRate=data["refreshRate"],
            x=data["x"],
            y=data["y"],
            activeWorkspace=ActiveWorkspace(**data["activeWorkspace"]),
            specialWorkspace=SpecialWorkspace(**data["specialWorkspace"]),
            reserved=data["reserved"],
            scale=data["scale"],
            transform=data["transform"],
            focused=data["focused"],
            dpmsStatus=data["dpmsStatus"],
            vrr=data["vrr"],
            activelyTearing=data["activelyTearing"],
            disabled=data["disabled"],
            currentFormat=data["currentFormat"],
            availableModes=data["availableModes"],
        )


@dataclass
class Monitors:
    @classmethod
    def get(cls):
        command = "hyprctl -j monitors"
        output = subprocess.check_output(command.split())
        data = json.loads(output)
        monitors = [Monitor.from_dict(monitor) for monitor in data]
        return monitors

    @classmethod
    def focused(cls):
        monitors = cls.get()
        for monitor in monitors:
            if monitor.focused is True:
                return monitor


@dataclass
class Workspace:
    id: int
    name: str
    monitor: str
    monitorID: str
    windows: int
    hasfullscreen: bool
    lastwindow_address: str
    lastwindow_title: str

    @classmethod
    def from_dict(cls, data: dict):
        return Workspace(
            id=data["id"],
            name=data["name"],
            monitor=data["monitor"],
            monitorID=data["monitorID"],
            windows=data["windows"],
            hasfullscreen=data["hasfullscreen"],
            lastwindow_address=data["lastwindow"],
            lastwindow_title=data["lastwindowtitle"],
        )


@dataclass
class Workspaces:
    @classmethod
    def get(cls):
        command = "hyprctl -j workspaces"
        output = subprocess.check_output(command.split())
        data = json.loads(output)
        workspaces = [Workspace.from_dict(workspaces) for workspaces in data]
        return workspaces

    @classmethod
    def current(cls):
        command = "hyprctl -j activeworkspace"
        output = subprocess.check_output(command.split())
        data = json.loads(output)
        workspace = Workspace.from_dict(data)
        return workspace


class Hyprctl:
    @staticmethod
    def hyprctl_command(command):
        command = f"hyprctl --batch {command}"
        subprocess.run(command.split())

    @staticmethod
    def focus_window(address):
        Hyprctl.hyprctl_command(f"dispatch focuswindow address:{address}")

    @staticmethod
    def move_to_workspace_silent(address, wsId):
        Hyprctl.hyprctl_command(
            f"dispatch movetoworkspacesilent {wsId},address:{address}"
        )

import tkinter as tk
import serial
import serial.tools.list_ports
import threading
import time

def find_pico_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "Pico" in p.description or "CircuitPython" in p.description or "USB Serial" in p.description:
            return p.device
    if ports:
        return ports[0].device
    return None

class DoomTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("UAC TERMINAL // DOOM TELEMETRY")
        self.bg_color = "#030303" 
        self.root.configure(bg=self.bg_color)
        self.root.geometry("450x450")
        self.root.resizable(False, False)

        self.shots = 0
        self.time_s = 0
        self.deaths = 0
        self.connected = False

        # Frame sa crvenim ivicama
        self.main_frame = tk.Frame(root, bg=self.bg_color, highlightbackground="#900000", highlightcolor="#900000", highlightthickness=3)
        self.main_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)

        # Naslov
        tk.Label(self.main_frame, text="UAC COMBAT LINK", font=("Consolas", 18, "bold", "underline"), 
                 fg="#ff003c", bg=self.bg_color).pack(pady=(20, 10))

        # Ammo Expended
        tk.Label(self.main_frame, text="AMMO EXPENDED [ROUNDS]:", font=("Consolas", 10), fg="#777777", bg=self.bg_color).pack(pady=(15, 0))
        self.lbl_shots = tk.Label(self.main_frame, text="0", font=("Consolas", 45, "bold"), fg="#ff003c", bg=self.bg_color)
        self.lbl_shots.pack()

        # Combat Duration
        tk.Label(self.main_frame, text="COMBAT DURATION [T-MINUS]:", font=("Consolas", 10), fg="#777777", bg=self.bg_color).pack(pady=(15, 0))
        self.lbl_time = tk.Label(self.main_frame, text="00:00", font=("Consolas", 35, "bold"), fg="#ffffff", bg=self.bg_color)
        self.lbl_time.pack()

        # Casualties
        tk.Label(self.main_frame, text="CASUALTIES [RESPAWNS]:", font=("Consolas", 10), fg="#777777", bg=self.bg_color).pack(pady=(15, 0))
        self.lbl_deaths = tk.Label(self.main_frame, text="0", font=("Consolas", 35, "bold"), fg="#ff8c00", bg=self.bg_color)
        self.lbl_deaths.pack()

        # Status Bar
        self.status_frame = tk.Frame(root, bg="#111111")
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.lbl_status = tk.Label(self.status_frame, text="[SYS] SEARCHING FOR HARDWARE...", 
                                   font=("Consolas", 9), fg="#ff0000", bg="#111111", anchor="w")
        self.lbl_status.pack(padx=10, pady=5, fill=tk.X)

        self.thread = threading.Thread(target=self.read_serial, daemon=True)
        self.thread.start()
        self.update_gui()

    def read_serial(self):
        while True:
            try:
                port = find_pico_port()
                if port is None:
                    self.connected = False
                    time.sleep(2)
                    continue

                with serial.Serial(port, 115200, timeout=1) as ser:
                    self.connected = True
                    while True:
                        line = ser.readline().decode("utf-8").strip()
                        if "," in line:
                            parts = line.split(",")
                            if len(parts) == 3:
                                self.shots = int(parts[0])
                                self.time_s = int(parts[1])
                                self.deaths = int(parts[2])
            except Exception:
                self.connected = False
                time.sleep(2)

    def update_gui(self):
        m = self.time_s // 60
        s = self.time_s % 60
        
        separator = ":" if time.time() % 1 > 0.5 else " "

        self.lbl_shots.config(text=str(self.shots))
        self.lbl_time.config(text="{:02d}{}{:02d}".format(m, separator, s))
        self.lbl_deaths.config(text=str(self.deaths))

        if self.connected:
            self.lbl_status.config(text="[SYS] UAC HARDWARE SYNCED - UPLINK ACTIVE", fg="#00ff00")
            self.main_frame.config(highlightbackground="#550000")
        else:
            self.lbl_status.config(text="[SYS] SIGNAL LOST - RECONNECT PICO...", fg="#ff003c")
            self.main_frame.config(highlightbackground="#ff0000")

        self.root.after(100, self.update_gui)

if __name__ == "__main__":
    root = tk.Tk()
    app = DoomTerminal(root)
    root.mainloop()
import sys
import logging
import pyperclip
import darkdetect
import pywinstyles
from re import findall

import sv_ttk
import tkinter as tk
from tkinter import ttk

# === Constants ===
COORDS_PATTERN = r'(-?\d+)[^\d-]+(-?\d+)[^\d-]+(-?\d+)'
LOG_FILE = "CMD Block Relative Calculator.log"

# === Logging Setup ===
logging.basicConfig(
    filename=LOG_FILE,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)

logging.info("App Launched")


# === UI Components ===
class LabeledEntry(ttk.Frame):
    def __init__(self, parent, label, **kwargs):
        super().__init__(parent)
        self.label = ttk.Label(self, text=label)
        self.label.pack(anchor="w", padx=2, pady=5)
        self.entry = ttk.Entry(self, **kwargs)
        self.entry.pack(fill="x")

    def get(self):
        return self.entry.get()

    def set(self, text):
        self.entry.configure(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        self.entry.configure(state="readonly")

    def grid(self, **kwargs):
        super().grid(**kwargs)


class ResultField(ttk.Frame):
    def __init__(self, parent, default_text="<...>"):
        super().__init__(parent)
        self.entry = ttk.Entry(self)
        self.entry.insert(0, default_text)
        self.entry.configure(state="readonly")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.copy_btn = ttk.Button(
            self, text="C", command=self.copy_to_clipboard, width=2, cursor="hand2")
        self.copy_btn.pack(side="right")

    def copy_to_clipboard(self):
        pyperclip.copy(" ".join(self.entry.get().split(" ")[1:]))

    def set(self, text):
        self.entry.configure(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.insert(0, text)
        self.entry.configure(state="readonly")

    def clear(self):
        self.set("")

    def grid(self, **kwargs):
        super().grid(**kwargs)


# === Main App ===
class RelativeCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CMD Block Relative Calculator")
        # self.root.geometry("273x478")
        self.root.minsize(273, 0)
        # self.root.maxsize(0, 478)
        self.root.attributes('-topmost', True)
        self.root.grid_columnconfigure(0, weight=1)

        self.build_ui()

        sv_ttk.set_theme(darkdetect.theme())
        if sys.platform.startswith("win32"):
            self.apply_theme()

    def apply_theme(self):
        version = sys.getwindowsversion()
        is_dark = sv_ttk.get_theme() == "dark"
        if version.major == 10 and version.build >= 22000:
            pywinstyles.change_header_color(
                self.root, "#1c1c1c" if is_dark else "#fafafa")
        elif version.major == 10:
            pywinstyles.apply_style(self.root, "dark" if is_dark else "normal")
            self.root.wm_attributes("-alpha", 0.99)
            self.root.wm_attributes("-alpha", 1)

    def build_ui(self):
        self.cmd_block = LabeledEntry(self.root, "CMD Block:")
        self.cmd_block.grid(row=0, column=0, padx=10, pady=5, sticky="we")

        self.src1 = LabeledEntry(self.root, "Source #1 (optional):")
        self.src1.grid(row=2, column=0, padx=10, pady=5, sticky="we")

        self.src2 = LabeledEntry(self.root, "Source #2 (optional):")
        self.src2.grid(row=4, column=0, padx=10, pady=5, sticky="we")

        self.dst = LabeledEntry(self.root, "Destination:")
        self.dst.grid(row=6, column=0, padx=10, pady=5, sticky="we")

        self.calc_btn = ttk.Button(
            self.root, text="Calculate", command=self.calculate, cursor="hand2")
        self.calc_btn.grid(row=8, column=0, pady=15)

        self.result_1 = ResultField(self.root, "/setblock <dst>")
        self.result_1.grid(row=9, column=0, padx=10, pady=5, sticky="we")

        self.result_2 = ResultField(self.root, "/fill <src_1> <dst>")
        self.result_2.grid(row=10, column=0, padx=10, pady=5, sticky="we")

        self.result_3 = ResultField(self.root, "/clone <src_1> <src_2> <dst>")
        self.result_3.grid(row=11, column=0, padx=10, pady=5, sticky="we")

        ttk.Label(self.root, text="Made with ♥ by zaktabyte").grid(
            row=12, column=0, sticky="ns", padx=10, pady=(10, 16)
        )

    def calculate(self):
        def parse_coords(field):
            value = field.get()
            coords = findall(COORDS_PATTERN, value)
            if coords:
                logging.info(f"{field_label[field]}: {value}")
            return coords

        def relative_coords(src, ref):
            return [
                f"~{int(s) - r}".replace("~0", "~")
                for s, r in zip(src, ref)
            ]

        field_label = {
            self.cmd_block: "CMD Block",
            self.src1: "Source #1",
            self.src2: "Source #2",
            self.dst: "Destination"
        }

        cmd = parse_coords(self.cmd_block)
        src1 = parse_coords(self.src1)
        src2 = parse_coords(self.src2)
        dst = parse_coords(self.dst)

        self.result_1.clear()
        self.result_2.clear()
        self.result_3.clear()

        if cmd and dst:
            r1 = relative_coords(dst[0], map(int, cmd[0]))
            result1_str = "/setblock " + " ".join(r1)
            self.result_1.set(result1_str)
            logging.info(f"RESULT #1: {result1_str}")

        if cmd and src1 and dst:
            ref = list(map(int, cmd[0]))
            points = [src1[0], dst[0]]
            result2_str = "/fill " + " ".join(
                " ".join(relative_coords(p, ref)) for p in points
            )
            self.result_2.set(result2_str)
            logging.info(f"RESULT #2: {result2_str}")

        if cmd and src1 and src2 and dst:
            ref = list(map(int, cmd[0]))
            points = [src1[0], src2[0], dst[0]]
            result3_str = "/clone " + " ".join(
                " ".join(relative_coords(p, ref)) for p in points
            )
            self.result_3.set(result3_str)
            logging.info(f"RESULT #3: {result3_str}")


# === Entry Point ===
if __name__ == "__main__":
    root = tk.Tk()
    app = RelativeCalculatorApp(root)
    root.mainloop()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GRAFFITI CALC — научный калькулятор в стиле граффити
"""

import tkinter as tk
from tkinter import font as tkfont
import math
import re


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("GRAFFITI CALC")
        self.root.configure(bg="#3a2020")
        self.root.resizable(False, False)

        self.expr = ""
        self.last_result = None
        self.just_evaluated = False

        self._build_background()
        self._build_ui()
        self._bind_keys()

    # ============================================================
    #  ФОН: кирпичная стена + неоновые брызги
    # ============================================================
    def _build_background(self):
        self.bg_canvas = tk.Canvas(self.root, width=460, height=720,
                                   highlightthickness=0, bg="#3a2020")
        self.bg_canvas.place(x=0, y=0)

        # Кирпичи
        brick_w, brick_h = 58, 40
        mortar = "#1a0f0f"
        colors = ["#4a2525", "#3d1f1f", "#522a2a", "#452222", "#4f2828"]

        for row in range(20):
            offset = 29 if row % 2 == 1 else 0
            for col in range(-1, 10):
                x = col * brick_w + offset
                y = row * brick_h
                color = colors[(row + col) % len(colors)]
                self.bg_canvas.create_rectangle(
                    x, y, x + brick_w - 2, y + brick_h - 2,
                    fill=color, outline=mortar, width=2
                )

        # Неоновые брызги (исправлено: передаём int шагов)
        self._draw_splash(60, 80, 180, "#ff00ff", steps=15)
        self._draw_splash(400, 650, 220, "#00ffff", steps=15)
        self._draw_splash(230, 400, 140, "#fff200", steps=12)

    def _draw_splash(self, cx, cy, r, color, steps=15):
        """
        Рисуем размытый неоновый круг через концентрические овалы.
        cx, cy — центр; r — радиус; color — hex-цвет; steps — целое число слоёв.
        """
        # Парсим hex-цвет в RGB
        color = color.lstrip("#")
        r_c, g_c, b_c = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)

        for i in range(steps, 0, -1):
            ratio = i / steps
            radius = r * ratio
            # Чем ближе к центру — тем ярче цвет
            brightness = 1.0 - (ratio * 0.7)
            rc = int(r_c * brightness)
            gc = int(g_c * brightness)
            bc = int(b_c * brightness)
            hex_color = f"#{rc:02x}{gc:02x}{bc:02x}"

            self.bg_canvas.create_oval(
                cx - radius, cy - radius, cx + radius, cy + radius,
                fill=hex_color, outline=""
            )

    # ============================================================
    #  ОСНОВНОЙ ИНТЕРФЕЙС
    # ============================================================
    def _build_ui(self):
        self.frame = tk.Frame(self.root, bg="#14100f",
                              highlightbackground="#000",
                              highlightthickness=6)
        self.frame.place(x=20, y=20, width=420, height=680)

        title_font = tkfont.Font(family="Impact", size=30, weight="bold")
        self.title = tk.Label(self.frame, text="★ GRAFFITI CALC ★",
                              font=title_font, fg="#fff200", bg="#14100f",
                              highlightthickness=0)
        self.title.place(x=0, y=10, width=420, height=50)

        self.display_frame = tk.Frame(self.frame, bg="#0a0a0a",
                                      highlightbackground="#000",
                                      highlightthickness=4)
        self.display_frame.place(x=20, y=75, width=380, height=120)

        expr_font = tkfont.Font(family="Consolas", size=13)
        self.expr_label = tk.Label(self.display_frame, text=" ",
                                   font=expr_font, fg="#888888", bg="#0a0a0a",
                                   anchor="e")
        self.expr_label.place(x=10, y=10, width=360, height=30)

        res_font = tkfont.Font(family="Consolas", size=32, weight="bold")
        self.result_label = tk.Label(self.display_frame, text="0",
                                     font=res_font, fg="#00ff88", bg="#0a0a0a",
                                     anchor="e")
        self.result_label.place(x=10, y=50, width=360, height=60)

        self.display_frame.after(10, self._draw_display_drops)

        self._build_buttons()

    def _draw_display_drops(self):
        drop1 = tk.Label(self.display_frame, text="●", fg="#ff00ff",
                         bg="#0a0a0a", font=("Arial", 10))
        drop1.place(x=60, y=-8)
        drop2 = tk.Label(self.display_frame, text="●", fg="#00ffff",
                         bg="#0a0a0a", font=("Arial", 8))
        drop2.place(x=280, y=-6)

    # ============================================================
    #  КНОПКИ
    # ============================================================
    def _build_buttons(self):
        COLORS = {
            "num":   {"bg": "#fff200", "fg": "#000000"},
            "op":    {"bg": "#ff00ff", "fg": "#ffffff"},
            "sci":   {"bg": "#00ffff", "fg": "#000000"},
            "clear": {"bg": "#ff3355", "fg": "#ffffff"},
            "equal": {"bg": "#00ff88", "fg": "#000000"},
        }

        btn_font = tkfont.Font(family="Arial", size=13, weight="bold")
        btn_font_small = tkfont.Font(family="Arial", size=11, weight="bold")
        btn_font_big = tkfont.Font(family="Arial", size=20, weight="bold")

        layout = [
            ("sin", "sci", "fn", "sin(", 1),
            ("cos", "sci", "fn", "cos(", 1),
            ("tan", "sci", "fn", "tan(", 1),
            ("log", "sci", "fn", "log(", 1),
            ("ln",  "sci", "fn", "ln(",  1),
            ("√",   "sci", "fn",   "sqrt(", 1),
            ("x²",  "sci", "sq",   None,    1),
            ("xʸ",  "sci", "insert", "^",   1),
            ("x!",  "sci", "insert", "!",   1),
            ("π",   "sci", "insert", "π",   1),
            ("e",   "sci", "insert", "e",   1),
            ("(",   "sci", "insert", "(",   1),
            (")",   "sci", "insert", ")",   1),
            ("%",   "sci", "insert", "%",   1),
            ("C",   "clear", "clear", None, 1),
            ("7",   "num", "insert", "7",   1),
            ("8",   "num", "insert", "8",   1),
            ("9",   "num", "insert", "9",   1),
            ("÷",   "op",  "insert", "÷",   1),
            ("CE",  "clear", "ce",   None,  1),
            ("4",   "num", "insert", "4",   1),
            ("5",   "num", "insert", "5",   1),
            ("6",   "num", "insert", "6",   1),
            ("×",   "op",  "insert", "×",   1),
            ("⌫",   "clear", "back", None,  1),
            ("1",   "num", "insert", "1",   1),
            ("2",   "num", "insert", "2",   1),
            ("3",   "num", "insert", "3",   1),
            ("−",   "op",  "insert", "-",   1),
            ("+",   "op",  "insert", "+",   1),
            ("0",   "num", "insert", "0",   2),
            (".",   "num", "insert", ".",   1),
            ("=",   "equal", "equals", None, 2),
        ]

        btn_frame = tk.Frame(self.frame, bg="#14100f")
        btn_frame.place(x=20, y=210, width=380, height=460)

        cols = 5
        btn_w = 72
        btn_h = 52
        gap = 5

        for idx, (text, kind, act, val, colspan) in enumerate(layout):
            row = idx // cols
            col = idx % cols

            colors = COLORS[kind]
            if kind == "equal":
                f = btn_font_big
            elif kind == "sci":
                f = btn_font_small
            else:
                f = btn_font

            btn = tk.Button(
                btn_frame, text=text, font=f,
                bg=colors["bg"], fg=colors["fg"],
                activebackground=colors["bg"],
                activeforeground=colors["fg"],
                relief="raised", bd=3,
                highlightbackground="#000", highlightthickness=2,
                cursor="hand2"
            )
            btn.configure(command=lambda a=act, v=val: self._handle(a, v))

            x = col * (btn_w + gap)
            y = row * (btn_h + gap)
            w = btn_w * colspan + gap * (colspan - 1)
            btn.place(x=x, y=y, width=w, height=btn_h)

    # ============================================================
    #  МАТЕМАТИКА
    # ============================================================
    @staticmethod
    def _factorial(n):
        if n < 0 or int(n) != n:
            raise ValueError("Factorial: integer >= 0 required")
        if n > 170:
            raise ValueError("Factorial: number too large")
        return math.factorial(int(n))

    def _process_factorials(self, s):
        safety = 0
        while "!" in s and safety < 100:
            safety += 1
            idx = s.find("!")
            if idx == -1:
                break
            before = s[idx - 1] if idx > 0 else ""

            if before == ")":
                depth = 1
                i = idx - 2
                while i >= 0 and depth > 0:
                    if s[i] == ")":
                        depth += 1
                    elif s[i] == "(":
                        depth -= 1
                    if depth > 0:
                        i -= 1
                if depth == 0:
                    inner = s[i:idx]
                    s = s[:i] + "factorial" + inner + s[idx + 1:]
                else:
                    raise ValueError("Unbalanced parentheses")
            elif before.isdigit() or before == ".":
                j = idx - 1
                while j >= 0 and (s[j].isdigit() or s[j] == "."):
                    j -= 1
                num = s[j + 1:idx]
                s = s[:j + 1] + "factorial(" + num + ")" + s[idx + 1:]
            else:
                raise ValueError("Invalid factorial")
        return s

    def _prepare(self, raw):
        s = raw
        s = s.replace("×", "*").replace("÷", "/").replace("−", "-")
        s = s.replace("π", "(math.pi)")
        s = re.sub(r"(?<![a-zA-Z])e(?![a-zA-Z(])", "(math.e)", s)

        s = s.replace("sin(", "math.sin(")
        s = s.replace("cos(", "math.cos(")
        s = s.replace("tan(", "math.tan(")
        s = s.replace("log(", "math.log10(")
        s = s.replace("ln(",  "math.log(")
        s = s.replace("sqrt(", "math.sqrt(")

        s = s.replace("^", "**")

        s = self._process_factorials(s)

        s = re.sub(r"(\d+(?:\.\d+)?)%", r"(\1/100)", s)

        s = re.sub(r"(\d)\(", r"\1*(", s)
        s = s.replace(")(", ")*(")
        s = re.sub(r"(\d)(math)", r"\1*math", s)
        s = re.sub(r"\)(math)", r")*math", s)
        s = re.sub(r"(math\.pi|math\.e)(\d|\()", r"\1*\2", s)

        return s

    def _evaluate(self, raw):
        if not raw or not raw.strip():
            raise ValueError("Empty expression")

        depth = 0
        for ch in raw:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            if depth < 0:
                raise ValueError("Unbalanced parentheses")

        processed = raw
        while depth > 0:
            processed += ")"
            depth -= 1

        prepared = self._prepare(processed)

        safe_ns = {"math": math, "factorial": self._factorial,
                   "__builtins__": {}}
        try:
            result = eval(prepared, safe_ns)
        except Exception:
            raise ValueError("Syntax error")

        if not isinstance(result, (int, float)):
            raise ValueError("Not a number")
        if math.isinf(result):
            raise ValueError("Infinity or division by zero")
        if math.isnan(result):
            raise ValueError("Math error")

        return result

    @staticmethod
    def _format_number(n):
        if n == 0:
            return "0"
        if abs(n) < 1e-10 or abs(n) >= 1e15:
            return f"{n:.8e}"
        return f"{n:.12g}"

    # ============================================================
    #  ЛОГИКА ИНТЕРФЕЙСА
    # ============================================================
    def _render(self):
        self.expr_label.configure(text=self.expr if self.expr else " ")
        self.result_label.configure(fg="#00ff88")

        if self.expr:
            try:
                value = self._evaluate(self.expr)
                self.result_label.configure(text=self._format_number(value))
            except Exception:
                self.result_label.configure(text="...")
        else:
            self.result_label.configure(text="0")

    def _show_error(self, msg):
        self.result_label.configure(text=f"Error: {msg}", fg="#ff3355")

    def _handle(self, act, val):
        try:
            if act == "insert":
                if self.just_evaluated:
                    is_op = val in ("+", "-", "×", "÷", "^")
                    if is_op and self.last_result is not None:
                        self.expr = self._format_number(self.last_result)
                    else:
                        self.expr = ""
                    self.just_evaluated = False
                self.expr += val
                self._render()

            elif act == "fn":
                if self.just_evaluated:
                    self.expr = ""
                    self.just_evaluated = False
                self.expr += val
                self._render()

            elif act == "sq":
                if self.just_evaluated and self.last_result is not None:
                    self.expr = f"({self._format_number(self.last_result)})^2"
                    self.just_evaluated = False
                else:
                    self.expr += "^2"
                self._render()

            elif act == "clear":
                self.expr = ""
                self.last_result = None
                self.just_evaluated = False
                self._render()

            elif act == "ce":
                self.expr = re.sub(r"(sin\(|cos\(|tan\(|log\(|ln\(|sqrt\()$", "", self.expr)
                self.expr = re.sub(r"[\d.]+$", "", self.expr)
                self._render()

            elif act == "back":
                if self.just_evaluated:
                    self.expr = ""
                    self.just_evaluated = False
                else:
                    m = re.search(r"(sin\(|cos\(|tan\(|log\(|ln\(|sqrt\()$", self.expr)
                    if m:
                        self.expr = self.expr[:-len(m.group(0))]
                    else:
                        self.expr = self.expr[:-1]
                self._render()

            elif act == "equals":
                if not self.expr:
                    return
                try:
                    value = self._evaluate(self.expr)
                    self.last_result = value
                    self.expr_label.configure(text=self.expr + " =")
                    self.result_label.configure(text=self._format_number(value), fg="#00ff88")
                    self.expr = self._format_number(value)
                    self.just_evaluated = True
                except Exception as e:
                    self._show_error(str(e))
                    self.just_evaluated = False

        except Exception:
            self._show_error("Internal error")

    # ============================================================
    #  КЛАВИАТУРА
    # ============================================================
    def _bind_keys(self):
        self.root.bind("<Key>", self._on_key)

    def _on_key(self, event):
        key = event.keysym

        if key in "0123456789":
            self._handle("insert", key)
        elif key == "period":
            self._handle("insert", ".")
        elif key == "plus":
            self._handle("insert", "+")
        elif key == "minus":
            self._handle("insert", "-")
        elif key == "asterisk":
            self._handle("insert", "×")
        elif key == "slash":
            self._handle("insert", "÷")
        elif key == "parenleft":
            self._handle("insert", "(")
        elif key == "parenright":
            self._handle("insert", ")")
        elif key == "asciicircum":
            self._handle("insert", "^")
        elif key == "percent":
            self._handle("insert", "%")
        elif key == "exclam":
            self._handle("insert", "!")
        elif key in ("Return", "KP_Enter", "equal"):
            self._handle("equals", None)
        elif key == "BackSpace":
            self._handle("back", None)
        elif key == "Escape":
            self._handle("clear", None)
        elif key == "Delete":
            self._handle("ce", None)


def main():
    root = tk.Tk()

    # Центрируем окно
    w, h = 460, 720
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    app = Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()

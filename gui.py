import math
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from calculations import (
    calculate_multiplication_factor,
    classify_criticality,
    load_nuclear_data,
)
from variables import (
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH,
)


ctk.set_appearance_mode("light")


class CriticalityCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(1100, 720)

        self.nuclear_data = load_nuclear_data()
        self.number_density_entries = {}

        self.background_colour = "#EEF7FF"
        self.header_background = "#E4F3FF"
        self.card_colour = "#FFFFFF"
        self.section_colour = "#EAF5FE"
        self.illustration_colour = "#F2F8FE"

        self.primary_blue = "#318FE4"
        self.dark_blue = "#102E63"
        self.muted_blue = "#687D9E"
        self.border_colour = "#D4E5F5"

        self.root.configure(bg=self.background_colour)

        self._create_interface()

    def _create_interface(self):
        self.main_container = ctk.CTkFrame(
            self.root,
            fg_color=self.background_colour,
            corner_radius=0,
        )
        self.main_container.pack(
            fill="both",
            expand=True,
        )

        self._create_header()
        self._create_content()

    def _create_header(self):
        header = ctk.CTkFrame(
            self.main_container,
            fg_color=self.header_background,
            corner_radius=0,
            height=82,
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="Reactor Criticality Calculator",
            font=("Arial", 25, "bold"),
            text_color=self.dark_blue,
        )
        title.pack(pady=(10, 0))

        subtitle = ctk.CTkLabel(
            header,
            text="One-speed thermal neutron model with zero neutron leakage",
            font=("Arial", 13),
            text_color=self.dark_blue,
        )
        subtitle.pack(pady=(0, 5))

    def _create_content(self):
        content = ctk.CTkFrame(
            self.main_container,
            fg_color=self.background_colour,
            corner_radius=0,
        )
        content.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=12,
        )

        content.grid_columnconfigure(0, weight=53)
        content.grid_columnconfigure(1, weight=47)
        content.grid_rowconfigure(0, weight=1)

        input_card = ctk.CTkFrame(
            content,
            fg_color=self.card_colour,
            corner_radius=17,
            border_width=1,
            border_color=self.border_colour,
        )
        input_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 7),
        )

        result_card = ctk.CTkFrame(
            content,
            fg_color=self.card_colour,
            corner_radius=17,
            border_width=1,
            border_color=self.border_colour,
        )
        result_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(7, 0),
        )

        self._create_input_panel(input_card)
        self._create_result_panel(result_card)

    def _create_input_panel(self, parent):
        heading_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            height=40,
        )
        heading_frame.pack(
            fill="x",
            padx=16,
            pady=(10, 5),
        )
        heading_frame.pack_propagate(False)

        icon = ctk.CTkLabel(
            heading_frame,
            text="△",
            width=25,
            font=("Arial", 18, "bold"),
            text_color=self.primary_blue,
        )
        icon.pack(
            side="left",
            padx=(0, 4),
        )

        heading = ctk.CTkLabel(
            heading_frame,
            text="Species Number Densities",
            font=("Arial", 16, "bold"),
            text_color=self.dark_blue,
        )
        heading.pack(side="left")

        header_frame = ctk.CTkFrame(
            parent,
            fg_color=self.section_colour,
            corner_radius=10,
            height=45,
        )
        header_frame.pack(
            fill="x",
            padx=14,
            pady=(0, 4),
        )
        header_frame.pack_propagate(False)

        headers = (
            "Species",
            "Number Density\n(m⁻³)",
            "σₐ\n(barns)",
            "σf\n(barns)",
            "ν",
        )

        column_widths = (150, 290, 115, 115, 60)

        for column, width in enumerate(column_widths):
            header_frame.grid_columnconfigure(
                column,
                weight=1,
                minsize=width,
            )

        for column, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Arial", 14, "bold"),
                text_color=self.dark_blue,
            )
            label.grid(
                row=0,
                column=column,
                padx=2,
                pady=3,
                sticky="nsew",
            )

        table_frame = ctk.CTkFrame(
            parent,
            fg_color=self.card_colour,
            corner_radius=0,
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=14,
            pady=(0, 8),
        )

        for column, width in enumerate(column_widths):
            table_frame.grid_columnconfigure(
                column,
                weight=1,
                minsize=width,
            )

        for row, (species, data) in enumerate(self.nuclear_data.items()):
            table_frame.grid_rowconfigure(
                row,
                weight=1,
            )

            species_label = ctk.CTkLabel(
                table_frame,
                text=species,
                font=("Arial", 13),
                text_color=self.dark_blue,
                anchor="w",
                height=22,
            )
            species_label.grid(
                row=row,
                column=0,
                padx=(3, 5),
                pady=1,
                sticky="ew",
            )

            entry = ctk.CTkEntry(
                table_frame,
                height=23,
                corner_radius=5,
                border_width=1,
                border_color="#BCD6EB",
                fg_color="#FFFFFF",
                text_color=self.dark_blue,
                font=("Arial", 13),
            )
            entry.insert(0, "0")
            entry.grid(
                row=row,
                column=1,
                padx=3,
                pady=1,
                sticky="ew",
            )

            self.number_density_entries[species] = entry

            absorption_label = ctk.CTkLabel(
                table_frame,
                text=f'{data["absorption_cross_section_barns"]:g}',
                font=("Arial", 13),
                text_color=self.dark_blue,
                anchor="center",
                height=22,
            )
            absorption_label.grid(
                row=row,
                column=2,
                padx=2,
                pady=1,
            )

            fission_label = ctk.CTkLabel(
                table_frame,
                text=f'{data["fission_cross_section_barns"]:g}',
                font=("Arial", 13),
                text_color=self.dark_blue,
                anchor="center",
                height=22,
            )
            fission_label.grid(
                row=row,
                column=3,
                padx=2,
                pady=1,
            )

            neutrons_label = ctk.CTkLabel(
                table_frame,
                text=f'{data["neutrons_per_fission"]:g}',
                font=("Arial", 13),
                text_color=self.dark_blue,
                anchor="center",
                height=22,
            )
            neutrons_label.grid(
                row=row,
                column=4,
                padx=2,
                pady=1,
            )

    def _create_result_panel(self, parent):
        heading_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            height=40,
        )
        heading_frame.pack(
            fill="x",
            padx=18,
            pady=(10, 5),
        )
        heading_frame.pack_propagate(False)

        bars_frame = ctk.CTkFrame(
            heading_frame,
            fg_color="transparent",
        )
        bars_frame.pack(
            side="left",
            padx=(0, 7),
        )

        for height in (12, 18, 14):
            bar = ctk.CTkFrame(
                bars_frame,
                width=5,
                height=height,
                fg_color=self.primary_blue,
                corner_radius=1,
            )
            bar.pack(
                side="left",
                anchor="s",
                padx=1,
            )

        heading = ctk.CTkLabel(
            heading_frame,
            text="Criticality Result",
            font=("Arial", 16, "bold"),
            text_color=self.dark_blue,
        )
        heading.pack(side="left")

        illustration_frame = ctk.CTkFrame(
            parent,
            fg_color=self.illustration_colour,
            corner_radius=14,
            height=240,
        )
        illustration_frame.pack(
            fill="x",
            padx=16,
            pady=(0, 5),
        )
        illustration_frame.pack_propagate(False)

        self.reactor_canvas = tk.Canvas(
            illustration_frame,
            width=400,
            height=230,
            bg=self.illustration_colour,
            highlightthickness=0,
        )
        self.reactor_canvas.pack(expand=True)

        self._draw_reactor("neutral")

        self.k_label = ctk.CTkLabel(
            parent,
            text="k = --",
            font=("Arial", 30, "bold"),
            text_color=self.dark_blue,
            height=38,
        )
        self.k_label.pack()

        self.status_label = ctk.CTkLabel(
            parent,
            text="Awaiting calculation",
            font=("Arial", 15, "bold"),
            text_color=self.muted_blue,
            height=27,
        )
        self.status_label.pack(pady=(0, 5))

        values_frame = ctk.CTkFrame(
            parent,
            fg_color=self.section_colour,
            corner_radius=9,
            height=48,
        )
        values_frame.pack(
            fill="x",
            padx=16,
            pady=(0, 6),
        )
        values_frame.pack_propagate(False)

        values_frame.grid_columnconfigure(0, weight=1)
        values_frame.grid_columnconfigure(1, weight=1)
        values_frame.grid_rowconfigure(0, weight=1)

        self.absorption_label = ctk.CTkLabel(
            values_frame,
            text="Σₐ = -- m⁻¹",
            font=("Arial", 13, "bold"),
            text_color=self.dark_blue,
        )
        self.absorption_label.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.production_label = ctk.CTkLabel(
            values_frame,
            text="νΣf = -- m⁻¹",
            font=("Arial", 13, "bold"),
            text_color=self.dark_blue,
        )
        self.production_label.grid(
            row=0,
            column=1,
            sticky="nsew",
        )

        definition_frame = ctk.CTkFrame(
            parent,
            fg_color="#EFF7FD",
            corner_radius=9,
            height=38,
        )
        definition_frame.pack(
            fill="x",
            padx=16,
            pady=(0, 6),
        )
        definition_frame.pack_propagate(False)

        definition = ctk.CTkLabel(
            definition_frame,
            text=(
                "Subcritical: k < 1    |    "
                "Critical: k ≈ 1    |    "
                "Supercritical: k > 1"
            ),
            font=("Arial", 12),
            text_color=self.dark_blue,
        )
        definition.pack(expand=True)

        calculate_button = ctk.CTkButton(
            parent,
            text="Calculate Criticality",
            command=self._calculate,
            height=38,
            corner_radius=9,
            fg_color=self.primary_blue,
            hover_color="#247BC5",
            text_color="#FFFFFF",
            font=("Arial", 13, "bold"),
        )
        calculate_button.pack(
            fill="x",
            padx=16,
            pady=(0, 6),
        )

        reset_button = ctk.CTkButton(
            parent,
            text="↻  Reset",
            command=self._reset,
            height=36,
            corner_radius=9,
            fg_color="#F6FAFE",
            hover_color="#E7F2FC",
            border_width=1,
            border_color=self.primary_blue,
            text_color=self.dark_blue,
            font=("Arial", 13, "bold"),
        )
        reset_button.pack(
            fill="x",
            padx=16,
            pady=(0, 10),
        )

    def _draw_reactor(self, state):
        self.reactor_canvas.delete("all")

        colours = {
            "neutral": {
                "outline": "#173D66",
                "tower": "#F5EEDD",
                "accent": "#4B99E0",
                "cheek": "#FFB7AD",
            },
            "subcritical": {
                "outline": "#397A52",
                "tower": "#F2EDDD",
                "accent": "#64A866",
                "cheek": "#FFB7AD",
            },
            "critical": {
                "outline": "#C98124",
                "tower": "#F5E9D5",
                "accent": "#E0A23E",
                "cheek": "#FFB7AD",
            },
            "supercritical": {
                "outline": "#C94040",
                "tower": "#F4E6DA",
                "accent": "#D95A4B",
                "cheek": "#FFB7AD",
            },
        }

        palette = colours[state]

        outline = palette["outline"]
        tower_fill = palette["tower"]
        accent = palette["accent"]
        cheek = palette["cheek"]

        self.reactor_canvas.create_oval(
            95,
            20,
            305,
            220,
            fill="#DCEEFF",
            outline="",
        )

        clouds = (
            (135, 5, 185, 48),
            (165, -5, 225, 48),
            (205, 8, 260, 52),
            (120, 28, 180, 72),
            (155, 25, 225, 78),
            (205, 30, 275, 80),
        )

        for x1, y1, x2, y2 in clouds:
            self.reactor_canvas.create_oval(
                x1,
                y1,
                x2,
                y2,
                fill="#FFFFFF",
                outline="#669DD2",
                width=3,
            )

        self.reactor_canvas.create_polygon(
            158,
            88,
            242,
            88,
            235,
            143,
            263,
            205,
            137,
            205,
            165,
            143,
            fill=tower_fill,
            outline=outline,
            width=4,
            smooth=True,
        )

        self.reactor_canvas.create_arc(
            156,
            78,
            244,
            102,
            start=0,
            extent=180,
            style="arc",
            outline=outline,
            width=4,
        )

        self.reactor_canvas.create_line(
            159,
            89,
            241,
            89,
            fill=outline,
            width=4,
        )

        for x_position in (175, 188, 200, 212, 225):
            self.reactor_canvas.create_line(
                x_position,
                99,
                x_position - 4,
                194,
                fill="#DDD5C3",
                width=1,
            )

        self.reactor_canvas.create_line(
            110,
            135,
            124,
            147,
            fill=accent,
            width=4,
            capstyle=tk.ROUND,
        )

        self.reactor_canvas.create_line(
            290,
            135,
            276,
            147,
            fill=accent,
            width=4,
            capstyle=tk.ROUND,
        )

        if state == "supercritical":
            self._draw_angry_face(
                outline,
                cheek,
            )
        elif state == "critical":
            self._draw_neutral_face(
                outline,
                cheek,
            )
        else:
            self._draw_happy_face(
                outline,
                cheek,
            )

        bush_fill = "#78B153"
        bush_outline = "#3E7A3E"

        bushes = (
            (123, 181, 157, 213),
            (145, 175, 179, 210),
            (221, 175, 255, 210),
            (243, 181, 277, 213),
        )

        for x1, y1, x2, y2 in bushes:
            self.reactor_canvas.create_oval(
                x1,
                y1,
                x2,
                y2,
                fill=bush_fill,
                outline=bush_outline,
                width=2,
            )

        self.reactor_canvas.create_line(
            118,
            208,
            282,
            208,
            fill=bush_outline,
            width=3,
        )

    def _draw_happy_face(self, colour, cheek):
        self.reactor_canvas.create_arc(
            169,
            131,
            186,
            148,
            start=0,
            extent=180,
            style="arc",
            outline=colour,
            width=3,
        )

        self.reactor_canvas.create_arc(
            214,
            131,
            231,
            148,
            start=0,
            extent=180,
            style="arc",
            outline=colour,
            width=3,
        )

        self.reactor_canvas.create_oval(
            154,
            148,
            172,
            161,
            fill=cheek,
            outline="",
        )

        self.reactor_canvas.create_oval(
            228,
            148,
            246,
            161,
            fill=cheek,
            outline="",
        )

        self.reactor_canvas.create_arc(
            183,
            143,
            217,
            176,
            start=200,
            extent=140,
            style="arc",
            outline=colour,
            width=3,
        )

    def _draw_neutral_face(self, colour, cheek):
        self.reactor_canvas.create_oval(
            174,
            138,
            182,
            146,
            fill=colour,
            outline=colour,
        )

        self.reactor_canvas.create_oval(
            218,
            138,
            226,
            146,
            fill=colour,
            outline=colour,
        )

        self.reactor_canvas.create_oval(
            155,
            150,
            172,
            162,
            fill=cheek,
            outline="",
        )

        self.reactor_canvas.create_oval(
            228,
            150,
            245,
            162,
            fill=cheek,
            outline="",
        )

        self.reactor_canvas.create_line(
            187,
            166,
            213,
            166,
            fill=colour,
            width=3,
            capstyle=tk.ROUND,
        )

    def _draw_angry_face(self, colour, cheek):
        self.reactor_canvas.create_line(
            166,
            133,
            185,
            142,
            fill=colour,
            width=3,
        )

        self.reactor_canvas.create_line(
            215,
            142,
            234,
            133,
            fill=colour,
            width=3,
        )

        self.reactor_canvas.create_oval(
            175,
            145,
            183,
            153,
            fill=colour,
            outline=colour,
        )

        self.reactor_canvas.create_oval(
            217,
            145,
            225,
            153,
            fill=colour,
            outline=colour,
        )

        self.reactor_canvas.create_oval(
            155,
            156,
            172,
            168,
            fill=cheek,
            outline="",
        )

        self.reactor_canvas.create_oval(
            228,
            156,
            245,
            168,
            fill=cheek,
            outline="",
        )

        self.reactor_canvas.create_arc(
            184,
            166,
            216,
            193,
            start=20,
            extent=140,
            style="arc",
            outline=colour,
            width=3,
        )

    def _format_output(self, value):
        return f"{value:.4g}"

    def _calculate(self):
        try:
            number_densities = {}

            for species, entry in self.number_density_entries.items():
                value_text = entry.get().strip()

                if not value_text:
                    value = 0.0
                else:
                    value = float(value_text)

                if not math.isfinite(value):
                    raise ValueError(
                        f"Number density for {species} must be a finite value."
                    )

                if value < 0:
                    raise ValueError(
                        f"Number density for {species} must not be negative."
                    )

                if value > 0:
                    number_densities[species] = value

            if not number_densities:
                raise ValueError(
                    "Enter at least one non-zero number density."
                )

            result = calculate_multiplication_factor(number_densities)

            multiplication_factor = result["multiplication_factor"]

            if not math.isfinite(multiplication_factor):
                raise ValueError(
                    "The calculated multiplication factor is not finite."
                )

            classification = classify_criticality(
                multiplication_factor
            )

            self.k_label.configure(
                text=f"k = {self._format_output(multiplication_factor)}"
            )

            self.absorption_label.configure(
                text=(
                    "Σₐ = "
                    f'{self._format_output(result["total_absorption"])} m⁻¹'
                )
            )

            self.production_label.configure(
                text=(
                    "νΣf = "
                    f'{self._format_output(result["total_neutron_production"])} m⁻¹'
                )
            )

            if classification == "Subcritical":
                self.status_label.configure(
                    text="SUBCRITICAL",
                    text_color="#397A52",
                )
                self._draw_reactor("subcritical")

            elif classification == "Critical":
                self.status_label.configure(
                    text="CRITICAL",
                    text_color="#C98124",
                )
                self._draw_reactor("critical")

            else:
                self.status_label.configure(
                    text="SUPERCRITICAL",
                    text_color="#C94040",
                )
                self._draw_reactor("supercritical")

        except ValueError as error:
            messagebox.showerror(
                "Invalid Input",
                str(error),
            )

    def _reset(self):
        for entry in self.number_density_entries.values():
            entry.delete(0, tk.END)
            entry.insert(0, "0")

        self.k_label.configure(text="k = --")

        self.status_label.configure(
            text="Awaiting calculation",
            text_color=self.muted_blue,
        )

        self.absorption_label.configure(
            text="Σₐ = -- m⁻¹"
        )

        self.production_label.configure(
            text="νΣf = -- m⁻¹"
        )

        self._draw_reactor("neutral")


def run_gui():
    root = ctk.CTk()
    CriticalityCalculatorGUI(root)
    root.mainloop()
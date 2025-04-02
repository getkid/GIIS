import os
import subprocess
import tkinter as tk
from tkinter import messagebox

from scripts.line_algorithms import DDA, Bresenham, Wu

class DrawingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Drawing App")
        self.geometry("800x600")
        self._create_menu()
        self._create_canvas()

        self._grid_size = 5
        self._draw_grid()

        self._start_x = None
        self._start_y = None

        self._current_line_algorithm = None
        self._current_curve_algorithm = None
        self._current_parametric_algorithm = None

        self._debug_mode = False

    def _create_menu(self):
        menubar = tk.Menu(self)

        line_menu = tk.Menu(menubar, tearoff=0)
        line_menu.add_command(label="DDA", command=lambda: self._set_line_algorithm("DDA"))
        line_menu.add_command(label="Bresenham", command=lambda: self._set_line_algorithm("Bresenham"))
        line_menu.add_command(label="Wu", command=lambda: self._set_line_algorithm("Wu"))
        menubar.add_cascade(label="Line", menu=line_menu)

        menubar.add_checkbutton(label="Debug", command=self._toggle_debug_mode)

        self.config(menu=menubar)

    def _create_canvas(self):
        self._canvas = tk.Canvas(self, bg="white")
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._canvas.bind("<Button-1>", self._on_canvas_click)
        self._canvas.bind("<Configure>", lambda event: self._draw_grid())

    def _clear_canvas(self):
        self._canvas.delete("all")
        self._draw_grid()

    def _toggle_debug_mode(self):
        self._debug_mode = not self._debug_mode

    def _on_canvas_click(self, event):
        if any((
                self._current_line_algorithm,
                self._current_curve_algorithm,
                self._current_parametric_algorithm
        )) is False:
            messagebox.showwarning('Warning', 'No algorithm selected.')
            return

        if self._start_x is None:
            self._start_x = event.x // self._grid_size
            self._start_y = event.y // self._grid_size

            self._canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill="red")
        else:
            end_x = event.x // self._grid_size
            end_y = event.y // self._grid_size

            self._canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill="red")

            if self._current_line_algorithm is not None:
                algorithm = self._current_line_algorithm(self._start_x, self._start_y, end_x, end_y)
            elif self._current_curve_algorithm is not None:
                algorithm = self._current_curve_algorithm(self._start_x, self._start_y, end_x, end_y)
            elif self._current_parametric_algorithm is not None:
                algorithm = self._current_parametric_algorithm(self._start_x, self._start_y, end_x, end_y)
            else:
                raise "'algorithm' variable is undeclared"
            points_to_draw = algorithm.get_points()

            if self._debug_mode:
                self._draw_points_with_latency(points_to_draw, 0)
            else:
                self._draw_points(points_to_draw)

            self._start_x = None
            self._start_y = None

    def _draw_points_with_latency(self, points, index):
        if index >= len(points):
            return
        x, y, color = points[index]
        self._canvas.create_rectangle(
            x * self._grid_size,
            y * self._grid_size,
            (x + 1) * self._grid_size,
            (y + 1) * self._grid_size,
            outline="black",
            fill=color
        )
        print(f"Point: {x:5} {y:5}")
        self.after(50, lambda: self._draw_points_with_latency(points, index + 1))

    def _draw_points(self, points):
        for point in points:
            x, y, color = point
            self._canvas.create_rectangle(
                x * self._grid_size,
                y * self._grid_size,
                (x + 1) * self._grid_size,
                (y + 1) * self._grid_size,
                outline='black',
                fill=color
            )

    def _draw_grid(self):
        self._canvas.delete("grid")
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()

        for x in range(0, width, self._grid_size):
            self._canvas.create_line(x, 0, x, height, fill="lightgray", tags="grid")

        for y in range(0, height, self._grid_size):
            self._canvas.create_line(0, y, width, y, fill="lightgray", tags="grid")

    def _set_line_algorithm(self, algorithm):
        self._uncheck_all_algorithms()

        match algorithm:
            case "DDA":
                self._current_line_algorithm = DDA
                self.title("DDA")
            case "Bresenham":
                self._current_line_algorithm = Bresenham
                self.title("Bresenham")
            case "Wu":
                self._current_line_algorithm = Wu
                self.title("Wu")

    def _uncheck_all_algorithms(self):
        self._current_line_algorithm = None

    @staticmethod
    def _launch_script(script_name):
        current_directory = os.getcwd()
        script_path = os.path.join(current_directory, script_name)
        if os.path.isfile(script_path):
            try:
                subprocess.run(['python3', script_path], check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror('Error', f'Error while executing script: {e}')
        else:
            messagebox.showerror('Error', 'Script not found.')


def main():
    app = DrawingApp()
    app.mainloop()


if __name__ == '__main__':
    main()
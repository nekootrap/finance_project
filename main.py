import tkinter as tk
from widgets import menu_button, main_menu


def create_app() -> None:
    """Создать и запустить главное окно приложения.

    Инициализирует окно Tkinter, задает геометрию, создает боковую панель
    и основную область контента, затем запускает главный цикл событий.
    """
    root = tk.Tk()
    root.title("Менеджер бюджета")
    root.geometry("800x600")

    sidebar_frame = tk.Frame(root, background='azure2', width=200)
    sidebar_frame.pack(side='left', fill='y')

    frame = tk.Frame(root, background='azure')
    frame.pack(side='right', fill='both', expand=True)

    menu_button(sidebar_frame, frame)
    main_menu(frame)

    root.mainloop()


if __name__ == "__main__":
    create_app()
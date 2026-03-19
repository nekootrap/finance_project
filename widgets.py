import tkinter as tk
from datetime import datetime
import storage


def clear_frame(frame: tk.Frame) -> None:
    """Очистить окно от всех виджетов.

    Args:
        frame (tk.Frame): Окно программы, которое необходимо очистить.
    """
    for widget in frame.winfo_children():
        widget.destroy()


def create_category_row(frame: tk.Frame, category: str, amount: float, color: str, row: int) -> None:
    """Создать строку с категорией и суммой в указанном фрейме.

    Args:
        frame (tk.Frame): Контейнер для размещения виджетов.
        category (str): Название категории.
        amount (float): Сумма операции.
        color (str): Цвет текста для суммы.
        row (int): Номер строки в сетке.
    """
    tk.Label(
        frame,
        text=category,
        background="azure",
        anchor="w",
        font=("Arial", 10)
    ).grid(row=row, column=0, sticky="w", padx=10, pady=3)

    tk.Label(
        frame,
        text=f"{amount:.2f} ₽",
        background="azure",
        fg=color,
        font=("Arial", 10, "bold")
    ).grid(row=row, column=1, sticky="e", padx=10, pady=3)


def show_main_stats(frame: tk.Frame) -> None:
    """Отобразить статистику по категориям за текущий месяц.

    Функция очищает переданный фрейм и заполняет его данными о доходах,
    расходах и балансе за текущий месяц, полученными из модуля storage.

    Args:
        frame (tk.Frame): Основной фрейм для отображения статистики.
    """
    clear_frame(frame)
    now = datetime.now()
    month_name = now.strftime("%B %Y")

    tk.Label(
        frame,
        text=f"Статистика за {month_name}",
        background="azure",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    income_cats, expense_cats = storage.get_category_stats(now.year, now.month)
    total_income = sum(income_cats.values())
    total_expense = sum(expense_cats.values())
    balance = total_income - total_expense

    top_frame = tk.Frame(frame, background="azure2", pady=10)
    top_frame.pack(fill="x", padx=40, pady=5)

    tk.Label(
        top_frame,
        text=f"Доходы: {total_income:.2f} ₽",
        background="azure2",
        fg="green",
        font=("Arial", 13, "bold")
    ).pack(side="left", padx=40)

    tk.Label(
        top_frame,
        text=f"Расходы: {total_expense:.2f} ₽",
        background="azure2",
        fg="red",
        font=("Arial", 13, "bold")
    ).pack(side="left", padx=40)

    separator = tk.Frame(frame, height=2, background="steelblue")
    separator.pack(fill="x", padx=40, pady=10)

    main_container = tk.Frame(frame, background="azure")
    main_container.pack(fill="both", expand=True, padx=40)

    left_frame = tk.Frame(main_container, background="azure")
    left_frame.pack(side="left", fill="both", expand=True)

    right_frame = tk.Frame(main_container, background="azure")
    right_frame.pack(side="right", fill="both", expand=True)

    tk.Label(
        left_frame,
        text="ДОХОДЫ",
        background="azure",
        fg="green",
        font=("Arial", 12, "bold")
    ).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(
        right_frame,
        text="РАСХОДЫ",
        background="azure",
        fg="red",
        font=("Arial", 12, "bold")
    ).grid(row=0, column=0, columnspan=2, pady=10)

    row = 1
    if income_cats:
        for category, amount in sorted(income_cats.items()):
            create_category_row(left_frame, category, amount, "green", row)
            row += 1
    else:
        tk.Label(
            left_frame,
            text="Нет данных",
            background="azure",
            fg="gray"
        ).grid(row=1, column=0, columnspan=2, pady=10)

    row = 1
    if expense_cats:
        for category, amount in sorted(expense_cats.items()):
            create_category_row(right_frame, category, amount, "red", row)
            row += 1
    else:
        tk.Label(
            right_frame,
            text="Нет данных",
            background="azure",
            fg="gray"
        ).grid(row=1, column=0, columnspan=2, pady=10)

    separator2 = tk.Frame(frame, height=2, background="steelblue")
    separator2.pack(fill="x", padx=40, pady=10)

    bottom_frame = tk.Frame(frame, background="azure2", pady=15)
    bottom_frame.pack(fill="x", padx=40, pady=5)

    balance_color = "green" if balance >= 0 else "red"
    balance_text = "Положительный" if balance >= 0 else "Отрицательный"

    tk.Label(
        bottom_frame,
        text=f"Баланс за месяц: {balance:.2f} ₽",
        background="azure2",
        fg=balance_color,
        font=("Arial", 15, "bold")
    ).pack()

    tk.Label(
        bottom_frame,
        text=f"({balance_text})",
        background="azure2",
        fg="gray",
        font=("Arial", 10)
    ).pack()


def show_add_operation(frame: tk.Frame) -> None:
    """Отобразить экран добавления новой операции.

    Создает интерфейс для ввода суммы, категории и типа операции.
    При сохранении данные валидируются и записываются через модуль storage.

    Args:
        frame (tk.Frame): Фрейм, в котором будет размещен интерфейс добавления.
    """
    clear_frame(frame)
    lbl_title = tk.Label(
        frame,
        text="Новая операция",
        background="azure",
        font=("Arial", 16)
    )
    lbl_title.pack(pady=10)

    tk.Label(
        frame,
        text="Сумма: ",
        background="azure",
        font=("Arial", 11)
    ).pack(pady=5)
    entry_amount = tk.Entry(frame, font=("Arial", 11))
    entry_amount.pack(pady=5)

    tk.Label(
        frame,
        text="Категория: ",
        background="azure",
        font=("Arial", 11)
    ).pack(pady=5)
    entry_category = tk.Entry(frame, font=("Arial", 11))
    entry_category.pack(pady=5)

    tk.Label(
        frame,
        text="Тип операции: ",
        background="azure",
        font=("Arial", 11)
    ).pack(pady=5)
    var_type = tk.StringVar(value="Расход")
    combo_type = tk.OptionMenu(frame, var_type, "Доход", "Расход")
    combo_type.config(font=("Arial", 11), width=15)
    combo_type.pack(pady=5)

    def save() -> None:
        try:
            amount = float(entry_amount.get())
            if amount <= 0:
                raise ValueError("Сумма должна быть положительной")
            transaction = {
                "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
                "amount": amount,
                "category": entry_category.get(),
                "type": var_type.get()
            }
            storage.add_transaction(transaction)
            show_main_stats(frame)
        except ValueError as e:
            clear_frame(frame)
            tk.Label(
                frame,
                text=f"Ошибка! {str(e)}",
                background="azure",
                fg="red",
                font=("Arial", 12)
            ).pack(pady=20)
            btn_back = tk.Button(
                frame,
                text="Назад",
                command=lambda: show_main_stats(frame),
                font=("Arial", 11)
            )
            btn_back.pack(pady=10)

    btn_save = tk.Button(
        frame,
        text="Сохранить",
        command=save,
        font=("Arial", 11),
        width=15
    )
    btn_save.pack(pady=20)

    btn_back = tk.Button(
        frame,
        text="Назад",
        command=lambda: show_main_stats(frame),
        font=("Arial", 11),
        width=15
    )
    btn_back.pack(pady=5)


def show_edit_operation(frame: tk.Frame, index: int) -> None:
    """Отобразить экран редактирования существующей операции.

    Загружает данные операции по индексу, позволяет изменить сумму,
    категорию и тип, затем сохраняет изменения.

    Args:
        frame (tk.Frame): Фрейм для отображения формы редактирования.
        index (int): Индекс операции в списке всех транзакций.
    """
    clear_frame(frame)
    data = storage.get_all_transactions()
    if index < 0 or index >= len(data):
        tk.Label(
            frame,
            text="Операция не найдена",
            background="azure",
            fg="red"
        ).pack(pady=20)
        btn_back = tk.Button(
            frame,
            text="Назад",
            command=lambda: show_all_operations(frame)
        )
        btn_back.pack()
        return

    transaction = data[index]

    lbl_title = tk.Label(
        frame,
        text="Редактировать операцию",
        background="azure",
        font=("Arial", 16)
    )
    lbl_title.pack(pady=10)

    tk.Label(
        frame,
        text="Сумма: ",
        background="azure",
        font=("Arial", 11)
    ).pack(pady=5)
    entry_amount = tk.Entry(frame, font=("Arial", 11))
    entry_amount.insert(0, str(transaction["amount"]))
    entry_amount.pack(pady=5)

    tk.Label(
        frame,
        text="Категория: ",
        background="azure",
        font=("Arial", 11)
    ).pack(pady=5)
    entry_category = tk.Entry(frame, font=("Arial", 11))
    entry_category.insert(0, transaction["category"])
    entry_category.pack(pady=5)

    tk.Label(
        frame,
        text="Тип операции: ",
        background="azure",
        font=("Arial", 11)
    ).pack(pady=5)
    var_type = tk.StringVar(value=transaction["type"])
    combo_type = tk.OptionMenu(frame, var_type, "Доход", "Расход")
    combo_type.config(font=("Arial", 11), width=15)
    combo_type.pack(pady=5)

    def save() -> None:
        try:
            amount = float(entry_amount.get())
            if amount <= 0:
                raise ValueError("Сумма должна быть положительной")
            data[index]["amount"] = amount
            data[index]["category"] = entry_category.get()
            data[index]["type"] = var_type.get()
            storage.save_data(data)
            show_all_operations(frame)
        except ValueError as e:
            tk.Label(
                frame,
                text=f"Ошибка! {str(e)}",
                background="azure",
                fg="red"
            ).pack(pady=10)

    btn_save = tk.Button(
        frame,
        text="Сохранить изменения",
        command=save,
        font=("Arial", 11),
        width=20
    )
    btn_save.pack(pady=20)

    btn_back = tk.Button(
        frame,
        text="Отмена",
        command=lambda: show_all_operations(frame),
        font=("Arial", 11),
        width=15
    )
    btn_back.pack(pady=5)


def show_all_operations(frame: tk.Frame) -> None:
    """Отобразить список всех операций с возможностью редактирования.

    Выводит последние 50 операций в прокручиваемом списке.
    Каждая строка содержит дату, категорию, сумму, тип и кнопку редактирования.

    Args:
        frame (tk.Frame): Фрейм для отображения списка операций.
    """
    clear_frame(frame)
    lbl = tk.Label(
        frame,
        text="Все операции",
        background="azure",
        font=("Arial", 16, "bold")
    )
    lbl.pack(pady=15)
    data = storage.get_all_transactions()

    if not data:
        tk.Label(
            frame,
            text="Нет операций",
            background="azure",
            fg="gray",
            font=("Arial", 12)
        ).pack(pady=20)
        btn_back = tk.Button(
            frame,
            text="На главную",
            command=lambda: show_main_stats(frame),
            font=("Arial", 11)
        )
        btn_back.pack(pady=10)
        return

    list_container = tk.Frame(frame, background="azure")
    list_container.pack(fill="both", expand=True, padx=20)

    header_frame = tk.Frame(list_container, background="steelblue", height=30)
    header_frame.pack(fill="x", pady=5)
    tk.Label(
        header_frame,
        text="Дата",
        background="steelblue",
        fg="white",
        font=("Arial", 10, "bold"),
        width=18
    ).pack(side="left", padx=5)
    tk.Label(
        header_frame,
        text="Категория",
        background="steelblue",
        fg="white",
        font=("Arial", 10, "bold"),
        width=15
    ).pack(side="left", padx=5)
    tk.Label(
        header_frame,
        text="Сумма",
        background="steelblue",
        fg="white",
        font=("Arial", 10, "bold"),
        width=12
    ).pack(side="left", padx=5)
    tk.Label(
        header_frame,
        text="Тип",
        background="steelblue",
        fg="white",
        font=("Arial", 10, "bold"),
        width=10
    ).pack(side="left", padx=5)
    tk.Label(
        header_frame,
        text=" ",
        background="steelblue",
        width=10
    ).pack(side="left")

    canvas = tk.Canvas(
        list_container,
        background="azure",
        highlightthickness=0
    )
    scrollbar = tk.Scrollbar(
        list_container, 
        orient="vertical", 
        command=canvas.yview
        )
    scrollable_frame = tk.Frame(canvas, background="azure")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for i, t in enumerate(reversed(data[-50:])):
        row_index = len(data) - 1 - i
        color = "green" if t['type'] == 'Доход' else "red"

        row_frame = tk.Frame(scrollable_frame, background="azure")
        row_frame.pack(fill="x", pady=2)

        tk.Label(
            row_frame,
            text=t['date'],
            background="azure",
            width=18,
            anchor="w"
        ).pack(side="left", padx=5)
        tk.Label(
            row_frame,
            text=t['category'],
            background="azure",
            width=15,
            anchor="w"
        ).pack(side="left", padx=5)
        tk.Label(
            row_frame,
            text=f"{t['amount']:.2f} ₽",
            background="azure",
            fg=color,
            width=12,
            anchor="w"
        ).pack(side="left", padx=5)
        tk.Label(
            row_frame,
            text=t['type'],
            background="azure",
            width=10,
            anchor="w"
        ).pack(side="left", padx=5)

        btn_edit = tk.Button(
            row_frame,
            text="~",
            width=3,
            command=lambda idx=row_index: show_edit_operation(frame, idx),
            font=("Arial", 9)
        )
        btn_edit.pack(side="left", padx=5)

    btn_back = tk.Button(
        frame,
        text="На главную",
        command=lambda: show_main_stats(frame),
        font=("Arial", 11),
        width=15
    )
    btn_back.pack(pady=10)


def menu_button(frame: tk.Frame, content_frame: tk.Frame) -> None:
    """Создать кнопки главного меню в боковой панели.

    Размещает кнопки навигации (Главная, Добавить, Все операции)
    в указанном фрейме с фиксированными координатами.

    Args:
        frame (tk.Frame): Фрейм боковой панели для размещения кнопок.
        content_frame (tk.Frame): Целевой фрейм для отображения
                                  контента при нажатии.
    """
    btn_home = tk.Button(
        frame,
        text="Главная",
        command=lambda: show_main_stats(content_frame),
        font=("Arial", 11)
    )
    btn_home.place(x=25, y=50, width=150)

    btn_add = tk.Button(
        frame,
        text="Добавить",
        command=lambda: show_add_operation(content_frame),
        font=("Arial", 11)
    )
    btn_add.place(x=25, y=100, width=150)

    btn_report = tk.Button(
        frame,
        text="Все операции",
        command=lambda: show_all_operations(content_frame),
        font=("Arial", 11)
    )
    btn_report.place(x=25, y=150, width=150)


def main_menu(frame: tk.Frame) -> None:
    """Инициализировать главное меню приложения.

    Отображает основную статистику в переданном фрейме при запуске.

    Args:
        frame (tk.Frame): Основной фрейм приложения.
    """
    show_main_stats(frame)
import json
import os
from datetime import datetime
from typing import List, Dict, Tuple, Any

FILE_NAME = "data.json"


def get_path() -> str:
    """Получить полный путь к файлу данных.

    Returns:
        str: Абсолютный путь к файлу data.json.
    """
    return os.path.join(os.path.dirname(__file__), FILE_NAME)


def load_data() -> List[Dict[str, Any]]:
    """Загрузить данные транзакций из JSON файла.

    Если файл не существует или содержит ошибку формата, возвращается пустой список.

    Returns:
        List[Dict[str, Any]]: Список словарей с данными транзакций.
    """
    path = get_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_data( List[Dict[str, Any]]) -> None:
    """Сохранить данные транзакций в JSON файл.

    Args:
        data (List[Dict[str, Any]]): Список словарей с данными для сохранения.
    """
    path = get_path()
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def add_transaction(transaction: Dict[str, Any]) -> None:
    """Добавить новую транзакцию в список и сохранить изменения.

    Args:
        transaction (Dict[str, Any]): Словарь с данными новой транзакции.
    """
    data = load_data()
    data.append(transaction)
    save_data(data)


def get_all_transactions() -> List[Dict[str, Any]]:
    """Получить список всех сохраненных транзакций.

    Returns:
        List[Dict[str, Any]]: Полный список всех транзакций.
    """
    return load_data()


def get_transactions_by_month(year: int, month: int) -> List[Dict[str, Any]]:
    """Получить список транзакций за указанный год и месяц.

    Args:
        year (int): Год для фильтрации.
        month (int): Месяц для фильтрации.

    Returns:
        List[Dict[str, Any]]: Отфильтрованный список транзакций.
    """
    data = load_data()
    result = []
    for t in data:
        try:
            date_obj = datetime.strptime(t['date'], "%d.%m.%Y %H:%M")
            if date_obj.year == year and date_obj.month == month:
                result.append(t)
        except (ValueError, KeyError):
            continue
    return result


def get_category_stats(year: int, month: int) -> Tuple[Dict[str, float], Dict[str, float]]:
    """Группировать операции по категориям за указанный месяц.

    Разделяет суммы на доходы и расходы по категориям.

    Args:
        year (int): Год для анализа.
        month (int): Месяц для анализа.

    Returns:
        Tuple[Dict[str, float], Dict[str, float]]: Кортеж из двух словарей:
            первый содержит суммы доходов по категориям,
            второй — суммы расходов по категориям.
    """
    transactions = get_transactions_by_month(year, month)
    income_categories: Dict[str, float] = {}
    expense_categories: Dict[str, float] = {}

    for t in transactions:
        category = t.get('category', 'Без категории')
        amount = t.get('amount', 0)
        t_type = t.get('type', 'Расход')

        if t_type == 'Доход':
            income_categories[category] = income_categories.get(category, 0) + amount
        else:
            expense_categories[category] = expense_categories.get(category, 0) + amount

    return income_categories, expense_categories
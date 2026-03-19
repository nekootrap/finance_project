import json
import os
from datetime import datetime

FILE_NAME = "data.json"

def get_path():
    return os.path.join(os.path.dirname(__file__), FILE_NAME)

def load_data():
    path = get_path()
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(data):
    path = get_path()
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_transaction(transaction):
    data = load_data()
    data.append(transaction)
    save_data(data)

def get_all_transactions():
    return load_data()

def get_transactions_by_month(year, month):
    """Получить операции за конкретный месяц"""
    data = load_data()
    result = []
    for t in data:
        try:
            date_obj = datetime.strptime(t['date'], "%d.%m.%Y %H:%M")
            if date_obj.year == year and date_obj.month == month:
                result.append(t)
        except:
            continue
    return result

def get_category_stats(year, month):
    """Группировка операций по категориям за месяц"""
    transactions = get_transactions_by_month(year, month)
    
    income_categories = {}
    expense_categories = {}
    
    for t in transactions:
        category = t.get('category', 'Без категории')
        amount = t.get('amount', 0)
        t_type = t.get('type', 'Расход')
        
        if t_type == 'Доход':
            income_categories[category] = income_categories.get(category, 0) + amount
        else:
            expense_categories[category] = expense_categories.get(category, 0) + amount
    
    return income_categories, expense_categories
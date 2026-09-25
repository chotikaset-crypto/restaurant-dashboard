import json
import os
from typing import List, Dict, Any

# กำหนด Path ไปยังไฟล์ JSON ข้อมูลเมนูอาหาร
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/sales_data.json")

# ฟังก์ชันที่ 1: โหลดข้อมูลพร้อมระบบป้องกัน Error (Try/Except)
def load_sales_data() -> List[Dict[str, Any]]:
    try:
        if not os.path.exists(DATA_PATH):
            return []
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")
        return []

# ฟังก์ชันที่ 2: คำนวณยอดขายรวมทั้งหมด (ราคา x จำนวน)
def calculate_total_sales(data: List[Dict[str, Any]]) -> float:
    total = 0.0
    for item in data:
        try:
            price = float(item.get("price", 0))
            qty = int(item.get("quantity", 0))
            total += price * qty
        except (ValueError, TypeError):
            continue
    return total

# ฟังก์ชันที่ 3: คำนวณจำนวนจาน/รายการที่ขายได้ทั้งหมด
def calculate_total_orders(data: List[Dict[str, Any]]) -> int:
    return sum(int(item.get("quantity", 0)) for item in data if isinstance(item.get("quantity"), int))

# ฟังก์ชันที่ 4: สรุปยอดขายแยกตามหมวดหมู่เพื่อส่งให้ Chart.js
def get_sales_by_category(data: List[Dict[str, Any]]) -> Dict[str, float]:
    category_summary = {}
    for item in data:
        cat = item.get("category", "อื่นๆ")
        sales = float(item.get("price", 0)) * int(item.get("quantity", 0))
        category_summary[cat] = category_summary.get(cat, 0.0) + sales
    return category_summary

# ฟังก์ชันที่ 5: หาเมนูขายดีอันดับ 1
def get_top_selling_menu(data: List[Dict[str, Any]]) -> str:
    if not data:
        return "ไม่มีข้อมูล"
    sorted_items = sorted(data, key=lambda x: int(x.get("quantity", 0)), reverse=True)
    return sorted_items[0].get("menu", "N/A")

# ฟังก์ชันที่ 6: ตรวจสอบความถูกต้องของข้อมูล (Validation)
def validate_menu_input(price: float, quantity: int) -> bool:
    if not isinstance(price, (int, float)) or not isinstance(quantity, int):
        return False
    if price < 0 or quantity < 0:
        return False
    return True
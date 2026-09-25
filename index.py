from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import sys

# เพิ่ม Path อ้างอิงโฟลเดอร์ utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_manager import (
    load_sales_data,
    calculate_total_sales,
    calculate_total_orders,
    get_sales_by_category,
    get_top_selling_menu
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def get_dashboard(request: Request):
    try:
        # โหลดข้อมูลเมนูทั้งหมด 60 รายการ
        raw_data = load_sales_data()
        
        # คำนวณค่าต่างๆ ผ่านฟังก์ชันใน utils
        total_sales = calculate_total_sales(raw_data)
        total_orders = calculate_total_orders(raw_data)
        top_menu = get_top_selling_menu(raw_data)
        category_sales = get_sales_by_category(raw_data)
        
        # แยก Label และ Data สำหรับกราฟ
        labels = list(category_sales.keys())
        chart_data = list(category_sales.values())

        # ส่งค่าไปยัง Template dashboard.html
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "total_sales": f"{total_sales:,.2f}",
            "total_orders": f"{total_orders:,}",
            "top_menu": top_menu,
            "labels": labels,
            "chart_data": chart_data,
            "raw_data": raw_data
        })
    except Exception as e:
        return HTMLResponse(content=f"<h3>เกิดข้อผิดพลาดในการโหลด Dashboard: {str(e)}</h3>", status_code=500)
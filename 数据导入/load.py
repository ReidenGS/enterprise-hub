import os
import django
import csv
from datetime import date
import re

# --- 请修改以下两行 ---
# 1. 将 'your_project_name' 替换为您的Django项目名称
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app01')
# 2. 将 'path/to/your/file.csv' 替换为CSV文件的实际路径
CSV_FILE_PATH = '客户拜访记录表.xlsx - Sheet3.csv'
# ---------------------

django.setup()

# 从您的sells_model中导入所需模型
# 注意：我们已经移除了 Visit 模型
from model import Client, ClientContact, ClientGeneration, ClientEquipment, ClientPurchase, SellsQuotation, \
    VisitRecord


def import_data(csv_file_path):
    """
    从指定的CSV文件将数据导入到Django数据库。
    此版本直接将拜访记录和备注存入 VisitRecord 模型。
    """
    print("开始导入数据...")
    try:
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:  # 使用 utf-8-sig 编码以处理BOM头
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                # 跳过公司名称为空的行
                company_name = row.get('公司名称', '').strip()
                if not company_name:
                    print(f"第 {i + 2} 行：跳过，因为公司名称为空。")
                    continue

                # 1. 创建或获取 Client 对象
                client, client_created = Client.objects.get_or_create(
                    name=company_name,
                    defaults={'address': row.get('公司地址', '').strip()}
                )
                if not client_created:
                    # 如果客户已存在，则更新其地址
                    client.address = row.get('公司地址', '').strip()

                # 2. 处理联系人1 (直接更新Client模型)
                contact1_text = row.get('联系人1', '').strip()
                if contact1_text:
                    match = re.match(r'(.+?)(\d+)', contact1_text)  # 尝试分离姓名和电话
                    if match:
                        name, phone = match.groups()
                        client.contact = name.strip()
                        client.phone = phone.strip()
                    else:
                        client.contact = contact1_text  # 如果没有电话，则全部视为姓名
                        client.phone = ''  # 清空电话字段
                client.save()

                # 3. 处理联系人2 (存入 ClientContact)
                contact2_text = row.get('联系人2', '').strip()
                if contact2_text:
                    match = re.match(r'(.+?)(\d+)', contact2_text)
                    if match:
                        name, phone = match.groups()
                        ClientContact.objects.get_or_create(client=client, name=name.strip(),
                                                            defaults={'phone': phone.strip()})
                    else:
                        ClientContact.objects.get_or_create(client=client, name=contact2_text)

                # 4. 处理联系人3 (存入 ClientContact)
                contact3_text = row.get('联系人3', '').strip()
                if contact3_text:
                    match = re.match(r'(.+?)(\d+)', contact3_text)
                    if match:
                        name, phone = match.groups()
                        ClientContact.objects.get_or_create(client=client, name=name.strip(),
                                                            defaults={'phone': phone.strip()})
                    else:
                        ClientContact.objects.get_or_create(client=client, name=contact3_text)

                # 5. 处理所做产品 (存入 ClientGeneration)
                products = row.get('所做产品', '').strip()
                if products:
                    for product_name in re.split(r'[、,，\s]+', products):
                        if product_name:
                            ClientGeneration.objects.get_or_create(client=client, name=product_name.strip())

                # 6. 处理现有设备 (存入 ClientEquipment)
                equipments = row.get('现有设备', '').strip()
                if equipments:
                    for equipment_name in re.split(r'[、,，\s]+', equipments):
                        if equipment_name:
                            ClientEquipment.objects.get_or_create(client=client, name=equipment_name.strip())

                # 7. 处理购买记录 (存入 ClientPurchase)
                purchases = row.get('购买记录', '').strip()
                if purchases:
                    for purchase_name in re.split(r'[、,，\s]+', purchases):
                        if purchase_name:
                            ClientPurchase.objects.get_or_create(client=client, name=purchase_name.strip())

                # 8. 处理报价 (存入 SellsQuotation)
                quotations = row.get('报价', '').strip()
                if quotations:
                    for quotation_name in re.split(r'[、,，\s]+', quotations):
                        if quotation_name:
                            SellsQuotation.objects.get_or_create(client=client, name=quotation_name.strip())

                # 9. 将备注和拜访记录合并，并直接创建 VisitRecord
                remarks = row.get('备注', '').strip()
                # CSV的列名可能包含换行符，需要精确匹配
                visit_log_key = next((key for key in reader.fieldnames if '拜访记录' in key), None)
                visit_log = row.get(visit_log_key, '').strip() if visit_log_key else ''

                # 拼接备注和拜访记录
                combined_message = f"备注：{remarks}\n拜访记录：{visit_log}".strip()

                # 如果有内容，则创建VisitRecord
                # 假设 VisitRecord 模型有 client, visit_date, 和 other_message 字段
                if remarks or visit_log:
                    VisitRecord.objects.create(
                        client=client,
                        visit_date=date.today(),
                        other_message=combined_message,
                        # 模型中的其他字段将使用其默认值
                    )
                print(f"第 {i + 2} 行：成功处理客户 “{company_name}”。")

    except FileNotFoundError:
        print(f"错误：找不到文件 '{csv_file_path}'。请检查文件路径是否正确。")
    except Exception as e:
        print(f"导入过程中发生错误: {e}")


if __name__ == '__main__':
    import_data(CSV_FILE_PATH)
    print("数据导入任务完成！")
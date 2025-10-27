# 🌐 Enterprise Hub / 企业中心平台

A full-stack enterprise management system combining a **WeChat Mini Program for users** and a **Django-based admin web interface for managers**, powered by a **Django REST backend**.
本项目是一个结合 **微信小程序（用户端）** 与 **Django 管理网页（管理员端）** 的企业管理平台，后端使用 **Django REST Framework** 实现接口与业务逻辑。系统集成了 **报修管理**、**销售计划与报表** 以及 **员工考勤数据清洗** 功能，用于作品展示与求职。

---

## 🧠 System Architecture / 系统架构

```
WeChat Mini Program (User Frontend)
        ↓ RESTful API (JSON)
Django Backend (DRF, Business Logic)
        ↓
Django Admin Web Interface (Management Frontend)
        ↓
MySQL / PostgreSQL Database
```

* **WeChat Mini Program (用户端)**：企业员工使用，负责发起报修、上传图片、查看处理状态。
* **Django Web Interface (管理端)**：企业管理员使用，基于 Django 自带模板系统，提供中文网页界面，用于审核、统计与数据维护。
* **Django REST Backend (后端)**：负责接口通信、数据存储、文件处理与逻辑控制。
* 前后端通过 **HTTPS + JSON** 进行安全通信。

---

## 🚀 Features Overview / 功能概览

### 📱 User Frontend — WeChat Mini Program / 用户端 — 微信小程序

* Search company names and equipment information.
  搜索企业名称及设备信息。
* Submit repair requests with image uploads.
  提交带图片的报修单。
* View repair progress and feedback.
  查看报修进度与反馈。
* User interface fully in Chinese for domestic accessibility.
  界面为中文，方便国内用户操作。

### 💻 Admin Frontend — Django Web Interface / 管理端 — Django 网页前端

* Manage repair orders, assign technicians, and close cases.
  管理报修单、分配人员、关闭任务。
* View, edit, and export visit and sales records.
  查看、编辑并导出销售拜访记录。
* Perform automated employee attendance data cleaning and validation.
  自动清洗与校验员工考勤数据。
* Entire admin interface is built in **Chinese** using Django templates.
  管理端使用 Django 自带模板系统，提供 **中文界面**。

---

## 📱 WeChat Mini Program Access / 微信小程序体验

You can directly access the deployed Mini Program from WeChat:
您可直接在微信中搜索并体验已上线的小程序：

**Mini Program Name / 小程序名称：** `景曜服务`
**Search Method / 搜索方式：** 打开微信 → 搜索框输入 “景曜服务”

📸 *(Optional: Add QR Code Image Here)*
可在此处插入小程序二维码截图，方便扫码访问。

The Mini Program connects in real time to the Django backend hosted on Alibaba Cloud.
小程序实时调用部署在阿里云上的 Django 后端 API。

---

## 🧩 Tech Stack / 技术栈

* **User Frontend / 用户端：** WeChat Mini Program (WXML, WXSS, JavaScript)
* **Admin Frontend / 管理端：** Django Templates (HTML, CSS, Bootstrap, Jinja2)
* **Backend / 后端：** Django, Django REST Framework
* **Database / 数据库：** MySQL / PostgreSQL
* **File Handling / 文件处理：** openpyxl, pandas, python-docx
* **Deployment / 部署：** Alibaba Cloud (ECS), Nginx, Gunicorn

---

## ⚙️ Backend Setup / 后端环境配置

```bash
# 1️⃣ Clone the repository / 克隆项目
git clone https://github.com/yourusername/enterprise-hub.git
cd enterprise-hub

# 2️⃣ Create and activate virtual environment / 创建并激活虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或 .venv\Scripts\activate 在 Windows

# 3️⃣ Install dependencies / 安装依赖
pip install -r requirements.txt

# 4️⃣ Apply migrations / 迁移数据库
python manage.py migrate

# 5️⃣ Run the local server / 启动本地服务器
python manage.py runserver
```

Backend API will run at **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🌩️ Deployment (Alibaba Cloud) / 部署（阿里云）

The backend and admin interface are deployed on **Alibaba Cloud ECS** using **Nginx + Gunicorn**, and the Mini Program connects to the APIs via HTTPS.
后端与管理端部署在 **阿里云 ECS** 上（Nginx + Gunicorn），微信小程序通过 HTTPS 调用后端接口。

* Configure an HTTPS domain for API access. / 为 API 接口配置 HTTPS 域名与证书
* Collect static files via `collectstatic`. / 使用 collectstatic 收集静态文件
* Store `.env` securely with sensitive data. / 安全存放环境变量文件 `.env`

🔗 [Demo of the repair backend system on Alibaba Cloud / 报修后台系统阿里云演示链接](https://szjysk.xyz)

Login account / 用户账号 ： test

password / 密码 ：test

🔗 [Demo of the data cleaning on Alibaba Cloud / 员工考情数据清洗阿里云演示链接](https://szjysk.xyz/attendance_info/)

---

## 📄 License / 许可协议

This project is licensed under the **MIT License** — free to view and learn from with proper attribution.
本项目采用 **MIT License**，允许他人学习和参考代码，但需保留署名。

---

## 👤 Author / 作者

**Junkun Wen**
📧 [jw9697@nyu.edu](mailto:jw9697@nyu.edu)
🌐 [GitHub Profile](https://github.com/ReidenGS)

---

⭐ *If you find this project useful, please consider starring it on GitHub!*
如果你觉得这个项目有帮助，请在 GitHub 上为它点亮一颗星 ⭐

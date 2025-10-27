from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer,Image
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
from reportlab.lib.units import cm,mm
from djangoProject import settings
import os


def generate_quotation(companyName,fileName,data=None,status=0):
    # 1. 注册系统中文字体（Windows系统通常有以下字体）
    # 修改印章相关代码
    seal_image_path = os.path.join(settings.MEDIA_ROOT, "project_images", "companyPatton.jpg")

    # 确保路径正确
    print(f"印章路径: {seal_image_path}")
    output_path = settings.MEDIA_ROOT + '/quotation'
    try:
        # 尝试注册常见中文字体
        fonts_folder = "C:/Windows/Fonts/"
        if os.path.exists(os.path.join(fonts_folder, "simsun.ttc")):
            pdfmetrics.registerFont(TTFont("SimSun", os.path.join(fonts_folder, "simsun.ttc")))
            default_cn_font = "SimSun"
        elif os.path.exists(os.path.join(fonts_folder, "msyh.ttf")):
            pdfmetrics.registerFont(TTFont("MicrosoftYaHei", os.path.join(fonts_folder, "msyh.ttf")))
            default_cn_font = "MicrosoftYaHei"
        else:
            # 如果系统没有常见中文字体，使用reportlab自带的黑体
            pdfmetrics.registerFont(TTFont("STHeiti", "STHeiti-Medium.ttf"))
            default_cn_font = "STHeiti"
    except:
        # 如果以上都失败，尝试使用内置字体
        default_cn_font = "Helvetica"
        print("警告：未找到中文字体，中文可能显示异常")

    print (default_cn_font)
    # output_filename = output_path +"/"+ companyName+'/' + fileName +".pdf"

    file_path = os.path.join(
        settings.MEDIA_ROOT,  # 或 settings.MEDIA_ROOT 如果你使用媒体文件
        'quotation',
        f'{companyName}',
        f'{fileName}.pdf',
    )
    dir_path = os.path.join(
        settings.MEDIA_ROOT,  # 或 settings.MEDIA_ROOT 如果你使用媒体文件
        'quotation',
        f'{companyName}',
    )
    os.makedirs(dir_path, exist_ok=True)  # exist_ok=True 避免目录已存在时报错
    # 2. 创建PDF文档
    doc = SimpleDocTemplate(file_path, pagesize=A4,
                            rightMargin=2 * cm, leftMargin=2 * cm,
                            topMargin=1 * cm, bottomMargin=1 * cm)

    # 3. 定义样式（全部使用中文字体）
    styles = getSampleStyleSheet()

    # 修改默认样式使用中文字体
    styles["Normal"].fontName = default_cn_font
    styles["Heading1"].fontName = default_cn_font
    styles["Heading2"].fontName = default_cn_font

    # 自定义样式
    company_style = ParagraphStyle(
        'Company',
        parent=styles['Heading1'],
        fontSize=14,
        fontName=default_cn_font,
        alignment=1,  # 居中
        spaceAfter=20
    )

    header_style = ParagraphStyle(
        'Header',
        parent=styles['Normal'],
        fontSize=10,
        fontName=default_cn_font,
        leading=14,
        spaceAfter=10
    )

    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        fontName=default_cn_font,
        alignment=1,
        spaceAfter=20
    )

    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        fontName=default_cn_font,
        leading=12,  # 减小行距
        spaceBefore=0,  # 减小与上方元素的间距
    )

    # 4. 构建文档内容
    content = []

    # 公司标题
    content.append(Paragraph("深圳市景曜数控设备有限公司", company_style))
    content.append(Paragraph("Shen Zhen Jing Yao Equipment CO., Ltd.", company_style))
    content.append(Spacer(1, 20))

    # 收件人信息
    recipient_info = Table([
        ["TO / 送 交：运丰（开平）电子制品有限公司",
        "Ref/参与：A0000089"],
        [f"Date/日期：{datetime.now().strftime('%Y-%m-%d')}", "From/发 件：罗晶"],
        ["Tel/电话：0750-2829021",
        "Subject/事由：配件报价"]
    ],colWidths=[10 * cm, 6 * cm])
    recipient_info.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), default_cn_font),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))

    content.append(recipient_info)
    # for line in recipient_info:
    #     content.append(Paragraph(line, header_style))

    content.append(Spacer(1, 20))

    # 报价单标题
    content.append(Paragraph("报价单    Quotation", title_style))
    content.append(Spacer(1, 20))

    # 报价表格
    table_data = [
        ["编号", "名称及型号", "单位", "数量", "税率%", "含税单价", "含税金额", "备注"],
        # ["1", "模具3.1 CKE.01-13/14", "套", "1", "13", "280", "280", ""],
        # ["1", "模具3.1 CKE.01-13/15", "套", "1", "13", "290", "290", ""],
    ]
    if data:
        for i in data:
            table_data.append(i)

    table = Table(table_data, colWidths=[1.5 * cm, 5 * cm, 1.5 * cm, 1.5 * cm, 1.5 * cm, 2 * cm, 2 * cm, 3 * cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), default_cn_font),  # 表头使用中文字体
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    content.append(table)
    content.append(Spacer(1, 20))

    # 银行信息
    if status == 0:
        bank_info = [
            "开户名：深圳市景曜数控设备有限公司",
            "开户行：建设银行股份有限公司深圳市横岗支行",
            "账号：4420 1558 5000 5250 4372",
            "",
            "付款方式：款到发货"
        ]
    else:
        bank_info = [
            "开户名：谭 小 年",
            "开户行：招商银行深圳市横岗支行",
            "账号：6214 8378 8557 0576",
            "",
            "付款方式：款到发货"
        ]

    for line in bank_info:
        content.append(Paragraph(line, styles['Normal']))

    content.append(Spacer(1, 20))

    # 备注信息
    notes = [
        "备  注：",
        "1、以上报价全部国内付款。",
        "2、贵公司若无异议，请签名并盖章回传。",
        "3、本报价单经买方签署并回传卖方之日起生效，传真件具同等法律效力。",
        "4、以上价格自报价之日起有效期为七天。",
        "",
        "以上报价经客户确认签回后视同订单。"
    ]

    for line in notes:
        content.append(Paragraph(line, styles['Normal']))

    content.append(Spacer(1, 30))

    # --- 签署区域 ---
    # 创建左侧签署区域表格
    left_sign_content = []

    # 添加签署文字（确保文字在印章上方）
    sign_text = Paragraph("景曜数控签署", ParagraphStyle(
        name="SignText",
        fontName=default_cn_font,  # 加粗字体
        fontSize=12,
        textColor=colors.black,
        alignment=0,
        leading=14,
        backColor=None  # 透明背景
    ))
    left_sign_content.append(sign_text)

    # 创建右侧签署区域
    right_sign_content = [
        Paragraph("客户/买方签署：", ParagraphStyle(
            name="SignText",
            fontName=default_cn_font,
            fontSize=10,
            alignment=0
        ))
    ]

    # 主签署表格
    sign_table_data = [
        [
            Table([left_sign_content], colWidths=[8 * cm]),
            Table([right_sign_content], colWidths=[8 * cm])
        ],
        [
            Table([[""]], colWidths=[8 * cm], rowHeights=[0.5 * cm]),
            Table([[""]], colWidths=[8 * cm], rowHeights=[0.5 * cm])
        ]
    ]

    sign_table = Table(sign_table_data, colWidths=[8 * cm, 8 * cm])
    sign_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, -1), default_cn_font),
        ('LINEABOVE', (0, 1), (0, 1), 0.5, colors.black),
        ('LINEABOVE', (1, 1), (1, 1), 0.5, colors.black),
    ]))

    content.append(sign_table)

    # --- 印章与文字重合的实现 ---
    if seal_image_path and os.path.exists(seal_image_path):
        seal_table = Table([
            ["", Image(  # 第一个空字符串控制左边距
                seal_image_path,
                width=3 * cm,
                height=3 * cm
            )]
        ], colWidths=[-5 * cm, 5 * cm])  # 调整第一个值控制左右位置

        content.append(Spacer(1, -2.5 * cm))  # 垂直调整
        content.append(seal_table)


    # --- 页脚信息 ---
    footer_content = Table([
        ["地址:深圳市龙岗区塘起街道大道南路328号楼", "电话:0755-85218075/17744979209"]
    ], colWidths=[10 * cm, 6 * cm])

    footer_content.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), default_cn_font),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))

    content.append(footer_content)

    # 5. 生成PDF文件
    doc.build(content)
    returnPath = settings.url_ROOT + '/media/quotation/'+ f'{companyName}' + '/' + fileName +'.pdf'
    return returnPath


# 使用示例
# if __name__ == "__main__":
#     # output_path = os.path.join(os.path.expanduser("~"), "Desktop", "运丰模具报价单.pdf")
#     output_path = settings.STATIC_ROOT + '/quotation'
#     seal_path = f"{settings.MEDIA_ROOT}\project_images\companyPatton.png"  # 替换为您的印章路径
#     fileName = "景耀有限公司"
#     generate_quotation(fileName = fileName)
#     print(f"报价单已生成")
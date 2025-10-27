import pandas as pd
from datetime import timedelta, datetime, time
import os

def clean_and_calculate_attendance(file_path, duplicate_threshold_minutes=5):
    """
    清理考勤数据，去除重复打卡记录，并计算每日工时。
    精细化判断工作人员在哪个预设时间点没有打卡，并只记录这些未打卡的时间点。

    参数:
    file_path (str): 考勤CSV文件的路径。
    duplicate_threshold_minutes (int): 定义重复打卡的分钟数阈值。
                                       例如，5分钟内连续打卡被视为重复。

    返回:
    pandas.DataFrame: 包含每位员工每日总工时及未打卡时间点的新数据表。
    """
    # --- 1. 数据加载与预处理 ---
    df = None
    file_extension = os.path.splitext(file_path)[1].lower()

    print(f"检测到文件类型为: {file_extension}")

    try:
        if file_extension in ['.xls', '.xlsx']:
            print("正在使用 pd.read_excel() 读取文件...")
            engine = 'xlrd' if file_extension == '.xls' else 'openpyxl'
            df = pd.read_excel(file_path, engine=engine, header=None)
            print("✅ Excel文件读取成功！")

        elif file_extension == '.csv':
            print("正在使用 pd.read_csv() 读取文件...")
            encodings_to_try = ['utf-8', 'utf-8-sig', 'gbk', 'gb18030', 'latin1']
            for encoding in encodings_to_try:
                try:
                    df = pd.read_csv(
                        file_path,
                        encoding=encoding,
                        engine='python',
                        sep=None,
                        header=None,
                        on_bad_lines='warn'
                    )
                    print(f"✅ CSV文件成功使用 '{encoding}' 编码读取。")
                    break
                except Exception:
                    continue
        else:
            print(f"❌ 错误: 不支持的文件类型 '{file_extension}'。请提供 .xls, .xlsx, 或 .csv 文件。")
            return pd.DataFrame()

    except Exception as e:
        print(f"❌ 致命错误: 无法读取文件 '{file_path}'。错误信息: {e}")
        return pd.DataFrame()

    if df is None or df.empty:
        print("❌ 错误: 读取文件后数据为空。请检查文件内容是否正确。")
        return pd.DataFrame()

    if df.shape[1] < 13:
        print(f"❌ 错误: 文件 '{file_path}' 的列数不足。预期至少13列（组织名称, 员工ID, 姓名, 日期, 星期, time1...time8），但只有 {df.shape[1]} 列。")
        return pd.DataFrame()

    new_columns = [
        'org_name', 'employee_id', 'name', 'date', 'weekday',
        'time1', 'time2', 'time3', 'time4', 'time5', 'time6', 'time7', 'time8'
    ]
    df.columns = new_columns

    df['employee_id'] = df['employee_id'].astype(str).str.strip()
    df['name'] = df['name'].astype(str).str.strip()


    # --- 2. 数据格式转换 (宽表变长表) ---
    id_vars = ['employee_id', 'name', 'date']
    value_vars = [f'time{i}' for i in range(1, 9) if f'time{i}' in df.columns]

    if not value_vars:
        print("❌ 错误: 未找到任何时间打卡列 (time1-time8)。请检查文件结构。")
        return pd.DataFrame()

    df_long = pd.melt(df, id_vars=id_vars, value_vars=value_vars, value_name='time_str')

    df_long['time_str'] = df_long['time_str'].astype(str).str.strip()
    df_long['datetime'] = pd.to_datetime(df_long['date'].astype(str) + ' ' + df_long['time_str'], errors='coerce')

    # --- 标记有效的打卡记录 ---
    df_long['valid_punch'] = ~df_long['datetime'].isna()
    # df_long['valid_punch'] = True
    df_long = df_long.sort_values(by=['employee_id', 'datetime']).reset_index(drop=True)


    # --- 3. 去除重复打卡记录 (仅针对有效打卡) ---
    df_long['time_diff'] = df_long.groupby('employee_id')['datetime'].diff()

    threshold = timedelta(minutes=duplicate_threshold_minutes)

    df_cleaned = df_long[(df_long['valid_punch']) &
                         ((df_long['time_diff'].isnull()) | (df_long['time_diff'] > threshold))].copy()

    # --- 4. 计算每日工作时长并精细判断未打卡时间点 ---
    daily_report_rows = []

    # 定义标准打卡时间点及其描述性名称
    expected_punch_times_map = {
        time(8, 0): "上午上班(8:00)",
        time(12, 0): "上午下班(12:00)",
        time(13, 30): "下午上班(13:30)",
        time(17, 30): "下午下班(17:30)",
        time(18, 0): "晚班开始(18:00)",
        # time(21, 0): "晚班结束(21:00)"
    }
    expected_times_sorted = sorted(expected_punch_times_map.keys())


    # 获取原始数据中所有唯一的员工ID、姓名和日期组合
    all_employee_dates = df[['employee_id', 'name', 'date']].drop_duplicates().copy()


    for _, row in all_employee_dates.iterrows():
        employee_id = row['employee_id']
        name = row['name']
        date = row['date']

        group_punches_df = df_cleaned[
            (df_cleaned['employee_id'] == employee_id) &
            (df_cleaned['date'] == date)
        ]
        actual_punches = sorted(group_punches_df['datetime'].tolist())
        # actual_punches = group_punches_df['datetime'].tolist()
        total_duration = timedelta(0)
        overtime_duration = timedelta(0)
        standard_workday_duration = timedelta(hours=8)
        missing_punch_points = [] # 用于记录缺失的打卡点

        # --- 计算总工时 ---
        punches_for_duration = actual_punches[:]
        if len(punches_for_duration) % 2 != 0:
            punches_for_duration = punches_for_duration[:-1]

        for i in range(0, len(punches_for_duration), 2):
            if i + 1 < len(punches_for_duration):
                punch_in = punches_for_duration[i]
                punch_out = punches_for_duration[i + 1]
                duration = punch_out - punch_in
                total_duration += duration
        # --- 计算加班时长 ---
        overtime_duration = total_duration - standard_workday_duration
        # --- 判断缺失打卡点 ---
        if not actual_punches or total_duration == timedelta(0) or len(actual_punches) < 2:
            # 如果当天没有任何有效打卡记录，则直接写未上岗
            missing_punch_points = ['未上岗']
        else:
            tolerance = timedelta(minutes=30) # 容忍时间窗

            for expected_time in expected_times_sorted:
                try:
                    full_expected_datetime = datetime.combine(pd.to_datetime(date).date(), expected_time)
                except ValueError:
                    continue

                matched = False
                for actual_punch in actual_punches:
                    if full_expected_datetime - tolerance <= actual_punch <= full_expected_datetime + tolerance:
                        matched = True
                        break

                if not matched:
                    missing_punch_points.append(expected_punch_times_map[expected_time])

        # 将缺失打卡点列表转换为易读的字符串
        # 关键修改：如果 missing_punch_points 为空，则字符串也为空，而不是显示"无"
        missing_punches_str = ", ".join(missing_punch_points)


        daily_report_rows.append({
            '员工ID': employee_id,
            '姓名': name,
            '日期': date,
            '总工时': total_duration,
            '加班时间': overtime_duration,  # 暂时不计算加班时间
            '未打卡时间点': missing_punches_str # 直接使用构建好的字符串
        })

    if not daily_report_rows:
        print("未找到任何工时记录。")
        return pd.DataFrame()

    result_df = pd.DataFrame(daily_report_rows)

    def format_duration_and_status(td):
        # if pd.isnull(td) or td.total_seconds() <= 0:
        #     return "未上岗"
        # else:
        if pd.isnull(td) or td.total_seconds() <= 0:
            return "未上岗"
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    result_df['总工时(时:分:秒)'] = result_df['总工时'].apply(format_duration_and_status)

    # 格式化加班时间
    # 如果加班时间为0，则显示 "无加班"
    overtimeLine = timedelta(minutes=15)  # 定义加班时间的阈值
    def format_overtime_duration(td):
        if pd.isnull(td) or td <= overtimeLine:
            return "无加班"
        else:
            total_seconds = int(td.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}"

    result_df['加班时间(时:分:秒)'] = result_df['加班时间'].apply(format_overtime_duration)
    result_df['星期'] = df['weekday']

    return result_df[['员工ID', '姓名', '日期', '星期', '总工时(时:分:秒)', '加班时间(时:分:秒)', '未打卡时间点']]


# # --- 执行脚本 ---
# file_path = 'File250705182422.xlsx' # 请替换为你的实际文件路径
# final_report = clean_and_calculate_attendance(file_path, duplicate_threshold_minutes=5)
#
# # --- 显示结果 ---
# print("\n每日工时计算，加班及未打卡点报告:")
# print(final_report.to_string())
#
# # --- 保存结果 ---
# try:
#     final_report.to_excel("每日工时、加班及未打卡点报告副本.xlsx", index=False)
#     print("\n✅ 每日工时及未打卡点报告已成功保存到 '每日工时、加班及未打卡点报告.xlsx'。")
# except Exception as e:
#     print(f"\n❌ 错误: 无法保存报告到 Excel 文件。错误信息: {e}")

# import pandas as pd
# from datetime import timedelta, datetime, time
# import os
#
#
# def clean_and_calculate_attendance(file_path, duplicate_threshold_minutes=5):
#     """
#     清理考勤数据，去除重复打卡记录，并计算每日工时。
#     将容忍范围内的打卡时间调整为规定的打卡时间，并计算加班时长。
#
#     参数:
#     file_path (str): 考勤CSV文件的路径。
#     duplicate_threshold_minutes (int): 定义重复打卡的分钟数阈值。
#                                        例如，5分钟内连续打卡被视为重复。
#
#     返回:
#     pandas.DataFrame: 包含每位员工每日总工时及未打卡时间点的新数据表。
#     """
#     # --- 1. 数据加载与预处理 ---
#     df = None
#     file_extension = os.path.splitext(file_path)[1].lower()
#
#     print(f"检测到文件类型为: {file_extension}")
#
#     try:
#         if file_extension in ['.xls', '.xlsx']:
#             print("正在使用 pd.read_excel() 读取文件...")
#             engine = 'xlrd' if file_extension == '.xls' else 'openpyxl'
#             df = pd.read_excel(file_path, engine=engine, header=None)
#             print("✅ Excel文件读取成功！")
#
#         elif file_extension == '.csv':
#             print("正在使用 pd.read_csv() 读取文件...")
#             encodings_to_try = ['utf-8', 'utf-8-sig', 'gbk', 'gb18030', 'latin1']
#             for encoding in encodings_to_try:
#                 try:
#                     df = pd.read_csv(
#                         file_path,
#                         encoding=encoding,
#                         engine='python',
#                         sep=None,
#                         header=None,
#                         on_bad_lines='warn'
#                     )
#                     print(f"✅ CSV文件成功使用 '{encoding}' 编码读取。")
#                     break
#                 except Exception:
#                     continue
#         else:
#             print(f"❌ 错误: 不支持的文件类型 '{file_extension}'。请提供 .xls, .xlsx, 或 .csv 文件。")
#             return pd.DataFrame()
#
#     except Exception as e:
#         print(f"❌ 致命错误: 无法读取文件 '{file_path}'。错误信息: {e}")
#         return pd.DataFrame()
#
#     if df is None or df.empty:
#         print("❌ 错误: 读取文件后数据为空。请检查文件内容是否正确。")
#         return pd.DataFrame()
#
#     if df.shape[1] < 13:
#         print(
#             f"❌ 错误: 文件 '{file_path}' 的列数不足。预期至少13列（组织名称, 员工ID, 姓名, 日期, 星期, time1...time8），但只有 {df.shape[1]} 列。")
#         return pd.DataFrame()
#
#     new_columns = [
#         'org_name', 'employee_id', 'name', 'date', 'weekday',
#         'time1', 'time2', 'time3', 'time4', 'time5', 'time6', 'time7', 'time8'
#     ]
#     df.columns = new_columns
#
#     df['employee_id'] = df['employee_id'].astype(str).str.strip()
#     df['name'] = df['name'].astype(str).str.strip()
#
#     # --- 2. 数据格式转换 (宽表变长表) ---
#     id_vars = ['employee_id', 'name', 'date']
#     value_vars = [f'time{i}' for i in range(1, 9) if f'time{i}' in df.columns]
#
#     if not value_vars:
#         print("❌ 错误: 未找到任何时间打卡列 (time1-time8)。请检查文件结构。")
#         return pd.DataFrame()
#
#     df_long = pd.melt(df, id_vars=id_vars, value_vars=value_vars, value_name='time_str')
#
#     df_long['time_str'] = df_long['time_str'].astype(str).str.strip()
#     df_long['datetime'] = pd.to_datetime(df_long['date'].astype(str) + ' ' + df_long['time_str'], errors='coerce')
#
#     # --- 标记有效的打卡记录 ---
#     df_long['valid_punch'] = ~df_long['datetime'].isna()
#     df_long = df_long.sort_values(by=['employee_id', 'datetime']).reset_index(drop=True)
#
#     # --- 3. 去除重复打卡记录 (仅针对有效打卡) ---
#     df_long['time_diff'] = df_long.groupby('employee_id')['datetime'].diff()
#
#     threshold = timedelta(minutes=duplicate_threshold_minutes)
#
#     df_cleaned = df_long[(df_long['valid_punch']) &
#                          ((df_long['time_diff'].isnull()) | (df_long['time_diff'] > threshold))].copy()
#
#     # --- 4. 定义标准打卡时间点及其描述性名称 ---
#     expected_punch_times_map = {
#         time(8, 0): "上午上班(8:00)",
#         time(12, 0): "上午下班(12:00)",
#         time(13, 30): "下午上班(13:30)",
#         time(17, 30): "下午下班(17:30)",
#         time(18, 0): "晚班开始(18:00)",
#         time(21, 0): "晚班结束(21:00)"
#     }
#     expected_times_sorted = sorted(expected_punch_times_map.keys())
#
#     # --- 5. 将容忍范围内的打卡时间调整为规定时间 ---
#     tolerance = timedelta(minutes=30)  # 容忍时间窗
#
#     def adjust_to_expected_time(dt):
#         if pd.isnull(dt):
#             return dt
#
#         dt_time = dt.time()
#         dt_date = dt.date()
#
#         # 寻找最接近的预期时间点
#         closest_time = None
#         min_diff = float('inf')
#
#         for expected_time in expected_times_sorted:
#             expected_dt = datetime.combine(dt_date, expected_time)
#             time_diff = abs((dt - expected_dt).total_seconds())
#
#             if time_diff < min_diff and time_diff <= tolerance.total_seconds():
#                 min_diff = time_diff
#                 closest_time = expected_time
#
#         # 如果找到在容忍范围内的预期时间，则调整为该时间
#         if closest_time is not None:
#             return datetime.combine(dt_date, closest_time)
#         else:
#             return dt
#
#     # 应用调整函数
#     df_cleaned['adjusted_datetime'] = df_cleaned['datetime'].apply(adjust_to_expected_time)
#
#     # 去除调整后可能出现的重复记录
#     df_cleaned = df_cleaned.sort_values(by=['employee_id', 'adjusted_datetime'])
#     df_cleaned['adjusted_time_diff'] = df_cleaned.groupby('employee_id')['adjusted_datetime'].diff()
#     df_final = df_cleaned[(df_cleaned['adjusted_time_diff'].isnull()) |
#                           (df_cleaned['adjusted_time_diff'] > threshold)].copy()
#
#     # --- 6. 计算每日工作时长并精细判断未打卡时间点 ---
#     daily_report_rows = []
#
#     # 获取原始数据中所有唯一的员工ID、姓名和日期组合
#     all_employee_dates = df[['employee_id', 'name', 'date']].drop_duplicates().copy()
#
#     for _, row in all_employee_dates.iterrows():
#         employee_id = row['employee_id']
#         name = row['name']
#         date = row['date']
#
#         group_punches_df = df_final[
#             (df_final['employee_id'] == employee_id) &
#             (df_final['date'] == date)
#             ]
#         actual_punches = sorted(group_punches_df['adjusted_datetime'].tolist())
#         total_duration = timedelta(0)
#         overtime_duration = timedelta(0)
#         standard_workday_duration = timedelta(hours=8)
#         missing_punch_points = []  # 用于记录缺失的打卡点
#
#         # --- 计算总工时 ---
#         punches_for_duration = actual_punches[:]
#         if len(punches_for_duration) % 2 != 0:
#             punches_for_duration = punches_for_duration[:-1]
#
#         for i in range(0, len(punches_for_duration), 2):
#             if i + 1 < len(punches_for_duration):
#                 punch_in = punches_for_duration[i]
#                 punch_out = punches_for_duration[i + 1]
#                 duration = punch_out - punch_in
#                 total_duration += duration
#
#         # --- 计算加班时长 (晚班结束和晚班开始的时间差) ---
#         # 查找晚班开始和结束时间
#         evening_start = None
#         evening_end = None
#
#         for punch in actual_punches:
#             punch_time = punch.time()
#             if punch_time == time(18, 0):  # 晚班开始
#                 evening_start = punch
#             elif punch_time == time(21, 0):  # 晚班结束
#                 evening_end = punch
#
#         # 如果找到了晚班开始和结束时间，计算加班时长
#         if evening_start and evening_end:
#             overtime_duration = evening_end - evening_start
#         # 计算工作时间
#         worktime_duration = total_duration - overtime_duration
#         # --- 判断缺失打卡点 ---
#         if not actual_punches or total_duration == timedelta(0) or len(actual_punches) < 2:
#             # 如果当天没有任何有效打卡记录，则直接写未上岗
#             missing_punch_points = ['未上岗']
#         else:
#             # 检查每个预期时间点是否有打卡
#             for expected_time in expected_times_sorted:
#                 matched = False
#                 for actual_punch in actual_punches:
#                     if actual_punch.time() == expected_time:
#                         matched = True
#                         break
#
#                 if not matched:
#                     missing_punch_points.append(expected_punch_times_map[expected_time])
#
#         # 将缺失打卡点列表转换为易读的字符串
#         missing_punches_str = ", ".join(missing_punch_points) if missing_punch_points else ""
#
#         daily_report_rows.append({
#             '员工ID': employee_id,
#             '姓名': name,
#             '日期': date,
#             '总工时': total_duration,
#             '工作时间': worktime_duration,
#             '加班时间': overtime_duration,
#             '未打卡时间点': missing_punches_str
#         })
#
#     if not daily_report_rows:
#         print("未找到任何工时记录。")
#         return pd.DataFrame()
#
#     result_df = pd.DataFrame(daily_report_rows)
#
#     def format_duration_and_status(td):
#         if pd.isnull(td) or td.total_seconds() <= 0:
#             return "未上岗"
#         total_seconds = int(td.total_seconds())
#         hours, remainder = divmod(total_seconds, 3600)
#         minutes, seconds = divmod(remainder, 60)
#         return f"{hours:02}:{minutes:02}:{seconds:02}"
#
#     result_df['总工时'] = result_df['总工时'].apply(format_duration_and_status)
#     result_df['工作时间'] = result_df['工作时间'].apply(format_duration_and_status)
#     # 格式化加班时间
#     overtimeLine = timedelta(minutes=15)  # 定义加班时间的阈值
#
#     def format_overtime_duration(td):
#         if pd.isnull(td) or td <= overtimeLine:
#             return "无加班"
#         else:
#             total_seconds = int(td.total_seconds())
#             hours, remainder = divmod(total_seconds, 3600)
#             minutes, seconds = divmod(remainder, 60)
#             return f"{hours:02}:{minutes:02}:{seconds:02}"
#
#     result_df['加班时间'] = result_df['加班时间'].apply(format_overtime_duration)
#     result_df['星期'] = df['weekday']
#
#     return result_df[['员工ID', '姓名', '日期', '星期', '总工时', '工作时间','加班时间', '未打卡时间点']]
#

# # coding:utf-8
#
# from bs4 import BeautifulSoup
# import urllib.parse
# import urllib.request
# from urllib.parse import quote
# import string
# # 设置字体
# from sc.ZDao import getConnect
#
#
# def getChartsData(areaName,jobName):
#     # 连接数据库
#     # 操作数据库,将数据存储进去
#     db =getConnect()
#     # 使用cursor()方法获取操作游标,即操作数据库的一个对象
#     sql = ""
#     cur = db.cursor()  # 游标 操作数据表
#     sql ="select job_edu,count(*) from jobs where job_loc like '%"+areaName+"%' and job_name like '%"+jobName+"%' group by job_edu "
#     print(sql)
#     edus = [];
#     counts = [];
#     try:
#         cur.execute(sql)
#         res = cur.fetchall()  # 查到的所有的记录 是一个集合
#         for r in res:
#             edus.append(r[0]);
#             counts.append(r[1]);
#         data = {"edus": edus, "counts": counts};
#         return data;
#     except:
#         db.rollback()
#
# # 爬取数据方法
# def run():
#     jName = input("请输入城市:");
#     #jName='北京'
#     city = {'北京': '530',
#             '上海': '538',
#             '广州': '763',
#             '深圳': '765',
#             '天津': '531',
#             '武汉': '736',
#             '西安': '854',
#             '成都': '801',
#             '沈阳': '599',
#             '南京': '635',
#             '杭州': '653',
#             '苏州': '639',
#             '重庆': '551',
#             '长沙': '749',
#             '厦门': '682',
#             '南昌': '691'
#             }  # 如果还要其它城市 对着页面，查看城市编码 https://sou.zhaopin.com/?jl=691&kw=java&p=1
#     jName=city[jName]
#     aName = input("请输入岗位:");
#     #aName='java'
#     #num = 1
#     #while num <= 5:
#     url = 'https://sou.zhaopin.com/?jl='+jName+'&kw=' + aName + '&p=1'
#     # 打印实际请求的URL
#     print(f"实际请求的URL: {url}")
#     url = quote(url, safe=string.printable)
#     res = urllib.request.urlopen(url)
#     content = res.read().decode()
#     # 在获取content后添加
#     with open('debug.html', 'w', encoding='utf-8') as f:
#         f.write(content)
#     print("已保存网页到debug.html")
#
#     # 整个页面的数据
#     # 创建一个Beautifulsoup对象
#     soup = BeautifulSoup(content, 'lxml')
#     # 旧选择器（可能失效）
#     # jobList = soup.select(".joblist-box__item")
#
#     # 尝试这些新选择器
#     jobList = soup.select(".joblist__item, .job-card-wrapper, [class*='job']")
#     print(f"找到 {len(jobList)} 个职位")  # 调试用
#
#     # 创建一个list存放job相关信息的字典
#     job_list = []
#     for job in jobList:
#         job_dic = {}
#         # 每一个job都是一个工作的信息的div
#         # 岗位名称
#         job_name = job.select('.jobinfo__name')[0].get_text()
#         #print(job_name)
#         # 公司名称
#         company_name = job.select('.companyinfo__name')[0].get_text()
#         #print(company_name)
#         # 工资
#         job_salary = job.select('.jobinfo__salary')[0].get_text()
#         job_salary = job_salary.strip().replace(' ', '').replace('\n', '')
#         str2 = job_salary  # 1万-2万，取的是1万
#
#         if '天' in str2:
#             str2 = int(str2.split("-")[0]) * 30
#         elif ('千' in str2):
#             str2 = (int(str2.split('千')[0]) * 1000)
#         elif ('万' in str2):  # 含万
#             str2 = float(str2.split("万")[0]) * 10000
#         else:
#             str2 = 5000
#         print(str2)
#         # 获取工作地点、经验要求、学历要求
#         lis = job.select('.jobinfo__other-info-item')
#         job_loc = lis[0].get_text()
#         job_exp = lis[1].get_text()
#         job_edu = lis[2].get_text()
#         job_dic['job_name'] = job_name
#         job_dic['company_name'] = company_name
#         job_dic['job_salary'] = str2
#         job_loc = job_loc.split("-")[0]
#         job_dic['job_loc'] = job_loc
#         job_dic['job_exp'] = job_exp
#         job_dic['job_edu'] = job_edu
#         job_list.append(job_dic)
#
#     # 打印爬取到的数据
#     import json
#     print("\n爬取到的职位数据：")
#     for job in job_list:
#         print(json.dumps(job, ensure_ascii=False, indent=2))
#
#     # 操作数据库,将数据存储进去
#     db = getConnect();
#     # 使用cursor()方法获取操作游标,即操作数据库的一个对象
#     cursor = db.cursor()
#     # 使用格式化输出的方式将变量传进去
#     for i in job_list:
#         sql = "INSERT INTO jobs(jid,job_name,company_name,job_sal,job_loc,job_exp,job_edu) VALUES(null,'%s','%s','%s','%s','%s','%s')" % (
#             i["job_name"], i["company_name"], i["job_salary"], i["job_loc"], i["job_exp"], i["job_edu"])
#         # 执行多条插入语句使用cursor.executemany(sql,list)
#         # 这个list是由每条数据组成的元组
#         # 执行语句
#         try:
#             cursor.execute(sql)
#             # 更新操作需要提交
#             db.commit()
#         except Exception as e:
#             print(e)
#             print('插入数据失败!')
#             # 如果有异常需要回滚
#             db.rollback()
#     # 关闭游标
#     cursor.close()
#     # 关闭数据库连接
#     db.close()
#     print("爬取数据成功")
#
# run();


# coding:utf-8
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import quote
import string
import json
import re
from sc.ZDao import getConnect


def clean_company_name(name):
    """清洗公司名称"""
    return re.split(r'·|HR|招聘|高回复率|立即沟通', name)[0].strip()


def parse_salary(salary_text):
    """解析复杂薪资文本为数字（取范围平均值）"""
    # 清洗薪资文本
    clean_text = re.sub(r'[^\d\-万千/.]+', '', salary_text.strip())

    # 处理无意义数据
    if not clean_text:
        return 0.0

    # 分割薪资范围
    if '-' in clean_text:
        parts = re.split(r'-|～|~', clean_text)
    else:
        parts = [clean_text]

    values = []
    for part in parts:
        # 处理单位转换
        if '千' in part:
            num = re.sub(r'千', '', part)
            values.append(float(num) * 1000)
        elif '万' in part:
            num = re.sub(r'万', '', part)
            values.append(float(num) * 10000)
        elif '元/天' in part:
            num = re.sub(r'元/天', '', part)
            values.append(float(num) * 22 * 30)  # 按22天/月估算
        else:
            try:
                values.append(float(part))
            except:
                continue

    # 计算有效值的平均值
    valid_values = [v for v in values if v > 0]
    if not valid_values:
        return 0.0
    return round(sum(valid_values) / len(valid_values), 2)


def run():
    # 输入处理
    jName = input("请输入城市:")
    city = {'北京': '530', '上海': '538', '广州': '763', '深圳': '765', '南昌': '691'}
    jName = city.get(jName, '691')  # 默认南昌

    aName = input("请输入岗位:")

    # 构造请求URL
    base_url = f'https://sou.zhaopin.com/?jl={jName}&kw={aName}&p=1'
    encoded_url = quote(base_url, safe=string.printable)

    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.zhaopin.com/'
    }

    try:
        # 发送请求
        req = urllib.request.Request(encoded_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')

        # 保存网页用于调试
        with open('zhaopin_debug.html', 'w', encoding='utf-8') as f:
            f.write(content)

        # 解析HTML
        soup = BeautifulSoup(content, 'lxml')
        print(f"页面标题: {soup.title.string if soup.title else '无标题'}")

        # 获取职位列表
        job_items = soup.select(".joblist-box__item, .job-item, [class*='job']")
        print(f"找到 {len(job_items)} 个职位")

        job_list = []
        seen_jobs = set()

        for job in job_items:
            try:
                # 解析基础信息
                job_name = job.select_one('.jobinfo__name, .job-title').get_text(strip=True)
                company = job.select_one('.companyinfo__name, .company-name').get_text(strip=True)
                company_name = clean_company_name(company)
                salary_text = job.select_one('.jobinfo__salary, .salary').get_text(strip=True)

                # 生成唯一标识去重
                job_key = f"{job_name}|{company_name}|{salary_text}"
                if job_key in seen_jobs:
                    continue
                seen_jobs.add(job_key)

                # 解析其他字段
                job_loc = job.select_one('.jobinfo__other-info-item, .job-location').get_text(strip=True)
                job_loc = job_loc.split('-')[0].strip()

                # 处理经验要求和学历
                other_info = job.select('.jobinfo__other-info-item')
                job_exp = other_info[1].get_text(strip=True) if len(other_info) > 1 else '不限'
                job_edu = other_info[2].get_text(strip=True) if len(other_info) > 2 else '不限'

                # 解析薪资
                salary = parse_salary(salary_text)

                job_list.append({
                    'job_name': job_name,
                    'company_name': company_name,
                    'job_salary': salary,
                    'job_loc': job_loc,
                    'job_exp': job_exp,
                    'job_edu': job_edu
                })
            except Exception as e:
                print(f"解析职位时出错: {str(e)}")
                continue

        # 打印清洗后的数据
        print("\n=== 清洗后的职位数据 ===")
        print(json.dumps(job_list, ensure_ascii=False, indent=2))

        # 数据库操作
        if job_list:
            db = getConnect()
            cursor = db.cursor()

            # 检查表结构并动态适配
            cursor.execute("SHOW COLUMNS FROM jobs LIKE 'jid'")
            has_jid = cursor.fetchone()

            # 构建插入语句
            if has_jid:
                sql = """INSERT INTO jobs 
                        (jid, job_name, company_name, job_sal, job_loc, job_exp, job_edu)
                        VALUES (NULL, %s, %s, %s, %s, %s, %s)"""
            else:
                sql = """INSERT INTO jobs 
                        (job_name, company_name, job_sal, job_loc, job_exp, job_edu)
                        VALUES (%s, %s, %s, %s, %s, %s)"""

            # 批量插入数据
            data = [
                (
                    job['job_name'],
                    job['company_name'],
                    job['job_salary'],
                    job['job_loc'],
                    job['job_exp'],
                    job['job_edu']
                )
                for job in job_list
            ]

            try:
                cursor.executemany(sql, data)
                db.commit()
                print(f"\n✅ 成功插入 {len(job_list)} 条数据")
            except Exception as e:
                print(f"数据库插入失败: {str(e)}")
                db.rollback()
            finally:
                cursor.close()
                db.close()
        else:
            print("⚠️ 没有可插入的数据")

    except Exception as e:
        print(f"请求出错: {str(e)}")


if __name__ == '__main__':
    run()
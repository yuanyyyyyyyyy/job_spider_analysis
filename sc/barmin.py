# from pyecharts.charts import Bar
# from pyecharts import options as opts
#
# from sc.ZDao import getConnect
#
#
# def initData():
#     # 连接数据库
#     # 操作数据库,将数据存储进去
#     db = getConnect();
#     # 使用cursor()方法获取操作游标,即操作数据库的一个对象
#     sql = ""
#     cur = db.cursor()  # 游标 操作数据表
#     #显示最新的8个城市的薪水情况
#     sql ="select job_name,min(job_sal+0),job_loc from jobs group by job_loc order by jid desc limit 8";
#     print(sql)
#
#     sal = [];
#     ci = [];
#     try:
#         cur.execute(sql)
#         res = cur.fetchall()  # 查到的所有的记录 是一个集合
#         for r in res:
#             sal.append(r[1]);
#             ci.append(r[2]);
#         print(sal)
#         print(ci)
#
#     except:
#         db.rollback()
#
#     bar = Bar()
#     bar.add_xaxis(ci)
#     bar.add_yaxis("月薪水/元", sal)
#     bar.set_global_opts(title_opts=opts.TitleOpts(title="各城市-最低薪水图", subtitle="单位/元"))
#
#     bar.render("barmin.html")
# initData();

from pyecharts.charts import Bar
from pyecharts import options as opts
from sc.ZDao import getConnect

def initData():
    # 获取数据库连接
    db = getConnect()
    cur = db.cursor()

    # 优化后的SQL查询
    sql = """
    SELECT 
        job_loc AS 城市,
        MIN(job_sal) AS 最低薪资 
    FROM jobs
    WHERE job_sal > 0  -- 过滤无效薪资数据
    GROUP BY job_loc
    HAVING 最低薪资 > 0  -- 确保有有效数据
    ORDER BY 最低薪资 ASC  -- 按最低薪资升序排列
    LIMIT 8
    """

    cities = []
    salaries = []

    try:
        print(f"执行SQL:\n{sql}")
        cur.execute(sql)
        results = cur.fetchall()

        if not results:
            print("⚠️ 没有查询到有效数据，请检查：")
            print("1. 是否已运行爬虫并成功插入数据")
            print("2. 数据库jobs表中是否存在有效薪资数据")
            return

        # 处理查询结果
        for city, salary in results:
            cities.append(city)
            salaries.append(salary)

        print("城市列表:", cities)
        print("最低薪资:", salaries)

        # 创建柱状图
        bar = (
            Bar(init_opts=opts.InitOpts(
                width="1400px",
                height="700px",
                theme="light"
            ))
            .add_xaxis(cities)
            .add_yaxis(
                series_name="最低月薪",
                y_axis=salaries,
                color="#FF6B6B",  # 红色系突出最低薪资
                label_opts=opts.LabelOpts(
                    position="top",
                    formatter="{c} 元",
                    font_size=12,
                    color="#FF4444"
                ),
                bar_max_width=60
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="各城市最低薪资TOP8",
                    subtitle="数据来源：智联招聘实时采集数据",
                    title_textstyle_opts=opts.TextStyleOpts(
                        font_size=22,
                        color="#2c3e50"
                    )
                ),
                xaxis_opts=opts.AxisOpts(
                    name="城市",
                    axislabel_opts=opts.LabelOpts(
                        rotate=25,
                        margin=8,
                        font_size=12
                    ),
                    splitline_opts=opts.SplitLineOpts(is_show=False)
                ),
                yaxis_opts=opts.AxisOpts(
                    name="最低薪资（元）",
                    min_=1000,  # 设置Y轴起点
                    axislabel_opts=opts.LabelOpts(
                        formatter="{value} 元",
                        font_size=12
                    ),
                    splitline_opts=opts.SplitLineOpts(
                        is_show=True,
                        linestyle_opts=opts.LineStyleOpts(
                            type_="dotted",
                            opacity=0.6
                        )
                    )
                ),
                tooltip_opts=opts.TooltipOpts(
                    trigger="item",
                    formatter="{b}<br/>最低薪资：{c} 元"
                ),
                datazoom_opts=[opts.DataZoomOpts()],
                toolbox_opts=opts.ToolboxOpts(
                    is_show=True,
                    pos_left="85%",
                    feature={
                        "saveAsImage": {"pixel_ratio": 2},
                        "restore": {}
                    }
                )
            )
        )

        # 渲染图表
        bar.render("barmin.html")
        print("✅ 最低薪资图表已生成到 barmin.html")

    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        db.rollback()
    finally:
        cur.close()
        db.close()

if __name__ == '__main__':
    initData()
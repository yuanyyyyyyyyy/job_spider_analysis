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
#     #显示最新的五个城市的薪水情况
#     sql ="select job_name,avg(job_sal),job_loc from jobs group by job_loc order by jid desc limit 8";
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
#     bar.set_global_opts(title_opts=opts.TitleOpts(title="各城市-平均薪水图", subtitle="单位/元"))
#
#     bar.render("baravg.html")
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
        ROUND(AVG(job_sal), 2) AS 平均薪资 
    FROM jobs
    WHERE job_sal > 0  -- 过滤无效薪资数据
    GROUP BY job_loc
    HAVING 平均薪资 > 0  -- 确保有有效数据
    ORDER BY 平均薪资 DESC
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
            print("2. 数据库jobs表中是否存在job_sal字段")
            return

        # 处理查询结果
        for city, salary in results:
            cities.append(city)
            salaries.append(salary)

        print("城市列表:", cities)
        print("平均薪资:", salaries)

        # 生成动态颜色
        colors = [
            "#5470c6", "#91cc75", "#fac858",
            "#ee6666", "#73c0de", "#3ba272",
            "#fc8452", "#9a60b4"
        ]

        # 创建柱状图
        bar = (
            Bar(init_opts=opts.InitOpts(
                width="1600px",
                height="800px",
                theme="white",  # 使用白色主题
                bg_color="rgba(255, 255, 255, 0.8)"
            ))
            .add_xaxis(cities)
            .add_yaxis(
                series_name="平均月薪",
                y_axis=salaries,
                itemstyle_opts=opts.ItemStyleOpts(color=colors[0]),
                label_opts=opts.LabelOpts(
                    position="top",
                    formatter="{c} 元",
                    font_size=14,
                    color="#333"
                ),
                bar_max_width=80  # 控制柱宽
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="各城市平均薪资TOP8",
                    subtitle="数据来源：智联招聘实时数据",
                    title_textstyle_opts=opts.TextStyleOpts(
                        font_size=24,
                        color="#2c343c"
                    ),
                    subtitle_textstyle_opts=opts.TextStyleOpts(
                        font_size=16,
                        color="#666"
                    )
                ),
                xaxis_opts=opts.AxisOpts(
                    name="城市",
                    axislabel_opts=opts.LabelOpts(
                        rotate=30,  # 旋转标签防止重叠
                        font_size=12,
                        margin=10  # 标签间距
                    ),
                    splitline_opts=opts.SplitLineOpts(is_show=False)
                ),
                yaxis_opts=opts.AxisOpts(
                    name="平均薪资（元）",
                    axislabel_opts=opts.LabelOpts(
                        formatter="{value} 元",
                        font_size=12
                    ),
                    splitline_opts=opts.SplitLineOpts(
                        is_show=True,
                        linestyle_opts=opts.LineStyleOpts(
                            type_="dashed",
                            opacity=0.5
                        )
                    )
                ),
                tooltip_opts=opts.TooltipOpts(
                    trigger="axis",
                    axis_pointer_type="shadow",
                    formatter="{b}<br/>平均薪资：{c} 元"
                ),
                datazoom_opts=[opts.DataZoomOpts()],  # 添加横向滚动
                toolbox_opts=opts.ToolboxOpts(
                    is_show=True,
                    feature={
                        "saveAsImage": {},
                        "dataZoom": {},
                        "restore": {}
                    }
                )
            )
        )

        # 渲染图表
        bar.render("baravg.html")
        print("✅ 图表已成功生成到 baravg.html")
        print("请用浏览器打开查看效果")

    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        db.rollback()
    finally:
        cur.close()
        db.close()

if __name__ == '__main__':
    initData()
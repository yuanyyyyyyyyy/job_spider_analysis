
from pyecharts import options as opts
from pyecharts.charts import Pie

def draw_pie_chart():
    pie = Pie()

    # 步骤3：添加数据和配置项
    data_pair = [["类别1", 30], ["类别2", 40], ["类别3", 50]]
    pie.add("类别", data_pair)
    pie.set_global_opts(title_opts=opts.TitleOpts(title="饼图示例"))

    # 步骤4：渲染图表
    pie.render("pie2.html")


if __name__ == "__main__":
    draw_pie_chart()
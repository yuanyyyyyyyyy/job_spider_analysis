from pyecharts.charts import Bar
from pyecharts import options as opts

bar = Bar()
bar.add_xaxis(["数学", "物理", "化学", "英语"])
bar.add_yaxis("成绩", [70, 85, 95, 64])
bar.set_global_opts(title_opts=opts.TitleOpts(title="柱状图", subtitle="分数"))
bar.render("bar1.html")
from pyecharts.charts import Bar
from pyecharts import options as opts

from sc.ZDao import getConnect
from pyecharts import options as opts
from pyecharts.charts import Pie

def initData():
    # 连接数据库
    # 操作数据库,将数据存储进去
    db = getConnect();
    # 使用cursor()方法获取操作游标,即操作数据库的一个对象
    sql = ""
    cur = db.cursor()  # 游标 操作数据表
    #显示最新的五个城市的薪水情况
    sql ="select job_loc,count(jid) from jobs group by job_loc order by jid desc limit 8";
    print(sql)

    sal = [];

    dict = {}
    zz=[]
    z=[]
    try:
        cur.execute(sql)
        res = cur.fetchall()  # 查到的所有的记录 是一个集合,因为饼图须要传入一个二维数组
        pie = Pie()
        # 步骤3：添加数据和配置项
        #data_pair = [("类别1", 30), ("类别2", 40), ("类别3", 50), ("类别4", 60)]
        print(res)
        data_pair = res;
        pie.add("单位/个", data_pair)
        pie.set_global_opts(title_opts=opts.TitleOpts(title="各城市-岗位数量图"))
        # 步骤4：渲染图表
        pie.render("pienum.html")
    except:
        db.rollback()


initData();
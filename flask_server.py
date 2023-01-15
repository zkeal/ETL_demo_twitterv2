from flask import Flask
from flask import render_template
from pyecharts import options as opts
from pyecharts.charts import Bar,Pie
import json
from comment_detector import detector
from threading import Thread

app = Flask(__name__, static_folder="templates")


def bar_base() -> Bar:
    meta_data = load_meta('meta.json')
    if len(meta_data) == 0:
        return None
    c = (
        Bar()
            .add_xaxis(list(meta_data.keys()))
            .add_yaxis("Twitter", list(meta_data.values()))
            .set_global_opts(title_opts=opts.TitleOpts(title="Twitter counting", subtitle="Bar Chart"))
    )
    return c


def pie_base() -> Pie:
    meta_data = load_meta('meta.json')
    if len(meta_data) == 0:
        return None
    c = (
        Pie()
            .add(series_name="percentage",data_pair=list(meta_data.items()),radius=["40%", "60%"],rosetype="radius")
    )
    return c


def load_meta(path):
    try:
        with open(path, 'r') as load_f:
            load_dict = json.load(load_f)
        return load_dict
    except:
        return dict()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/barChart")
def get_bar_chart():
    try:
        c = bar_base()
        return c.dump_options_with_quotes()
    except:
        return {}


@app.route("/pieChart")
def get_pie_chart():
    try:
        c = pie_base()
        return c.dump_options_with_quotes()
    except:
        return {}


def main():
    stream_detector = detector()
    t1 = Thread(target=app.run)
    t2 = Thread(target=stream_detector.detect_streaming)
    t1.start()
    t2.start()

if __name__ == "__main__":
    main()
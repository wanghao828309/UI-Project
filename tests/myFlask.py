#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:wanghao
# datetime:2019/10/16 11:20


# from flask import Flask,render_template
#
# app = Flask(__name__,template_folder=r'C:\Users\ws\Desktop\css3-bar-chart')
#
# @app.route('/index/')
# def index():
# 	context = {
# 		'username':'xxx',
# 		'age':18,
# 		'height':180,
# 	}
# 	return render_template('3.html',**context)


import jinja2

versions = [u'9.2.7.13', u'9.2.7.12', u'9.2.7.11', u'9.2.7.10', u'9.2.7.9']

context ={'export_GPU': {'AMD_R9': {u'9.2.7.9': u'19.73', u'9.2.7.11': u'20.81', u'9.2.7.10': u'19.86', u'9.2.7.13': u'20.76', u'9.2.7.12': u'20.78'}, 'NVIDIA_970': {u'9.2.7.9': u'31.65', u'9.2.7.11': u'31.54', u'9.2.7.10': u'53.56', u'9.2.7.13': u'32.09', u'9.2.7.12': u'32.54'}, 'NVIDIA_1050': {u'9.2.7.9': u'39.24', u'9.2.7.11': u'36.96', u'9.2.7.10': u'35.51', u'9.2.7.13': u'35.2', u'9.2.7.12': u'34.98'}, 'Intel_5500': {u'9.2.7.9': u'64.18', u'9.2.7.11': u'56.93', u'9.2.7.10': u'56.11', u'9.2.7.13': u'57.52', u'9.2.7.12': u'57.52'}}, 'export_CPU': {'AMD_R9': {u'9.2.7.9': u'21.69', u'9.2.7.11': u'23.82', u'9.2.7.10': u'21.84', u'9.2.7.13': u'22.98', u'9.2.7.12': u'25.08'}, 'NVIDIA_970': {u'9.2.7.9': u'37.14', u'9.2.7.11': u'38.2', u'9.2.7.10': u'50.55', u'9.2.7.13': u'38.5', u'9.2.7.12': u'36.57'}, 'NVIDIA_1050': {u'9.2.7.9': u'42.75', u'9.2.7.11': u'39.6', u'9.2.7.10': u'38.08', u'9.2.7.13': u'38.06', u'9.2.7.12': u'38.88'}, 'Intel_5500': {u'9.2.7.9': u'63.16', u'9.2.7.11': u'62.11', u'9.2.7.10': u'60.64', u'9.2.7.13': u'62.17', u'9.2.7.12': u'62.27'}}, 'open_filmora': {'AMD_R9': {u'9.2.7.9': u'33.05', u'9.2.7.11': u'17.69', u'9.2.7.10': u'21.07', u'9.2.7.13': u'24.71', u'9.2.7.12': u'40.73'}, 'NVIDIA_970': {u'9.2.7.9': u'29.16', u'9.2.7.11': u'35.88', u'9.2.7.10': u'41.12', u'9.2.7.13': u'41.16', u'9.2.7.12': u'39.95'}, 'NVIDIA_1050': {u'9.2.7.9': u'51.86', u'9.2.7.11': u'4.78', u'9.2.7.10': u'24.92', u'9.2.7.13': u'42.85', u'9.2.7.12': u'38.17'}, 'Intel_5500': {u'9.2.7.9': u'81.02', u'9.2.7.11': u'3.3', u'9.2.7.10': u'24.56', u'9.2.7.12': u'35.34'}}}




RENDER_RULES_TEMPLATE = """	
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ECharts</title>
    <!-- 引入 echarts.js -->
    <script src="js/echarts.min.js"></script>
</head>
<body>
    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <p>GPU: AMD Radeon (TM) R9 380 Series  CPU: &nbsp; &nbsp; Intel(R) Core(TM) i7-6700 &nbsp; &nbsp; size: 16G</p>
    <div id="main" style="width: 600px;height:400px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main'));

        // 指定图表的配置项和数据
        var option = {
                legend: {},
                tooltip: {},
                dataset: {
                    dimensions: ['product','{{versions[0]}}','{{versions[1]}}','{{versions[2]}}','{{versions[3]}}','{{versions[4]}}'],
                    source: [
                        {product: 'open filmora',
                        {% for key, value in context.open_filmora.AMD_R9.iteritems() %}
                            '{{ key }}': {{ value}},
                        {% endfor %}
                         },
                        {product: 'export(CPU)',
                        {% for key, value in context.export_CPU.AMD_R9.iteritems() %}
                            '{{ key }}': {{ value}},
                        {% endfor %}
                         },
                        {product: 'export(GPU)',
                        {% for key, value in context.export_GPU.AMD_R9.iteritems() %}
                            '{{ key }}': {{ value}},
                        {% endfor %}
                         },
                    ]
                },
                xAxis: {type: 'category'},
                yAxis: {},
                // Declare several bar series, each will be mapped
                // to a column of dataset.source by default.
                series: [
                    {type: 'bar'},
                    {type: 'bar'},
                    {type: 'bar'},
                    {type: 'bar'},
                    {type: 'bar'}
                ]
            };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>

    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <p>GPU: NVIDIA GeForce GTX 970  CPU: &nbsp; &nbsp; Intel(R) Core(TM) i5-4460 &nbsp; &nbsp; size: 8G</p>
    <div id="main2" style="width: 600px;height:400px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main2'));

        // 指定图表的配置项和数据
        var option = {
                legend: {},
                tooltip: {},
                dataset: {
                    dimensions: ['product','{{versions[0]}}','{{versions[1]}}','{{versions[2]}}','{{versions[3]}}','{{versions[4]}}'],
                    source: [
                        {product: 'open filmora',
                        {% for key, value in context.open_filmora.NVIDIA_970.iteritems() %}
                            '{{ key }}': {{ value}},
                        {% endfor %}
                         },
                        {product: 'export(CPU)',
                        {% for key, value in context.export_CPU.NVIDIA_970.iteritems() %}
                            '{{ key }}': {{ value}},
                        {% endfor %}
                         },
                        {product: 'export(GPU)',
                        {% for key, value in context.export_GPU.NVIDIA_970.iteritems() %}
                            '{{ key }}': {{ value}},
                        {% endfor %}
                         },
                    ]
                },
                xAxis: {type: 'category'},
                yAxis: {},
                // Declare several bar series, each will be mapped
                // to a column of dataset.source by default.
                series: [
                    {type: 'bar'},
                    {type: 'bar'},
                    {type: 'bar'},
                    {type: 'bar'},
                    {type: 'bar'}
                ]
            };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>

    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <p>GPU: NVIDIA GeForce GTX 1050  CPU: &nbsp; &nbsp; Intel(R) Core(TM) i7-7700HQ &nbsp; &nbsp; size: 8G</p>
    <div id="main3" style="width: 600px;height:400px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main3'));

        // 指定图表的配置项和数据
        var option = {
                legend: {},
                tooltip: {},
                dataset: {
                    dimensions: ['product','{{versions[0]}}','{{versions[1]}}','{{versions[2]}}','{{versions[3]}}','{{versions[4]}}'],
                    source: [
                        {product: 'open filmora',
                        {% for key, value in context.open_filmora.NVIDIA_1050.iteritems() %}
                            '{{ key }}': {{ value}},
                        {% endfor %}
                         },
                        {product: 'export(CPU)',
                        {% for key, value in context.export_CPU.NVIDIA_1050.iteritems() %}
                            '{{ key }}': {{ value}},
                        {% endfor %}
                         },
                        {product: 'export(GPU)',
                        {% for key, value in context.export_GPU.NVIDIA_1050.iteritems() %}
                            '{{ key }}': {{ value}},
                        {% endfor %}
                         },
                    ]
                },
                xAxis: {type: 'category'},
                yAxis: {},
                // Declare several bar series, each will be mapped
                // to a column of dataset.source by default.
                series: [
                    {type: 'bar'},
                    {type: 'bar'},
                    {type: 'bar'},
                    {type: 'bar'},
                    {type: 'bar'}
                ]
            };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>

    <!-- 为ECharts准备一个具备大小（宽高）的Dom -->
    <p>GPU: Intel(R) HD Graphics 5500  CPU: &nbsp; &nbsp; Intel(R) Core(TM) i5-5200U &nbsp; &nbsp; size: 4G</p>
    <div id="main4" style="width: 600px;height:400px;"></div>
    <script type="text/javascript">
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('main4'));

        // 指定图表的配置项和数据
        var option = {
                legend: {},
                tooltip: {},
                dataset: {
                    dimensions: ['product','{{versions[0]}}','{{versions[1]}}','{{versions[2]}}','{{versions[3]}}','{{versions[4]}}'],
                    source: [
                        {product: 'open filmora',
                        {% for key, value in context.open_filmora.Intel_5500.iteritems() %}
                            '{{ key }}': {{ value}},
                        {% endfor %}
                         },
                        {product: 'export(CPU)',
                        {% for key, value in context.export_CPU.Intel_5500.iteritems() %}
                            '{{ key }}': {{ value}},
                        {% endfor %}
                         },
                        {product: 'export(GPU)',
                        {% for key, value in context.export_GPU.Intel_5500.iteritems() %}
                            '{{ key }}': {{ value}},
                        {% endfor %}
                         },
                    ]
                },
                xAxis: {type: 'category'},
                yAxis: {},
                // Declare several bar series, each will be mapped
                // to a column of dataset.source by default.
                series: [
                    {type: 'bar'},
                    {type: 'bar'},
                    {type: 'bar'},
                    {type: 'bar'},
                    {type: 'bar'}
                ]
            };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    </script>
</body>
</html>
"""

result = jinja2.Template(source=RENDER_RULES_TEMPLATE).render(versions=versions,context=context)
print result

# from jinja2 import PackageLoader, Environment
#
# env = Environment(loader=PackageLoader('python_project', 'templates'))  # 创建一个包加载器对象
#
# template = env.get_template('3.html')  # 获取一个模板文件
# template.render(name='daxin', age=rules)  # 渲染

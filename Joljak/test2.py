import pandas as pd
import os
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool, CustomJS, RadioButtonGroup
from bokeh.layouts import column
from bokeh.io import curdoc
from bokeh.resources import INLINE
from bokeh.models import NumeralTickFormatter

table_names = [
    'BGF리테일_test_result'
]
csv_dir = r'C:\Users\wnsgm\OneDrive\바탕 화면\Stock_Project\Joljak\data\Alist'

for table_name in table_names:

    csv_path = os.path.join(csv_dir, f'{table_name}.csv')

    # CSV 파일에서 데이터 읽어오기
    # data = pd.read_csv(r'C:\Users\JUNI\Desktop\Stock_Project\stock\data\A_lstm\BGF리테일_test_result.csv')
    data = pd.read_csv(csv_path)

    # 날짜를 datetime 형식으로 변환
    data['Date'] = pd.to_datetime(data['Date'])

    # ColumnDataSource 생성
    source = ColumnDataSource(data=dict(Date=data['Date'], Actual=data['Actual Closing Price'], Forecast=data['Forecast Closing Price']))

    # 빈 figure 생성
    title_name = table_name.replace("_test_result", "")
    p = figure(x_axis_type="datetime", title=f"{title_name}", height=600, width=1500)

    p.title.align = 'center'  # 제목 가운데 정렬
    p.title.text_font_size = '25pt'  # 제목 글자 크기 조절
    p.yaxis.formatter = NumeralTickFormatter(format='0,0')

    # 눈금 크기 및 스타일 조절
    p.yaxis.major_label_text_font_size = '15pt'  # 눈금 텍스트 크기 조절
    p.yaxis.major_label_text_font_style = 'bold'  # 눈금 텍스트 굵게 설정

    # 눈금 크기 및 스타일 조절
    p.xaxis.major_label_text_font_size = '15pt'  # 눈금 텍스트 크기 조절
    p.xaxis.major_label_text_font_style = 'bold'  # 눈금 텍스트 굵게 설정

    # 실제 종가와 예측 종가 라인 그리기
    line_actual = p.line('Date', 'Actual', source=source, legend_label='실제 종가', line_width=2, color='blue')
    line_forecast = p.line('Date', 'Forecast', source=source, legend_label='예측 종가', line_width=2, color='red')
    p.legend.location = 'top_right'

    hover_forecast = HoverTool(renderers=[line_forecast], tooltips=[("날짜", "@Date{%F}"), ("실제 종가", "@Actual{0,0}"), ("예측 종가", "@Forecast{0,0}")],
                            formatters={'@Date': 'datetime'}, mode='vline')

    p.add_tools(hover_forecast)

    # 라디오 버튼 그룹 생성
    radio_button_group = RadioButtonGroup(labels=["최근 1주", "최근 1개월", "최근 3개월", "전체"], active=3)

    callback = CustomJS(args=dict(source=source, original_data=source.data, p=p), code="""
        var data = source.data;
        var original_data = original_data;
        var f = cb_obj.active;
        var date = original_data['Date'];
        var actual = original_data['Actual'];
        var forecast = original_data['Forecast'];

        // 그래프의 확대/축소, 팬 이동 상태 초기화
        p.reset.emit();

        var new_date = [];
        var new_actual = [];
        var new_forecast = [];

        if (f == 0) {
            for (var i = date.length - 7; i < date.length; i++) {
                new_date.push(date[i]);
                new_actual.push(actual[i]);
                new_forecast.push(forecast[i]);
            }
        } else if (f == 1) {
            for (var i = date.length - 30; i < date.length; i++) {
                new_date.push(date[i]);
                new_actual.push(actual[i]);
                new_forecast.push(forecast[i]);
            }
        } else if (f == 2) {
            for (var i = date.length - 90; i < date.length; i++) {
                new_date.push(date[i]);
                new_actual.push(actual[i]);
                new_forecast.push(forecast[i]);
            }
        } else {
            new_date = date;
            new_actual = actual;
            new_forecast = forecast;
        }

        data['Date'] = new_date;
        data['Actual'] = new_actual;
        data['Forecast'] = new_forecast;
        source.change.emit();
    """)

    radio_button_group.js_on_change('active', callback)

    # 레이아웃 설정
    layout = column(radio_button_group, p)

    # HTML 파일로 저장
    output_file(f"C:\\Users\\wnsgm\\OneDrive\\바탕 화면\\Stock_Project\\Joljak\\data\\stock_graph\\{table_name}.html")
    save(layout, resources=INLINE)
    print(f"HTML file saved as {table_name}.html")
import pandas as pd
import os
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool, CustomJS, RadioButtonGroup
from bokeh.layouts import column
from bokeh.io import curdoc
from bokeh.resources import INLINE
from bokeh.models import NumeralTickFormatter

table_names = [
    'bgf리테일_test_result', 'cj제일제당_test_result', 'db손해보험_test_result', 'f&f_test_result', 'gs_test_result',
    'gs리테일_test_result', 'hd한국조선해양_test_result', 'hd현대_test_result', 'hd현대중공업_test_result', 'hmm_test_result',
    'kb금융_test_result', 'kt&g_test_result', 'kt_test_result', 'lg_test_result', 'lg디스플레이_test_result',
    'lg생활건강_test_result', 'lg에너지솔루션_test_result', 'lg유플러스_test_result', 'lg이노텍_test_result', 'lg전자_test_result',
    'lg화학_test_result', 'naver_test_result', 'nh투자증권_test_result', 'posco홀딩스_test_result', 's-oil_test_result',
    'sk 바이오팜_test_result', 'sk_test_result', 'skc_test_result', 'sk바이오사이언스_test_result', 'sk스퀘어_test_result',
    'sk아이이테크놀리지_test_result', 'sk이노베이션_test_result', 'sk텔레콤_test_result', 'sk하이닉스_test_result', '강원랜드_test_result',
    '고려아연_test_result', '금양_test_result', '금호석유_test_result', '기아_test_result', '기업은행_test_result', '넷마블_test_result',
    '대한항공_test_result', '두산밥캣_test_result', '두산에너빌리티_test_result', '롯데지주_test_result', '롯데케미칼_test_result',
    '메리츠금융지주_test_result', '미래에셋증권_test_result', '삼성sdi_test_result', '삼성sds_test_result', '삼성물산_test_result',
    '삼성바이오로직스_test_result', '삼성생명_test_result', '삼성엔지니어링_test_result', '삼성전기_test_result', '삼성전자_test_result',
    '삼성중공업_test_result', '삼성증권_test_result', '삼성카드_test_result', '삼성화재_test_result', '셀트리온_test_result',
    '신한지주_test_result', '쌍용c&e_test_result', '아모레g_test_result', '아모레퍼시픽_test_result', '에코프로머티리얼즈_test_result',
    '엔씨소프트_test_result', '오리온_test_result', '우리금융지주_test_result', '유한양행_test_result', '이마트_test_result',
    '제일기획_test_result', '카카오_test_result', '카카오뱅크_test_result', '카카오페이_test_result', '코웨이_test_result',
    '크래프톤_test_result', '포스코dx_test_result', '포스코인터내셔널_test_result', '포스코퓨처엠_test_result', '하나금융지주_test_result',
    '하이브_test_result', '한국가스공사_test_result', '한국금융지주_test_result', '한국전력_test_result', '한국타이어앤테크놀로지_test_result',
    '한국항공우주_test_result', '한미사이언스_test_result', '한미약품_test_result', '한온시스템_test_result', '한진칼_test_result',
    '한화솔루션_test_result', '한화에어로스페이스_test_result', '한화오션_test_result', '현대건설_test_result', '현대글로비스_test_result',
    '현대모비스_test_result', '현대제철_test_result', '현대차_test_result', '호텔신라_test_result'
]
csv_dir = r'C:\Users\JUNI\Desktop\Stock_Project\stock\data\A_lstm'

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
    output_file(f"C:/Apache24/flask/app/stock/static/stock_graph/{table_name}.html")
    save(layout, resources=INLINE)
    print(f"HTML file saved as {table_name}.html")

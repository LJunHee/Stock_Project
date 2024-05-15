def show_graph2():
    import matplotlib.pyplot as plt
    import pandas as pd
    from matplotlib import font_manager, rc
    from matplotlib.widgets import RadioButtons

    class HoverDisplay:
        def __init__(self, ax, lines):
            self.ax = ax
            self.lines = lines
            self.annotation_price = ax.annotate('', xy=(0, 0), xytext=(20, 20), textcoords='offset points',
                                                 bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                                                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
            self.annotation_price.set_visible(False)
            self.annotation_date = ax.annotate('', xy=(0, 0), xytext=(-40, -40), textcoords='offset points',
                                                bbox=dict(boxstyle='round,pad=0.5', fc='lightblue', alpha=0.5),
                                                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
            self.annotation_date.set_visible(False)
            self.point = ax.plot([], [], 'ko', markersize=5, visible=False)[0]

        def hover(self, event):
            if event.inaxes == self.ax:
                for line in self.lines:
                    contains, ind = line.contains(event)
                    if contains:
                        x, y = line.get_data()
                        index = ind['ind'][0]
                        x_hover = x[index]
                        y_hover = y[index]
                        if line.get_label() == '실제 종가':
                            label_text = '실제 종가'
                        elif line.get_label() == '예측 종가':
                            label_text = '예측 종가'
                        else:
                            label_text = ''
                        formatted_date = pd.to_datetime(x_hover).strftime('%Y-%m-%d')
                        y_hover_int = int(y_hover)
                        self.annotation_price.xy = (x_hover, y_hover)
                        self.annotation_price.set_text(f'{label_text}={y_hover_int:,.0f}')
                        self.annotation_price.set_visible(True)
                        self.annotation_date.xy = (x_hover, min(self.ax.get_ylim()))
                        self.annotation_date.set_text(f'날짜={formatted_date}')
                        self.annotation_date.set_visible(True)
                        self.point.set_data([x_hover], [y_hover])
                        self.point.set_visible(True)
                        plt.draw()
                        return
                self.annotation_price.set_visible(False)
                self.annotation_date.set_visible(False)
                self.point.set_visible(False)
                plt.draw()
            else:
                self.annotation_price.set_visible(False)
                self.annotation_date.set_visible(False)
                self.point.set_visible(False)
                plt.draw()

    # CSV 파일에서 데이터 읽어오기
    data = pd.read_csv(r'C:\Users\JUNI\Desktop\Stock_Project\stock\data\A_lstm\BGF리테일_test_result.csv')

    # 한글 폰트 설정
    font_path = 'C:/Windows/Fonts/malgun.ttf'  # 한글 폰트 경로
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)

    # 날짜를 datetime 형식으로 변환
    data['Date'] = pd.to_datetime(data['Date'])

    # 빈 figure 생성
    fig, ax = plt.subplots(figsize=(20, 10))

    # 우측 상단에 라디오 버튼 생성
    rax = plt.axes([0.8, 0.9, 0.1, 0.1], facecolor='lightgoldenrodyellow')
    periods = ['1주', '1개월', '3개월', '전체']
    radio = RadioButtons(rax, periods)

    # 처음에는 1주가 선택되어 있지 않도록 설정
    radio.set_active(3)

    hover_display = None  # 초기화

    # 기간 선택 함수
    def select_period(label):
        ax.clear()
        ax.set_xlabel('Date')
        ax.set_ylabel('Closing Price')
        selected_data = data
        # 선택된 기간에 따라 데이터 필터링
        if label == '1주':
            selected_data = data.iloc[-7:]
        elif label == '1개월':
            selected_data = data.iloc[-30:]
        elif label == '3개월':
            selected_data = data.iloc[-90:]

        # 실제 종가 그래프 그리기
        line_actual, = ax.plot(selected_data['Date'], selected_data['Actual Closing Price'], label='실제 종가')

        # 예측 종가 그래프 그리기
        line_forecast, = ax.plot(selected_data['Date'], selected_data['Forecast Closing Price'], label='예측 종가')

        nonlocal hover_display  # hover_display를 전역 변수로 사용

        # 기존의 hover_display 객체가 있다면 삭제
        if hover_display:
            del hover_display

        hover_display = HoverDisplay(ax, [line_actual, line_forecast])
        fig.canvas.mpl_connect('motion_notify_event', hover_display.hover)

        # Add artists to legend
        ax.legend(handles=[line_actual, line_forecast])

        ax.set_title('실제 종가 vs 예측 종가', fontsize=20, fontweight='bold', y=1.05, backgroundcolor='yellow', color='black')

        fig.canvas.draw()

    # 라디오 버튼의 상태가 변경되면 select_period 함수를 호출하여 그래프를 업데이트
    radio.on_clicked(select_period)

    # 처음에는 전체를 선택한 상태로 그래프 그리기
    select_period('전체')
    plt.show()


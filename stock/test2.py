import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager, rc

class HoverDisplay:
    def __init__(self, ax, lines):
        self.ax = ax
        self.lines = lines
        self.annotation = ax.annotate('', xy=(0, 0), xytext=(20, 20), textcoords='offset points',
                                       bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                                       arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        self.annotation.set_visible(False)
    
    def hover(self, event):
        if event.inaxes == self.ax:
            for line in self.lines:
                contains, ind = line.contains(event)
                if contains:
                    x, y = line.get_data()
                    index = ind['ind'][0]
                    x_hover = x[index]
                    y_hover = y[index]
                    self.annotation.xy = (x_hover, y_hover)
                    if line.get_label() == 'Actual Closing Price':
                        label_text = '실제 종가'
                    elif line.get_label() == 'Forecast Closing Price':
                        label_text = '예측 종가'
                    else:
                        label_text = ''
                    formatted_date = pd.to_datetime(x_hover).strftime('%Y-%m-%d')
                    # 소수점 이하를 제거하여 정수로 표시
                    y_hover_int = int(y_hover)
                    self.annotation.set_text(f'날짜={formatted_date}, {label_text}={y_hover_int}')
                    self.annotation.set_visible(True)
                    plt.draw()
                    return
            self.annotation.set_visible(False)
            plt.draw()
        else:
            self.annotation.set_visible(False)
            plt.draw()

class ZoomPan:
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
        self.base_xlim = None
        self.base_ylim = None

    def zoom_factory(self, ax, base_scale=1.1):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location
            if event.button == 'up':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'down':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
                print(event.button)
            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
            # Adjusting scale to ensure it doesn't go beyond original scale
            if new_width / (self.base_xlim[1] - self.base_xlim[0]) > 1:
                scale_factor = (self.base_xlim[1] - self.base_xlim[0]) / (cur_xlim[1] - cur_xlim[0])
                new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            if new_height / (self.base_ylim[1] - self.base_ylim[0]) > 1:
                scale_factor = (self.base_ylim[1] - self.base_ylim[0]) / (cur_ylim[1] - cur_ylim[0])
                new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
            relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()
        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)
        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax:
                return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None:
                return
            if event.inaxes != ax:
                return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)
            ax.figure.canvas.draw()

        fig = ax.get_figure() # get the figure of interest

        fig.canvas.mpl_connect('button_press_event', onPress)
        fig.canvas.mpl_connect('button_release_event', onRelease)
        fig.canvas.mpl_connect('motion_notify_event', onMotion)
        return onMotion

# CSV 파일에서 데이터 읽어오기
data = pd.read_csv(r'C:\Users\mintm\Documents\GitHub\Stock_Project\stock\data\A_lstm\BGF리테일_test_result.csv')

# 한글 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'  # 한글 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 날짜를 datetime 형식으로 변환
data['Date'] = pd.to_datetime(data['Date'])

# x와 y 데이터 추출
x = data['Date']
y_actual = data['Actual Closing Price']
y_forecast = data['Forecast Closing Price']

# 빈 figure 생성
fig, ax = plt.subplots(figsize=(20,10))

# 실제 종가 그래프 그리기
line_actual, = ax.plot(x, y_actual, label='Actual Closing Price')

# 예측 종가 그래프 그리기
line_forecast, = ax.plot(x, y_forecast, label='Forecast Closing Price')

# 그래프에 범례 추가
ax.legend()

hover_display = HoverDisplay(ax, [line_actual, line_forecast])
fig.canvas.mpl_connect('motion_notify_event', hover_display.hover)

# x축 레이블 설정
ax.set_xlabel('Date')

# x축 눈금 비우기
ax.set_xticks([])

# Store initial axis limits for later reference
zp = ZoomPan()
zp.base_xlim = ax.get_xlim()
zp.base_ylim = ax.get_ylim()

figZoom = zp.zoom_factory(ax, base_scale=1.1)
figPan = zp.pan_factory(ax)

plt.show()
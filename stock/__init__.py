from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
import test

app = Flask(__name__)

# MySQL 데이터베이스 연결 설정
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1324",
    database="kospistocks"
)

# 테이블 이름 리스트
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

# 검색 쿼리 함수 정의
def search_query(query):
    cursor = db.cursor()

    # 먼저 kospi 테이블에서 검색합니다.
    cursor.execute(f"SELECT * FROM kospi WHERE 종목명 LIKE %s OR 종목코드 LIKE %s", ('%' + query + '%', '%' + query + '%'))
    kospi_results = cursor.fetchall()

    # 만약 kospi 테이블에서 검색 결과가 있다면
    if kospi_results:
        # 검색한 테이블명을 확인하고 존재하면 결과 반환
        table_name = query + '_test_result'
        if table_name in table_names:
            cursor.execute(f"SELECT * FROM {table_name}")
            test_result_results = cursor.fetchall()
            return test_result_results
        else:
            return None
    else:
        # 검색 결과가 없으면 None 반환
        return None

#자동 완성 검색 쿼리 함수 정의
def search_query_name(query):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM kospi WHERE 종목명 LIKE %s OR 종목코드 LIKE %s", ('%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    return results

# 자동완성 엔드포인트 정의
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    term = request.args.get('term')
    if term:
        results = search_query_name(term)
        autocomplete_results = [{"label": item[1], "value": item[1]} for item in results]
        return jsonify(autocomplete_results)
    else:
        return jsonify([])  # 검색어가 없을 경우 빈 리스트 반환

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        results = search_query(query)
        return render_template('search.html', data=results, query=query)
    else:
        return render_template('search.html', data=None, query=None)


@app.route('/')
def index():
    return redirect(url_for('index_html'))

@app.route('/index.html')
def index_html():
    return render_template('index.html')

@app.route('/generic.html')
def generic_html():
    return render_template('generic.html')

@app.route('/elements.html')
def elements_html():
    return render_template('elements.html')

@app.route('/prediction.html')
def prediction_html():
    return render_template('prediction.html')

@app.route('/showGraph')
def show_graph():
    test.show_graph2()
    return redirect(url_for('search'))


if __name__ == "__main__":
    app.run()

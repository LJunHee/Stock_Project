from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL 데이터베이스 연결 설정
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1324",
    database="kospistocks"
)

# 검색 쿼리 함수 정의
def search_query(query):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM kospi WHERE 종목명 LIKE %s OR 종목코드 LIKE %s", ('%' + query + '%', '%' + query + '%'))
    results = cursor.fetchall()
    return results

# 자동완성 엔드포인트 정의
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    term = request.args.get('term')
    if term:
        results = search_query(term)
        autocomplete_results = [{"label": item[1], "value": item[2]} for item in results]
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

if __name__ == "__main__":
    app.run()

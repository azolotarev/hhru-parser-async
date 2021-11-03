from flask import Flask

from hhru_parser_async.reporter import read_cache

app = Flask(__name__)


@app.route("/")
def index():
    all_vacancies = '<h1>Container from web hook</h1>'
    all_vacancies += read_cache()
    # htmlize
    all_vacancies = all_vacancies.replace('\n\n\n', '<hr>')
    all_vacancies = all_vacancies.replace('\n', '<br>')
    return all_vacancies


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

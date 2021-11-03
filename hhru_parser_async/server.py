from flask import Flask

from hhru_parser_async.reporter import read_cache

app = Flask(__name__)


@app.route("/")
def index():
    all_vacancies = read_cache()
    # htmlize
    all_vacancies = all_vacancies.replace('\n\n\n', '<hr>')
    all_vacancies = all_vacancies.replace('\n', '<br>')
    return all_vacancies

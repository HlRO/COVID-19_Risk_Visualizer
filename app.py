import time 
import pandas as pd
import scripts.analysis as analysis
from flask import Flask, render_template, request

app = Flask(__name__)

def getRateChangeString(rate_change):
    # Check if the growth rate changed.
    if rate_change > 0.0:
        return 'up'
    elif rate_change == 0.0:
        return 'same'
    else:
        return 'down'

def common(name, data_path, data_source_html):
    # Calculate the estimations.
    [menu_items, current, day_rate, rate_change, update_time, time_1_per_500, time_1_per_3, time_everyone, time_no_bed] = analysis.Analyse(name, data_path + 'total_cases.csv', data_path + 'population.csv', data_path + 'beds.csv')

    # Create a list of countries.
    menu_items_html = ''
    for item in menu_items:
        menu_items_html += '<option value="' + str(item)+ '">' + str(item)+ '</option>\n'

    change_str = getRateChangeString(rate_change)

    html = render_template('index.html', 
        menu_items = menu_items_html,
        date = time.strftime('%b %d', update_time),
        current_total = '{:,d}'.format(current),
        rate = '{:4.0f}'.format(day_rate),
        change = change_str,
        name = name,
        time_1_per_500 = '{:3.0f}'.format(time_1_per_500), 
        time_1_per_3 = '{:3.0f}'.format(time_1_per_3), 
        time_everyone = '{:3.0f}'.format(time_everyone), 
        time_no_bed = '{:3.0f}'.format(time_no_bed),
        data_source = data_source_html,
        )
    return html

@app.route('/')
def top():
    return usa()

@app.route('/usa/')
def usa():
    name = request.args.get('name')
    if not name:
        name = 'California'

    # Create a list of data sources.
    data_source_html = "\
        <p class='appendix sentence'>Number of cases:<br> <a href='https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html'>The New York Times</a></p>\
        <p class='appendix sentence'>Population:<br> <a href='https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/state/detail'>United States Census</a></p>\
        <p class='appendix sentence'>Number of hospital beds:<br> <a href='https://www.kff.org/other/state-indicator/beds-by-ownership'>Kaiser Family Foundation</a></p>\
    "

    return common(name, 'data/usa/', data_source_html);

@app.route('/world/')
def world():
    name = request.args.get('name')
    if not name:
        name = 'Japan'

    # Create a list of data sources.
    data_source_html = "\
    <p class='appendix sentence'>Number of cases:<br> <a href='https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide'>European Centre for Disease Prevention and Control</a></p>\
    <p class='appendix sentence'>Population:<br> <a href='https://population.un.org/wpp/Download/Standard/CSV/'>United Nations</a></p>\
    <p class='appendix sentence'>Number of hospital beds:<br> <a href='https://apps.who.int/gho/data/view.main.HS07v'>World Health Organization</a>, \
    <a href='https://www.pwc.tw/en/publications/assets/taiwan-health-industries.pdf'>PricewaterhouseCoopers</a></p>\
    "

    return common(name, 'data/world/', data_source_html);

if __name__ == "__main__":
    app.run(host='0.0.0.0')

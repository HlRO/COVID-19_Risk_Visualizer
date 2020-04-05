import time 
import pandas as pd
import scripts.analysis as analysis
import scripts.world.analysis as analysis_world
from flask import Flask, render_template, request

app = Flask(__name__)

def GetRateChangeString(rate_change):
    # Check if the growth rate changed.
    if rate_change > 0.0:
        return 'up'
    elif rate_change == 0.0:
        return 'same'
    else:
        return 'down'

@app.route('/')
def usa():
    state = request.args.get('state')
    if not state:
        state = 'California'

    # Calculate the estimations.
    [current, day_rate, rate_change, stat_update_time, time_1_per_500, time_1_per_3, time_everyone, time_no_bed] = analysis.Analyse(state)

    # Check if the growth rate changed.
    if rate_change > 0.0:
        change_str = 'up'
    elif rate_change == 0.0:
        change_str = 'same'
    else:
        change_str = 'down'

    html = render_template('index.html', 
        date = time.strftime('%b %d', stat_update_time),
        current_total = '{:,d}'.format(current),
        rate = '{:4.0f}'.format(day_rate),
        change = change_str,
        state = state,
        time_1_per_500 = '{:3.0f}'.format(time_1_per_500), 
        time_1_per_3 = '{:3.0f}'.format(time_1_per_3), 
        time_everyone = '{:3.0f}'.format(time_everyone), 
        time_no_bed = '{:3.0f}'.format(time_no_bed))
    return html

@app.route('/world/')
def world():
    country = request.args.get('country')
    if not country:
        country = 'Japan'

    # Calculate the estimations.
    [names, current, day_rate, rate_change, update_time, time_1_per_500, time_1_per_3, time_everyone, time_no_bed] = analysis_world.Analyse(country)

    # Create a list of countries.
    menu_items = ''
    for name in names:
        menu_items += '<option value="' + str(name)+ '">' + str(name)+ '</option>\n'

    # Create a list of data sources.
    data_source = "\
    <p class='appendix sentence'>Number of cases:<br> <a href='https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide'>European Centre for Disease Prevention and Control</a></p>\
    <p class='appendix sentence'>Population:<br> <a href='https://population.un.org/wpp/Download/Standard/CSV/'>United Nations</a></p>\
    <p class='appendix sentence'>Number of hospital beds:<br> <a href='https://apps.who.int/gho/data/view.main.HS07v'>World Health Organization</a>, \
    <a href='https://www.pwc.tw/en/publications/assets/taiwan-health-industries.pdf'>PricewaterhouseCoopers</a></p>\
    "

    change_str = GetRateChangeString(rate_change)

    html = render_template('world/index.html', 
        menu_items = menu_items,
        date = time.strftime('%b %d', update_time),
        current_total = '{:,d}'.format(current),
        rate = '{:4.0f}'.format(day_rate),
        change = change_str,
        country = country,
        time_1_per_500 = '{:3.0f}'.format(time_1_per_500), 
        time_1_per_3 = '{:3.0f}'.format(time_1_per_3), 
        time_everyone = '{:3.0f}'.format(time_everyone), 
        time_no_bed = '{:3.0f}'.format(time_no_bed),
        data_source = data_source,
        )
    return html

if __name__ == "__main__":
    app.run(host='0.0.0.0')

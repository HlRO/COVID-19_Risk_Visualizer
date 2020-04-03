import time 
import scripts.analysis as analysis
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello():
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

if __name__ == "__main__":
    app.run(host='0.0.0.0')

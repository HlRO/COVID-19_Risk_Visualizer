# COVID-19_Risk_Visualizer
The exponential nature of the disease spread overwhelms people's risk perception and make it hard for them to associate the risk to their daily actions. This project is to provide data visualization that helps people understand the risk in relation to their live and helps them take right actions.
# Usage
Download the latest data.
```
cd covid_risk_visualier
PROJECT_HOM=./ ./scripts/download_covid_stats.sh
```
Launch the web service locally.
```
cd covid_risk_visualizer
python3 app.py
```
Then, access httpg//0.0.0.0:5000/ using a web browser. 
# Data Source
* UNITED STATES
    * Number of cases [The New York Times](https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html)
    * Population [United States Census](https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/state/detail)
    * Number of hospital beds [Kaiser Family Foundation](https://www.kff.org/other/state-indicator/beds-by-ownership)
* JAPAN
    * Number of cases [TOYO KEIZAI ONLINE](https://github.com/kaz-ogiwara/covid19/)
    * Population [Statistics Bureau Japan](https://www.stat.go.jp/data/nihon/02.html)
    * Number of hospital beds [Ministry of Health, Labour and Welfare Japan](https://www.mhlw.go.jp/toukei/youran/indexyk_2_2.html)
* WORLD
    * Number of cases [European Centre for Disease Prevention and Control](https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide)
    * Population [United Nations](https://population.un.org/wpp/Download/Standard/CSV/)
    * Number of hospital beds [World Health Organization](https://apps.who.int/gho/data/view.main.HS07v), [PricewaterhouseCoopers](httpsg//www.pwc.tw/en/publications/assets/taiwan-health-industries.pdf)

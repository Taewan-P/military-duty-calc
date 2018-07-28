from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('home.html')


@app.route('/submit', methods=['POST'])
def submit():
    date = request.form['date']
    import datetime
    try:
        datetime.datetime.strptime(date, '%Y%m%d')
    except ValueError:
        return render_template('error.html')
    type = request.form['military type']
    if type == "군별선택":
        return render_template('error2.html')
    elif type == "육군/의경" or type == "해병" or type == "의무소방":
        total_month = 21
    elif type == "해군/해양의무경찰":
        total_month = 22
    elif type == "공군" or type == "사회복무요원":
        total_month = 24
    else:
        total_month = 0
    year, month, day = int(date[:4]), int(date[4:6]) + total_month, int(date[6:])
    while(month > 12):
        year += 1
        month -= 12
    day -= 1
    if day == 0:
        finish_date = datetime.datetime(year, month, day + 1) - datetime.timedelta(days=1)
    else:
        finish_date = datetime.datetime(year, month, day)
    total_time = finish_date - datetime.datetime(int(date[:4]), int(date[4:6]), int(date[6:]))
    remain_time = finish_date - datetime.datetime.now()
    if int(remain_time.days) > int(total_time.days):
        remain_day = 0
    else:
        remain_day = int(remain_time.days)
    percent = round(remain_day / total_time.days * 100,1)
    if int(remain_time.days) < 0:
        remain_day = total_time.days
        percent = 100
    shorten_time = datetime.datetime(int(date[:4]), int(date[4:6]), int(date[6:])) - datetime.datetime(2016,9,15)
    shorten_day = shorten_time.days//14
    result = datetime.datetime(finish_date.year, finish_date.month, finish_date.day) - datetime.timedelta(
        days=shorten_day)
    finish_year, finish_month, finish_day = finish_date.year, finish_date.month, finish_date.day
    if (datetime.datetime(int(date[:4]), int(date[4:6]), int(date[6:])) - datetime.datetime(finish_date.year, finish_date.month, finish_date.day)).days > 0:
        shorten_day = 0
        result = datetime.datetime(finish_date.year, finish_date.month, finish_date.day)
    return render_template('result.html', result=total_month, year=finish_year, month=finish_month, day=finish_day, total_day=total_time.days, remain_day=remain_day, percent=percent, shorten_days=shorten_day
                           ,shorten_year=result.year, shorten_month=result.month, shorten_day=result.day)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
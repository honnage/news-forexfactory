import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
from datetime import datetime, timedelta, date
import time

def GetNews(date, option_news, currency_type):
    current_date = date.strftime("%Y-%m-%d")
    current_date = datetime.strptime(current_date, '%Y-%m-%d').date()
    # current_date = FormatDate(current_date)  # แปลง current_date_str เป็นวัตถุ datetime.date
    formatted_date = current_date.strftime("%b%d.%Y").lower()

    day = current_date.strftime('%d').lower()
    day_name = current_date.strftime('%a')  # Abbreviated day names
    # day_name = current_date.strftime('%A').lower()  # full name date
    month_name = current_date.strftime('%b').lower()
    month_num = current_date.strftime('%m')
    year = current_date.strftime('%Y').lower()

    # Create a new date format
    date_format = date.strftime("%b%d.%Y")
    # print(date_format)  # Result "Jul05.2023"

    news_date = f'calendar?day={date_format}'
    # print('get news:', news_date)
    scraper = cloudscraper.create_scraper()
    url = 'https://www.forexfactory.com/' + news_date
    print('\nurl', url,)

    page = scraper.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    # Take out the <div> of name and get its value

    # Find the table containing all the data
    table = soup.find('table', class_='calendar__table')
    event_times = table.find_all('td', class_='calendar__time')   # Event Times


    # if (day_name != 'Sat' and day_name != 'Sun'):
    if (True): # All Day
        data_news = []

        print('option news:', option_news)
        print('currency type:', currency_type)

        for news in event_times:
            curr = news.find_next_sibling('td', class_='calendar__currency').text.strip()
            impacts = news.find_next_sibling( 'td', class_='calendar__impact').find_next('span')['class']
            impact_level = impacts[1].replace('icon--ff-impact-', '')
            # impact_icon = impacts[0]
            # impact = "%s-%s" % (impact_icon, impact_level)
            impact = "%s" % (impact_level)
            event = news.find_next_sibling('td', class_='calendar__event').find_next('span').text.strip()
            previous = news.find_next_sibling('td', class_='calendar__previous').text.strip()
            forecast = news.find_next_sibling('td', class_='calendar__forecast').text.strip()
            actual = news.find_next_sibling('td', class_='calendar__actual').text.strip()
            event_time = news.text.strip()
            date = "%02d %s %s" % (int(day), str(month_num), year)
            formatted_date = "%s-%s-%02d " % (year,  str(month_num), int(day) )

            try:
                # Case: Focus
                if option_news == 'Focus':
                    # Currency All
                    if not currency_type:
                        raw = {
                            'date_news': date_format,
                            'date': formatted_date,
                            'day_name': day_name,
                            'event_time': event_time,
                            'curr': curr,
                            'impact': impact,
                            'news': event,
                            # "news_lower": event.lower(),
                            'previous': previous,
                            'forecast': forecast,
                            'actual': actual
                        }
                        data_news.append(raw)

                    # Currency By
                    elif curr in currency_type:
                        raw = {
                            'date_news': date_format,
                            'date': formatted_date,
                            'day_name': day_name,
                            'event_time': event_time,
                            'curr': curr,
                            'impact': impact,
                            'news': event,
                            # "news_lower": event.lower(),
                            'previous': previous,
                            'forecast': forecast,
                            'actual': actual
                        }
                        data_news.append(raw)

                # Case: Not Focus
                else:
                    # Currency All
                    if not currency_type:
                        data_news = []

                    # Currency By
                    elif curr not in currency_type:
                        raw = {
                            'date_news': date_format,
                            'date': formatted_date,
                            'day_name': day_name,
                            'event_time': event_time,
                            'curr': curr,
                            'impact': impact,
                            'news': event,
                            # "news_lower": event.lower(),
                            'previous': previous,
                            'forecast': forecast,
                            'actual': actual
                        }
                        data_news.append(raw)

            except Exception as e:
                print("There was an error: " + str(e))

        return data_news

    else:
        # print('='*30)
        # print('no date')
        # print('='*30, '\n')
        return ''


def DataNews(startDate_news, endDate_news, option_news, currency_type):
    startDate_news = datetime.strptime(startDate_news, '%Y-%m-%d').date()
    endDate_news = datetime.strptime(endDate_news, '%Y-%m-%d').date()

    data_news_list = []
    for n in range((endDate_news - startDate_news).days + 1):
        current_date = startDate_news + timedelta(days=n)
        data_news = GetNews(current_date, option_news, currency_type)

        if (len(data_news) > 0) :
            df = pd.DataFrame(data_news)
            df.index = df.index + 1  # กำหนด index เริ่มต้นที่ 1
            print(tabulate(df, showindex=False, headers=df.columns))
            # print('df', df)
        else:
            print('No Data.')

        data_news_list.extend(data_news)

    return data_news_list


def main():
    startDate_news = '2023-08-20'
    endDate_news = '2023-08-26'

    # 'Focus' or 'Not Focus'
    option_news = 'Not Focus'
    currency_type = ['USD'] # ['JPY', 'NZD', 'GBP', 'EUR', 'CNY']
    # currency_type = []

    dataNews = DataNews(startDate_news, endDate_news, option_news, currency_type)
    dataPD = pd.DataFrame(dataNews)  # สร้าง DataFrame จากลิสต์ของดิกชันนารี
    dataPD.index = dataPD.index + 1  # กำหนด index เริ่มต้นที่ 1
    newsAll = tabulate(dataPD, showindex=True, headers=dataPD)
    countNews = len(newsAll)
    if (countNews > 0):
        print('\n','News All\n', newsAll)

    else:
        print('\n','None News\n',)

if __name__ == "__main__":
    main()
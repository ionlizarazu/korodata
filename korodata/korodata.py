from unidecode import unidecode

import datetime
import json
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import os
import string
import urllib.request


class Korodata():
    """docstring for ClassName"""

    def __init__(self):
        super(Korodata, self).__init__()

    def datetimeTodate(date, delta):
        return datetime.datetime.strftime(
            datetime.datetime.strptime(
                date, '%Y-%m-%dT%H:%M:%SZ') - datetime.timedelta(days=delta),
            '%Y-%m-%d')

    def getHerriThisDate(herriname, herrilist, datesearch):
        for herri in herrilist:
            i = 0
            if 'geoMunicipality' in herri.keys():
                if herriname in herri['geoMunicipality']['officialName']:
                    return int(herri['positiveCount'])
        return 0

    def getHerriBefore(herriname, date, days):
        datesearch = Korodata.datetimeTodate(date, days)
        datetoprint = Korodata.datetimeTodate(date, days - 1)
        with open('tmp.json', 'r') as file:
            data_str = file.read()
            data = json.loads(data_str)
            for egun in data['newPositivesByDateByMunicipality']:

                if(datesearch in egun['date']):
                    return Korodata.getHerriThisDate(herriname, egun['items'], datetoprint[5:]), datetoprint[5:]

    def draw_figure(j, herriname, datesforplot, positivesforplot):
        plt.figure(j, figsize=(14, 8))
        barlist = plt.bar(datesforplot, positivesforplot)
        Korodata.colorize_chart(barlist, positivesforplot)
        handles = [mpatches.Patch(color='white')]
        i = 0
        while i < len(Korodata.colors()):
            if i == 0:
                handles.append(mpatches.Patch(
                    facecolor=Korodata.colors()[i], label='Lasai baina arduraz', hatch=Korodata.hatches()[i], edgecolor='k'))
            elif i == len(Korodata.colors()) - 1:
                handles.append(mpatches.Patch(
                    facecolor=Korodata.colors()[i], label='Joera kezkagarria', hatch=Korodata.hatches()[i], edgecolor='k'))
            else:
                handles.append(mpatches.Patch(facecolor=Korodata.colors()[
                               i], hatch=Korodata.hatches()[i], edgecolor='k'))
            i += 1
        leg = plt.legend(loc='upper left', handles=handles,
                         title="Datuen joera", labelspacing=1, title_fontsize=13, handlelength=4)
        for patch in leg.get_patches():
            patch.set_height(15)
        for index, value in enumerate(positivesforplot):
            plt.text(index, value * 1.01, str(value))
        plt.text(len(positivesforplot) * 0.35, max(positivesforplot) * -0.09, 'Azken ' +
                 str(len(positivesforplot)) + ' egunetan guztira: ' + str(sum(positivesforplot)))
        plt.title(herriname)
        os.makedirs('./grafikak')
        plt.savefig('./grafikak/' +
                    "".join(x for x in herriname if x.isalnum()) + '.png')
        plt.close(plt.figure(j, figsize=(14, 8)))

    def set_color(i, color, colors_l, barlist):
        hatch = Korodata.hatches()[Korodata.colors().index(color)]
        barlist[i].set_hatch(hatch)
        barlist[i].set_color(color)
        barlist[i].set_edgecolor('k')
        colors_l[i] = color
        return colors_l

    def colors():
        color_list = ['green', 'yellowgreen', 'greenyellow',
                      'yellow', 'gold', 'orange', 'darkorange', 'red']
        return color_list

    def hatches():
        hatch_list = ["", "/", "//", "x", ".", "o", "O", "*"]
        return hatch_list

    def select_color(color, diff):
        color_list = Korodata.colors()
        if (color_list.index(color) == 0 and diff < 0) or (color_list.index(color) == len(color_list) - 1 and diff > 0):
            return color
        elif (color_list.index(color) == len(color_list) - 2 and diff > 1):
            diff = 1
        elif (color_list.index(color) == 1 and diff < -1):
            diff = -1
        return color_list[color_list.index(color) + diff]

    def colorize_chart(barlist, values):
        colors = ['b'] * len(barlist)
        starters = values[:3]
        if min(starters) == values[0] and values[0] == 0:
            colors = Korodata.set_color(0, 'green', colors, barlist)
        elif min(starters) == values[0] and values[0] != 0:
            colors = Korodata.set_color(0, 'yellowgreen', colors, barlist)
        elif min(starters) == values[1]:
            colors = Korodata.set_color(0, 'yellowgreen', colors, barlist)
        elif min(starters) == values[2]:
            if values[0] < values[1] and values[0] == 0:
                colors = Korodata.set_color(0, 'green', colors, barlist)
            elif values[0] < values[1] and values[0] != 0:
                colors = Korodata.set_color(0, 'yellowgreen', colors, barlist)
            elif values[0] > values[1]:
                colors = Korodata.set_color(0, 'yellowgreen', colors, barlist)
            elif values[0] == values[1]:
                colors = Korodata.set_color(0, 'yellowgreen', colors, barlist)

        i = 1
        while i < len(barlist):
            if values[i] == 0:
                colors = Korodata.set_color(i, 'green', colors, barlist)
            elif values[i - 1] < values[i]:
                diff = 1
                if (values[i - 1] * 2 < values[i] and values[i - 1] != 0) or (4 < values[i] and values[i - 1] == 0):
                    diff = 2
                colors = Korodata.set_color(i, Korodata.select_color(
                    colors[i - 1], diff), colors, barlist)
            elif values[i - 1] > values[i]:
                diff = -1
                colors = Korodata.set_color(i, Korodata.select_color(
                    colors[i - 1], diff), colors, barlist)
            else:
                colors = Korodata.set_color(i, colors[i - 1], colors, barlist)
            i += 1

    def format_filename(s):
        valid_chars = "-_%s%s" % (string.ascii_letters, string.digits)
        filename = ''.join(c for c in unidecode(s) if c in valid_chars)
        return filename

    def has_today_data():
        with urllib.request.urlopen("https://opendata.euskadi.eus/contenidos/ds_informes_estudios/covid_19_2020/opendata/generated/covid19-bymunicipality.json") as url:
            url_str = url.read().decode('unicode_escape').encode('utf-8')
            data = json.loads(url_str)
            today = datetime.datetime.strftime(
                datetime.datetime.now(), '%Y-%m-%d')
            lastUpdate = datetime.datetime.strftime(
                datetime.datetime.strptime(
                    data['lastUpdateDate'], '%Y-%m-%dT%H:%M:%SZ'),
                '%Y-%m-%d %H:%M'
            )
            return today in lastUpdate

    def azkenEguneraketa():
        with urllib.request.urlopen("https://opendata.euskadi.eus/contenidos/ds_informes_estudios/covid_19_2020/opendata/generated/covid19-bymunicipality.json") as url:
            url_str = url.read().decode('unicode_escape').encode('utf-8')
            data = json.loads(url_str)
            lastUpdate = datetime.datetime.strftime(
                datetime.datetime.strptime(
                    data['lastUpdateDate'], '%Y-%m-%dT%H:%M:%SZ'),
                '%Y-%m-%d %H:%M'
            )
            return lastUpdate
    def herria(herriname):
        how_may_days_original = 24
        days = 0
        file = None
        with urllib.request.urlopen("https://opendata.euskadi.eus/contenidos/ds_informes_estudios/covid_19_2020/opendata/generated/covid19-bymunicipality.json") as url:
            f = open('tmp.json', 'w')
            url_str = url.read().decode('unicode_escape').encode('utf-8')
            data = json.loads(url_str)
            f.write(str(json.dumps(data)))
            lastUpdate = datetime.datetime.strftime(
                datetime.datetime.strptime(
                    data['lastUpdateDate'], '%Y-%m-%dT%H:%M:%SZ'),
                '%Y-%m-%d %H:%M'
            )

            herritot = 0
            datesforplot = []
            positivesforplot = []
            i = 0
            herria = ''
            for herri in data['newPositivesByDateByMunicipality'][len(data['newPositivesByDateByMunicipality']) - 1]['items']:
                datesforplot = []
                positivesforplot = []
                herritot = 0
                how_may_days = how_may_days_original
                if 'geoMunicipality' in herri.keys():
                    if herriname.lower() in herri['geoMunicipality']['officialName'].lower():
                        herria = herri['geoMunicipality']['officialName']
                        i += 1
                        print('#' + herriname)
                        date = data['newPositivesByDateByMunicipality'][
                            len(data['newPositivesByDateByMunicipality']) - 1]['date']
                        while days <= how_may_days:
                            herrisum, datetoplot = Korodata.getHerriBefore(
                                herria, date, how_may_days)
                            positivesforplot.append(herrisum)
                            datesforplot.append(datetoplot)
                            herritot += herrisum
                            how_may_days -= 1
                        Korodata.draw_figure(
                            i, herria, datesforplot, positivesforplot)
                        lastDays = 'Azken ' + \
                            str(len(positivesforplot)) + \
                            ' egunetan guztira: ' + str(sum(positivesforplot))

    def zerrenda():
        min_positives = 2
        how_may_days_original = 24
        days = 0

        with urllib.request.urlopen("https://opendata.euskadi.eus/contenidos/ds_informes_estudios/covid_19_2020/opendata/generated/covid19-bymunicipality.json") as url:
            f = open('tmp.json', 'w')
            url_str = url.read().decode('unicode_escape').encode('utf-8')
            data = json.loads(url_str)
            f.write(str(json.dumps(data)))
            lastUpdate = datetime.datetime.strftime(
                datetime.datetime.strptime(
                    data['lastUpdateDate'], '%Y-%m-%dT%H:%M:%SZ'),
                '%Y-%m-%d %H:%M'
            )
            print('Azken eguneraketa:', lastUpdate)
            herritot = 0
            datesforplot = []
            positivesforplot = []
            i = 0
            for herri in data['newPositivesByDateByMunicipality'][len(data['newPositivesByDateByMunicipality']) - 1]['items']:
                datesforplot = []
                positivesforplot = []
                herritot = 0
                how_may_days = how_may_days_original
                herriname = herri['geoMunicipality']['officialName']
                if herri['positiveCount'] >= min_positives:
                    i += 1
                    print('#' + herriname)
                    date = data['newPositivesByDateByMunicipality'][
                        len(data['newPositivesByDateByMunicipality']) - 1]['date']
                    while days <= how_may_days:
                        herrisum, datetoplot = Korodata.getHerriBefore(
                            herriname, date, how_may_days)
                        positivesforplot.append(herrisum)
                        datesforplot.append(datetoplot)
                        herritot += herrisum
                        how_may_days -= 1
                    Korodata.draw_figure(
                        i, herriname, datesforplot, positivesforplot)
                    lastDays = 'Azken ' + \
                        str(len(positivesforplot)) + \
                        ' egunetan guztira: ' + str(sum(positivesforplot))

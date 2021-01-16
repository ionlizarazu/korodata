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
                if herriname == herri['geoMunicipality']['officialName']:
                    return int(herri['positiveCount'])
        return 0

    def getHerriBefore(herriname, date, days, data):
        datesearch = Korodata.datetimeTodate(date, days)
        datetoprint = Korodata.datetimeTodate(date, days - 1)
        if 'newPositivesByDateByMunicipality' in data.keys():
            for egun in data['newPositivesByDateByMunicipality']:
                if(datesearch[5:] in egun['date']):
                    return Korodata.getHerriThisDate(herriname, egun['items'], datetoprint[5:]), datetoprint[5:]
        return 0, 'EA'

    def draw_figure(j, herriname, datesforplot, positivesforplot, population=1):
        plt.figure(j, figsize=(14, 9))
        barlist = plt.bar(datesforplot, positivesforplot, width=0.6)
        Korodata.colorize_chart(barlist, positivesforplot, population)
        handles = [mpatches.Patch(color='white')]
        labels = ['Kalkulatu gabe', '< 40', '40 - 60', '60 - 170',
                  '170 - 300', '300 - 400', '400 - 500', '>= 500']
        i = 0
        while i < len(Korodata.colors()):
            handles.append(mpatches.Patch(facecolor=Korodata.colors()[i], label=labels[
                           i], hatch=Korodata.hatches()[i], edgecolor='k'))
            i += 1
        leg = plt.legend(loc='upper left', handles=handles,
                         title="Inzidentzia-tasa", labelspacing=1, title_fontsize=13, handlelength=4)
        for patch in leg.get_patches():
            patch.set_height(15)
        for index, value in enumerate(positivesforplot):
            plt.text(index - 0.6, value * 1.01, str(value))

        hamalauEgun = positivesforplot[len(positivesforplot) - 14:]
        per100 = 100000 * sum(hamalauEgun) / population
        plt.text(len(positivesforplot) * 0.20, max(positivesforplot) * -0.12, 'Azken ' +
                 str(len(hamalauEgun)) + ' egunetan: Guztira ' + str(sum(hamalauEgun)) +
                 ' positibo | 100M biztanleko ' + str(round(per100, 2)), fontsize=17)
        plt.text(len(positivesforplot) * 0.1, max(positivesforplot) * 1.09,
                 'COVID-19aren garapena azken 60 egunetan. Kasuak eguneko eta inzidentzia-tasa.', fontsize=17)
        plt.title(herriname, fontsize=26, pad=50)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig('./korodata/grafikak/' +
                    "".join(x for x in herriname if x.isalnum()) + '.png')
        plt.close(plt.figure(j, figsize=(14, 9)))

    def set_color(i, color, colors_l, barlist):
        hatch = Korodata.hatches()[Korodata.colors().index(color)]
        barlist[i].set_hatch(hatch)
        barlist[i].set_color(color)
        barlist[i].set_edgecolor('k')
        colors_l[i] = color
        return colors_l

    def colors():
        color_list = ['grey', 'yellowgreen', 'greenyellow',
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

    def colorize_chart(barlist, values, population=1):
        colors = ['grey'] * len(barlist)
        i = 0
        if population > 5000:
            while i <= len(barlist):
                if i < 14:
                    colors = Korodata.set_color(i, 'grey', colors, barlist)
                else:
                    min_range = i - 14
                    per100 = 100000 * sum(values[min_range:i]) / population
                    # print(values[min_range:i], sum(values[min_range:i]), per100)
                    if per100 < 40:
                        colors = Korodata.set_color(
                            i - 1, 'yellowgreen', colors, barlist)
                    elif per100 < 60:
                        colors = Korodata.set_color(
                            i - 1, 'greenyellow', colors, barlist)
                    elif per100 < 170:
                        colors = Korodata.set_color(
                            i - 1, 'yellow', colors, barlist)
                    elif per100 < 300:
                        colors = Korodata.set_color(
                            i - 1, 'gold', colors, barlist)
                    elif per100 < 400:
                        colors = Korodata.set_color(
                            i - 1, 'orange', colors, barlist)
                    elif per100 < 500:
                        colors = Korodata.set_color(
                            i - 1, 'darkorange', colors, barlist)
                    else:
                        colors = Korodata.set_color(
                            i - 1, 'red', colors, barlist)
                i += 1
        else:
            while i < len(barlist):
                colors = Korodata.set_color(i, 'grey', colors, barlist)
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
            yesterday = Korodata.datetimeTodate(datetime.datetime.strftime(
                datetime.datetime.now(), '%Y-%m-%dT%H:%M:%SZ'), 2)
            lastUpdate = datetime.datetime.strftime(
                datetime.datetime.strptime(
                    data['lastUpdateDate'], '%Y-%m-%dT%H:%M:%SZ'),
                '%Y-%m-%d %H:%M'
            )
            return today in lastUpdate and yesterday in data['newPositivesByDateByMunicipality'][len(data['newPositivesByDateByMunicipality']) - 1]['date']

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
        how_may_days_original = 59
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
                        population = Korodata.getPopulation(herria, data)
                        i += 1
                        print('#' + herriname)
                        date = data['newPositivesByDateByMunicipality'][
                            len(data['newPositivesByDateByMunicipality']) - 1]['date']
                        while days <= how_may_days:
                            herrisum, datetoplot = Korodata.getHerriBefore(
                                herria, date, how_may_days, data)
                            positivesforplot.append(herrisum)
                            datesforplot.append(datetoplot)
                            herritot += herrisum
                            how_may_days -= 1
                        Korodata.draw_figure(
                            i, herria, datesforplot, positivesforplot, population)
                        print(
                            len(positivesforplot[len(positivesforplot) - 14:]))
                        lastDays = 'Azken ' + \
                            str(len(positivesforplot[len(positivesforplot) - 14:])) + \
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
                if 'geoMunicipality' in herri.keys():
                    herriname = herri['geoMunicipality']['officialName']
                    if herri['positiveCount'] >= min_positives:
                        i += 1
                        print('#' + herriname)
                        date = data['newPositivesByDateByMunicipality'][
                            len(data['newPositivesByDateByMunicipality']) - 1]['date']
                        while days <= how_may_days:
                            herrisum, datetoplot = Korodata.getHerriBefore(
                                herriname, date, how_may_days, data)
                            positivesforplot.append(herrisum)
                            datesforplot.append(datetoplot)
                            herritot += herrisum
                            how_may_days -= 1
                        Korodata.draw_figure(
                            i, herriname, datesforplot, positivesforplot, population)
                        lastDays = 'Azken ' + \
                            str(len(positivesforplot)) + \
                            ' egunetan guztira: ' + str(sum(positivesforplot))

    def getProbintziaBefore(kodea, date, days, data):
        datesearch = Korodata.datetimeTodate(date, days)
        datetoprint = Korodata.datetimeTodate(date, days - 1)
        positives = 0
        for egun in data['newPositivesByDateByMunicipality']:
            if(datesearch in egun['date']):
                for herri in egun['items']:
                    if 'geoMunicipality' in herri.keys():
                        if kodea == herri['geoMunicipality']['countyId']:
                            positives += int(herri['positiveCount'])
        return positives, datetoprint[5:]

    def probintzia(kodea):
        switcher = {
            '01': "Araba",
            '48': "Bizkaia",
            '20': "Gipuzkoa"
        }
        probintzia = switcher.get(kodea, 'okerreko kodea')

        how_may_days_original = 59
        days = 0

        with urllib.request.urlopen("https://opendata.euskadi.eus/contenidos/ds_informes_estudios/covid_19_2020/opendata/generated/covid19-bymunicipality.json") as url:
            f = open('tmp.json', 'w')
            url_str = url.read().decode('unicode_escape').encode('utf-8')
            data = json.loads(url_str)
            f.write(str(json.dumps(data)))
            probintziaTot = 0
            probintziaSum = 0
            population = 0
            datesforplot = []
            positivesforplot = []
            date = data['newPositivesByDateByMunicipality'][
                len(data['newPositivesByDateByMunicipality']) - 1]['date']
            for herri in data['newPositivesByDateByMunicipality'][len(data['newPositivesByDateByMunicipality']) - 1]['items']:
                if 'geoMunicipality' in herri.keys():
                    if kodea == herri['geoMunicipality']['countyId']:
                        herriname = herri['geoMunicipality']['officialName']
                        population += Korodata.getPopulation(herriname, data)
            how_may_days = how_may_days_original
            while days <= how_may_days:
                probintziaSum, datetoplot = Korodata.getProbintziaBefore(
                    kodea, date, how_may_days, data)
                positivesforplot.append(probintziaSum)
                datesforplot.append(datetoplot)
                probintziaTot += probintziaSum
                how_may_days -= 1

            file = Korodata.draw_figure(
                1, probintzia, datesforplot, positivesforplot, population)
            print('#Korodatuak')
            print('---------------------------------')
        return file

    def getEaeBefore(date, days, data):
        datesearch = Korodata.datetimeTodate(date, days)
        datetoprint = Korodata.datetimeTodate(date, days - 1)
        positives = 0
        for egun in data['newPositivesByDateByMunicipality']:
            if(datesearch in egun['date']):
                for herri in egun['items']:
                    positives += int(herri['positiveCount'])
        return positives, datetoprint[5:]

    def eae():
        how_may_days_original = 59
        days = 0

        with urllib.request.urlopen("https://opendata.euskadi.eus/contenidos/ds_informes_estudios/covid_19_2020/opendata/generated/covid19-bymunicipality.json") as url:
            f = open('tmp.json', 'w')
            url_str = url.read().decode('unicode_escape').encode('utf-8')
            data = json.loads(url_str)
            f.write(str(json.dumps(data)))
            eaeTot = 0
            eaeSum = 0
            population = 0
            datesforplot = []
            positivesforplot = []
            date = data['newPositivesByDateByMunicipality'][
                len(data['newPositivesByDateByMunicipality']) - 1]['date']
            for herri in data['newPositivesByDateByMunicipality'][len(data['newPositivesByDateByMunicipality']) - 1]['items']:
                if 'geoMunicipality' in herri.keys():
                    herriname = herri['geoMunicipality']['officialName']
                    population += Korodata.getPopulation(herriname, data)
            how_may_days = how_may_days_original
            while days <= how_may_days:
                eaeSum, datetoplot = Korodata.getEaeBefore(
                    date, how_may_days, data)
                positivesforplot.append(eaeSum)
                datesforplot.append(datetoplot)
                eaeTot += eaeSum
                how_may_days -= 1

            file = Korodata.draw_figure(
                1, 'Euskal Autonomia Erkidegoa', datesforplot, positivesforplot, population)
        return file

    def getPopulation(herriname, data):
        for herripopulation in data['byDateByMunicipality'][0]['items']:
            if herripopulation['geoMunicipality']['officialName'] == herriname:
                return herripopulation['population']
        return -1

    def hezkuntza():
        min_positives = 1
        how_may_days_original = 6
        days = 0

        with urllib.request.urlopen("https://opendata.euskadi.eus/contenidos/ds_informes_estudios/covid_19_2020/opendata/generated/covid19-bymunicipality.json") as url:
            url_str = url.read().decode('unicode_escape').encode('utf-8')
            data = json.loads(url_str)
            lastUpdate = datetime.datetime.strftime(
                datetime.datetime.strptime(
                    data['lastUpdateDate'], '%Y-%m-%dT%H:%M:%SZ'),
                '%Y-%m-%d %H:%M'
            )
            print('Azken eguneraketa:', lastUpdate)
            herritot = 0
            datesforplot = []
            positivesforplot = []
            plotdata = {}
            for herri in data['newPositivesByDateByMunicipality'][len(data['newPositivesByDateByMunicipality']) - 1]['items']:
                herritot = 0
                how_may_days = how_may_days_original
                if 'geoMunicipality' in herri.keys():
                    herriname = herri['geoMunicipality']['officialName']
                    population = Korodata.getPopulation(herriname, data)
                    if population > 1200:
                        date = data['newPositivesByDateByMunicipality'][
                            len(data['newPositivesByDateByMunicipality']) - 1]['date']
                        while days <= how_may_days:
                            herrisum, datetoplot = Korodata.getHerriBefore(
                                herriname, date, how_may_days, data)
                            herritot += herrisum
                            how_may_days -= 1
                            per100 = 100000 * herritot / population
                        if per100 < 1000 and herritot > 0:
                            plotdata[herriname] = per100
                            print(herriname, herritot, population)
            plotdata = {k: v for k, v in sorted(
                plotdata.items(), key=lambda item: item[1])}
            positivesforplot = list(plotdata.values())
            datesforplot = list(plotdata.keys())
            print(datesforplot, positivesforplot)
            plt.figure(0, figsize=(30, 10))
            barlist = plt.bar(datesforplot, positivesforplot, width=0.6)
            bar = 0
            while bar < len(barlist):
                if positivesforplot[bar] < 7:
                    barlist[bar].set_color('green')
                    barlist[bar].set_hatch('')
                elif positivesforplot[bar] < 70:
                    barlist[bar].set_color('yellow')
                    barlist[bar].set_hatch('/')
                elif positivesforplot[bar] < 175:
                    barlist[bar].set_color('orange')
                    barlist[bar].set_hatch('//')
                else:
                    barlist[bar].set_color('red')
                    barlist[bar].set_hatch('X')
                barlist[bar].set_edgecolor('k')

                bar += 1
            handles = [mpatches.Patch(color='white')]
            handles.append(mpatches.Patch(
                facecolor='green', label='Eskola guztiak irekita', hatch='', edgecolor='k'))
            handles.append(mpatches.Patch(
                facecolor='yellow', hatch='/', edgecolor='k'))
            handles.append(mpatches.Patch(
                facecolor='orange', hatch='//', edgecolor='k'))
            handles.append(mpatches.Patch(
                facecolor='red', label='Etxean geratu, urrutiko irakaskuntza.', hatch='X', edgecolor='k'))
            leg = plt.legend(loc='upper left', handles=handles,
                             title="Datuen eragina hezkuntzan", labelspacing=1, title_fontsize=13, handlelength=4)
            for patch in leg.get_patches():
                patch.set_height(15)

            plt.xticks(rotation=45, ha="right")
            plt.title(
                "100.000 biztanleko positibo kopurua azken 7 egunak batuta", fontsize=26, pad=50)
            plt.tight_layout()
            plt.savefig('./korodata/grafikak/100.png')
            plt.close(plt.figure(0, figsize=(14, 8)))

    def gorriak():
        with urllib.request.urlopen("https://opendata.euskadi.eus/contenidos/ds_informes_estudios/covid_19_2020/opendata/generated/covid19-bymunicipality.json") as url:
            url_str = url.read().decode('unicode_escape').encode('utf-8')
            data = json.loads(url_str)
            herrilist = data['newPositivesByMunicipalityByDate']['positiveCountByMunicipalityByDate']
            emaitza = ''
            for herri in herrilist:
                herria = herri['dimension']['officialName']
                batura = sum(herri['values'][-14:])
                population = Korodata.getPopulation(herria, data)
                per100 = 100000 * batura / population
                if per100 > 500:
                    emaitza += str(herria) + ' -> ' + str(per100) + '\n'
            return emaitza
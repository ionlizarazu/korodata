from unidecode import unidecode

import datetime
import json
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import urllib.request
import io
import numpy as np


JSON_DATA_URL = "https://opendata.euskadi.eus/contenidos/ds_informes_estudios/covid_19_2020/opendata/generated/covid19-bymunicipality.json"


class Korodata:
    """docstring for ClassName"""

    def __init__(self):
        super(Korodata, self).__init__()

    def datetimeTodate(date, delta):
        return datetime.datetime.strftime(
            datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            - datetime.timedelta(days=delta),
            "%Y-%m-%d",
        )

    def draw_figure(
        j,
        herriname,
        datesforplot,
        positivesforplot,
        population=1,
        how_many_days=60,
    ):
        plt.figure(j, figsize=(14, 9))
        barlist = plt.bar(datesforplot, positivesforplot)
        Korodata.colorize_chart(barlist, positivesforplot, population)
        handles = [mpatches.Patch(color="white")]
        labels = ["Kalkulatu gabe", "< 60", "60 - 300", "300 - 400", ">= 400"]
        i = 0
        while i < len(Korodata.colors()):
            handles.append(
                mpatches.Patch(
                    facecolor=Korodata.colors()[i],
                    label=labels[i],
                    hatch=Korodata.hatches()[i],
                    edgecolor="k",
                )
            )
            i += 1
        leg = plt.legend(
            loc="upper left",
            handles=handles,
            title="Intzidentzia-tasa",
            labelspacing=1,
            title_fontsize=13,
            handlelength=4,
        )
        for patch in leg.get_patches():
            patch.set_height(15)
        for index, value in enumerate(positivesforplot):
            plt.text(index - 0.6, value * 1.01, str(value))
        hamalauEgun = positivesforplot[len(positivesforplot) - 14 :]
        per100 = 100000 * sum(hamalauEgun) / population
        plt.text(
            len(positivesforplot) * 0.20,
            max(positivesforplot) * -0.12,
            "Azken "
            + str(len(hamalauEgun))
            + " egunetan: Guztira "
            + str(sum(hamalauEgun))
            + " positibo | 100M biztanleko "
            + str(round(per100, 2)),
            fontsize=17,
        )
        plt.text(
            len(positivesforplot) * 0.1,
            max(positivesforplot) * 1.09,
            "COVID-19aren garapena azken "
            + str(how_many_days)
            + " egunetan. Kasuak eguneko eta intzidentzia-tasa.",
            fontsize=17,
        )
        plt.title(herriname, fontsize=26, pad=50)
        # plt.savefig('./static/charts/' + str(j).zfill(3) + 'figure.png')
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close(plt.figure(j, figsize=(14, 9)))
        return buf

    def set_color(i, color, colors_l, barlist):
        hatch = Korodata.hatches()[Korodata.colors().index(color)]
        barlist[i].set_hatch(hatch)
        barlist[i].set_color(color)
        barlist[i].set_edgecolor("k")
        colors_l[i] = color
        return colors_l

    def colors():
        color_list = ["grey", "greenyellow", "yellow", "orange", "red"]
        return color_list

    def hatches():
        hatch_list = ["", "/", "x", ".", "*"]
        return hatch_list

    def colorize_chart(barlist, values, population=1):
        colors = ["grey"] * len(barlist)
        i = 0
        if population > 5000:
            while i <= len(barlist):
                if i < 14:
                    colors = Korodata.set_color(i, "grey", colors, barlist)

                else:
                    min_range = i - 14
                    per100 = 100000 * sum(values[min_range:i]) / population
                    # print(values[min_range:i], sum(values[min_range:i]), per100)
                    if per100 < 60:
                        colors = Korodata.set_color(
                            i - 1, "greenyellow", colors, barlist
                        )
                    elif per100 < 300:
                        colors = Korodata.set_color(
                            i - 1, "yellow", colors, barlist
                        )
                    elif per100 < 400:
                        colors = Korodata.set_color(
                            i - 1, "orange", colors, barlist
                        )
                    else:
                        colors = Korodata.set_color(
                            i - 1, "red", colors, barlist
                        )
                i += 1
        else:
            while i < len(barlist):
                colors = Korodata.set_color(i, "grey", colors, barlist)
                i += 1

    def gaurko_informazioa_dauka():
        with urllib.request.urlopen(JSON_DATA_URL) as url:
            url_str = url.read().decode("unicode_escape").encode("utf-8")
            data = json.loads(url_str)
            today = datetime.datetime.strftime(
                datetime.datetime.now(), "%Y-%m-%d"
            )
            yesterday = Korodata.datetimeTodate(
                datetime.datetime.strftime(
                    datetime.datetime.now(), "%Y-%m-%dT%H:%M:%SZ"
                ),
                2,
            )
            lastUpdate = datetime.datetime.strftime(
                datetime.datetime.strptime(
                    data["lastUpdateDate"], "%Y-%m-%dT%H:%M:%SZ"
                ),
                "%Y-%m-%d %H:%M",
            )
            return (
                today in lastUpdate
                and yesterday
                in data["newPositivesByDateByMunicipality"][
                    len(data["newPositivesByDateByMunicipality"]) - 1
                ]["date"]
            )

    def azken_eguneraketa():
        with urllib.request.urlopen(JSON_DATA_URL) as url:
            url_str = url.read().decode("unicode_escape").encode("utf-8")
            data = json.loads(url_str)
            lastUpdate = datetime.datetime.strftime(
                datetime.datetime.strptime(
                    data["lastUpdateDate"], "%Y-%m-%dT%H:%M:%SZ"
                ),
                "%Y-%m-%d %H:%M",
            )
            return lastUpdate

    def herria(herri_izena, zenbat_egun=60):
        file = None
        with urllib.request.urlopen(JSON_DATA_URL) as url:
            i = 0
            url_str = url.read().decode("unicode_escape").encode("utf-8")
            data = json.loads(url_str)
            herri_zerrenda = data["newPositivesByMunicipalityByDate"][
                "positiveCountByMunicipalityByDate"
            ]
            for herria in herri_zerrenda:
                i += 1
                current_herri_izena = herria["dimension"]["officialName"]
                if herri_izena.lower() in current_herri_izena.lower():
                    positives = herria["values"][-zenbat_egun:]
                    dates = herria["dates"][-zenbat_egun:]
                    dates_to_return = [
                        datetime.datetime.strftime(
                            datetime.datetime.strptime(
                                date, "%Y-%m-%dT%H:%M:%SZ"
                            ),
                            "%m-%d",
                        )
                        for date in dates
                    ]
                    population = Korodata.get_populazioa(
                        current_herri_izena, data
                    )
                    file = Korodata.draw_figure(
                        i,
                        current_herri_izena,
                        dates_to_return,
                        positives,
                        population,
                        zenbat_egun,
                    )
                    return file, current_herri_izena
        return None, "Ez da herria aurkitu"

    def probintzia(kodea, zenbat_egun=60):
        switcher = {"01": "Araba", "48": "Bizkaia", "20": "Gipuzkoa"}
        probintzia_izena = switcher.get(kodea, "okerreko kodea")

        with urllib.request.urlopen(JSON_DATA_URL) as url:
            url_str = url.read().decode("unicode_escape").encode("utf-8")
            data = json.loads(url_str)
            probintzia_populazioa = 0
            positibo_zerrendak = []
            herri_zerrenda = data["newPositivesByMunicipalityByDate"][
                "positiveCountByMunicipalityByDate"
            ]
            for herria in herri_zerrenda:
                current_herri_probintzia_kodea = herria["dimension"][
                    "countyId"
                ]
                if kodea == current_herri_probintzia_kodea:
                    positibo_zerrendak.append(herria["values"][-zenbat_egun:])
                    probintzia_populazioa += Korodata.get_populazioa(
                        herria["dimension"]["officialName"], data
                    )

            positibo_zerrendak = np.array(positibo_zerrendak)
            positiboak = positibo_zerrendak.sum(axis=0)
            dates = herria["dates"][-zenbat_egun:]
            grafika_datak = [
                datetime.datetime.strftime(
                    datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ"),
                    "%m-%d",
                )
                for date in dates
            ]
            file = Korodata.draw_figure(
                1,
                probintzia_izena,
                grafika_datak,
                positiboak,
                probintzia_populazioa,
                zenbat_egun,
            )
        return file

    def eae(zenbat_egun=60):
        with urllib.request.urlopen(JSON_DATA_URL) as url:
            url_str = url.read().decode("unicode_escape").encode("utf-8")
            data = json.loads(url_str)
            eae_populazioa = 0
            positibo_zerrendak = []
            herri_zerrenda = data["newPositivesByMunicipalityByDate"][
                "positiveCountByMunicipalityByDate"
            ]
            for herria in herri_zerrenda:
                positibo_zerrendak.append(herria["values"][-zenbat_egun:])
                eae_populazioa += Korodata.get_populazioa(
                    herria["dimension"]["officialName"], data
                )
            positibo_zerrendak = np.array(positibo_zerrendak)
            positiboak = positibo_zerrendak.sum(axis=0)
            dates = herria["dates"][-zenbat_egun:]
            grafika_datak = [
                datetime.datetime.strftime(
                    datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ"),
                    "%m-%d",
                )
                for date in dates
            ]
            file = Korodata.draw_figure(
                1,
                "Euskal Autonomia Erkidegoa",
                grafika_datak,
                positiboak,
                eae_populazioa,
                zenbat_egun,
            )
        return file

    def get_populazioa(herri_izena, data):
        for herri_population in data["newPositivesByDateByMunicipality"][-1][
            "items"
        ]:
            if "geoMunicipality" in herri_population.keys():
                if (
                    herri_izena.lower()
                    in herri_population["geoMunicipality"][
                        "officialName"
                    ].lower()
                ):
                    return herri_population["population"]
        return -1

    def gorriak(muga):
        with urllib.request.urlopen(JSON_DATA_URL) as url:
            url_str = url.read().decode("unicode_escape").encode("utf-8")
            data = json.loads(url_str)
            herrilist = data["newPositivesByMunicipalityByDate"][
                "positiveCountByMunicipalityByDate"
            ]
            emaitza = ""
            araba = "*Araba*\n"
            bizkaia = "*Bizkaia*\n"
            gipuzkoa = "*Gipuzkoa*\n"
            for herri in herrilist:
                herria = herri["dimension"]["officialName"]
                batura = sum(herri["values"][-14:])
                populazioa = Korodata.get_populazioa(
                    herria, data
                )
                per100 = round(100000 * batura / populazioa, 2)
                if per100 > muga:
                    if "01" == herri["dimension"]["countyId"]:
                        araba += str(herria) + " -> " + str(per100) + "\n"
                    if "48" == herri["dimension"]["countyId"]:
                        bizkaia += str(herria) + " -> " + str(per100) + "\n"
                    if "20" == herri["dimension"]["countyId"]:
                        gipuzkoa += str(herria) + " -> " + str(per100) + "\n"
                emaitza = araba + "\n" + bizkaia + "\n" + gipuzkoa

            return emaitza

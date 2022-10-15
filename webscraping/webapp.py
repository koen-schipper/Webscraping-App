from django.shortcuts import render
from bs4 import BeautifulSoup
import requests

def button(request):
    return render(request,'webscraping.html')

def verhelst(request):
    if request.method == 'POST':
        if request.method == 'POST':
            form = request.POST
            try:
                source = requests.get(form['verhelst_url'])
                source.raise_for_status()
                soup = BeautifulSoup(source.text, "html.parser")

                kenmerken = ['<div style="page-break-inside:avoid;">']

                sections = soup.find("div", class_="tabs-content").find_all("section")

                for section in sections:
                    if section.get("id") == "general":
                        kenmerken.append("<h3 class='object-kenmerken-list-header'>Algemeen</h3>")
                    elif section.get("id") == "division":
                        kenmerken.append("<h3 class='object-kenmerken-list-header'>Indeling</h3>")
                    elif section.get("id") == "comfort":
                        kenmerken.append("<h3 class='object-kenmerken-list-header'>Comfort</h3>")
                    elif section.get("id") == "legal":
                        kenmerken.append(
                            "<h3 class='object-kenmerken-list-header'>Wettelijke gegevens</h3>"
                        )
                    else:
                        kenmerken.append("")

                    kenmerken.append(
                        '<table class="kenmerkentabel table-sm table" autosize="1" width="100%"><tbody>'
                    )

                    tables = section.find_all("table")
                    for table in tables:
                        trs = table.find_all("tr")
                        for tr in trs:
                            tdlabel = tr.find("td", class_="kenmerklabel").text
                            tdname = tr.find("td", class_="kenmerk").text

                            if (
                                tdlabel != "Adres:"
                                and tdlabel != "Referentie:"
                                and tdlabel != "Vraagprijs:"
                            ):
                                kenmerken.append(
                                    '<tr class="kenmerkenrow"><td class="kenmerkenkey w-50" width="50%">'
                                    + tdlabel
                                    + '</td><td class="kenmerkenValue w-50" width="50%">'
                                    + tdname
                                    + "</td></tr>"
                                )

                    kenmerken.append("</tbody></table>")
                unformatted_output = str("".join(kenmerken))
                output_data = BeautifulSoup(unformatted_output).prettify()

            except Exception as e:
                print(e)
    return render(request,"webscraping.html",{"output_data":output_data})

def century(request):
    if request.method == 'POST':
        form = request.POST
            
        try:
            source = requests.get(form['century21_url'])
            source.raise_for_status()
            soup = BeautifulSoup(source.text, "html.parser")

            kenmerken = ['<div style="page-break-inside:avoid;">']

            groups = soup.find("div", class_="group-container").find_all("div", class_="group")

            for group in groups:
                groupTitle = group.find("div", class_="caption")

                if (
                    groupTitle.a.get("href") != "#financial-info"
                    and groupTitle.a.get("href") == "#peb-info"
                ):
                    kenmerken.append(
                        "<h3 class='object-kenmerken-list-header'>"
                        + groupTitle.a.text
                        + "</h3>"
                    )

                    kenmerken.append(
                        '<table class="kenmerkentabel table-sm table" autosize="1" width="100%"><tbody>'
                    )

                    fields = group.find_all("div", class_="field")

                    kenmerken.append(
                        '<tr class="kenmerkenrow"><td class="kenmerkenkey w-50" width="50%">EPC No.</td><td class="kenmerkenValue w-50" width="50%">'
                        + fields[0].text
                        + "</td></tr>"
                    )

                    epcName = fields[1].find("div", class_="name").text
                    epcValue = fields[1].find("div", class_="value").text

                    kenmerken.append(
                        '<tr class="kenmerkenrow"><td class="kenmerkenkey w-50" width="50%">'
                        + epcName
                        + '</td><td class="kenmerkenValue w-50" width="50%">'
                        + epcValue
                        + "</td></tr>"
                    )

                    kenmerken.append("</tbody></table>")
                elif groupTitle.a.get("href") != "#financial-info":
                    kenmerken.append(
                        "<h3 class='object-kenmerken-list-header'>"
                        + groupTitle.a.text
                        + "</h3>"
                    )

                    kenmerken.append(
                        '<table class="kenmerkentabel table-sm table" autosize="1" width="100%"><tbody>'
                    )

                    fields = group.find_all("div", class_="field")

                    for field in fields:
                        tdlabel = field.find("div", class_="name").text
                        tdname = field.find("div", class_="value").text

                        if tdlabel != "Prijs" and tdlabel != "Adres":
                            kenmerken.append(
                                '<tr class="kenmerkenrow"><td class="kenmerkenkey w-50" width="50%">'
                                + tdlabel
                                + '</td><td class="kenmerkenValue w-50" width="50%">'
                                + tdname
                                + "</td></tr>"
                            )

                    kenmerken.append("</tbody></table>")
                    
            unformatted_output = str("".join(kenmerken))
            output_data = BeautifulSoup(unformatted_output).prettify()

        except Exception as e:
            print(e)
            
    return render(request,"webscraping.html",{"output_data":output_data})
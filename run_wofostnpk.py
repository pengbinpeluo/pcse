from __future__ import print_function
import sys
import os
import csv
import datetime as dt
import pcse
from pcse.engine import Engine
from pcse.base_classes import ParameterProvider, MultiCropParameterProvider
from agromanager import AgroManager
import yaml

start_day = dt.date(1976,1,1)

def write_CSV(outfile, data):

    rows = [d for d in data if d is not None]
    with open(outfile, 'wb') as fp:
        firstrow = rows[0]
        writer = csv.DictWriter(fp, sorted(firstrow.keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
def main():
    agromanagement = yaml.load(open('wofost_npk.amgt'))['AgroManagement']

    soil = pcse.fileinput.CABOFileReader('ec4.soil')
    crop = {'winter-wheat': pcse.fileinput.CABOFileReader('wwh102.crop')}
    site = pcse.fileinput.CABOFileReader('manage.data')
    weather = pcse.fileinput.CABOWeatherDataProvider('NL1', fpath=r"D:\UserData\WOFOST Control Centre\METEO\CABOWE")
    parvalues = MultiCropParameterProvider(sitedata=site, soildata=soil, multi_cropdata=crop)
    pw = Engine(parvalues,  weather, agromanagement=agromanagement, config="Wofost71_NPK.conf")
    pw.run(days=300)
    r = pw.get_output()
    print("TAGP should be 4608.467 = %8.3f" % r[-1]["TAGP"])
    print("TWSO should be 1014.083 = %8.3f" % r[-1]["TWSO"])
    print("TWST should be 2678.155 = %8.3f" % r[-1]["TWST"])

    write_CSV("NPK_reference_results_B.csv", pw._saved_output)

if __name__ == '__main__':
        main()
import os
import csv
import sys
from Myfinance.settings import MEDIA_ROOT

def data_export(model):
    data = model.objects.all().values()
    keys = sorted(data[0].keys())
    path = os.path.join(MEDIA_ROOT, '%s.csv' % model.__name__)
    with open(path, 'w') as csvfile:
        try:
            writer = csv.DictWriter(csvfile, keys, delimiter="\t")
            writer.writeheader()
            writer.writerows(data)
            answer = True
        except Exception:
            answer = str(sys.exc_info())
        csvfile.close()
    return answer
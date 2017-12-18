import os

file_path = '../dist2coast.signed.txt'

with open(file_path, 'r') as in_f: 
    lat = int(list(map(float, in_f.readline().split('\t')))[1])
    out_f = open('../land_latitudes/{}.csv'.format(lat), 'w')
    out_f.write('LNG\tLAT\tDISTANCE\n')
    in_f.seek(0, 0)
    for row in in_f:
        cur_line = list(map(float, row.split('\t')))
        if int(cur_line[1]) == lat:
            if cur_line[2] < 0:
                out_f.write(row)
        else:
            out_f.close()
            lat = int(cur_line[1])
            out_f = open('../land_latitudes/{}.csv'.format(lat), 'w')
            out_f.write('LNG\tLAT\tDISTANCE\n')
            out_f.write(row)
    out_f.close()

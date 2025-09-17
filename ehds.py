import serial
import csv
import time


SERIAL_PORT = 'COM3' # or '/dev/ttyUSB0'
BAUD = 115200
OUTFILE = 'harvest_log.csv'


def parse_line(line):
line = line.strip()
if line.startswith('STATUS'):
# STATUS,<ms>,V=<voltage>,hits=<n>
parts = line.split(',')
ms = parts[1]
v = float(parts[2].split('=')[1])
hits = int(parts[3].split('=')[1])
return ('STATUS', int(ms), v, hits)
elif line.startswith('HIT'):
parts = line.split(',')
ms = int(parts[1])
return ('HIT', ms)
else:
return None
if __name__ == '__main__':
ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)
time.sleep(2)
with open(OUTFILE, 'w', newline='') as csvfile:
writer = csv.writer(csvfile)
writer.writerow(['type','ms','voltage','hits'])
while True:
raw = ser.readline().decode('utf-8', errors='ignore').strip()
if not raw:
continue
parsed = parse_line(raw)
if not parsed:
print('?', raw)
continue
if parsed[0] == 'STATUS':
_, ms, v, hits = parsed
writer.writerow(['STATUS', ms, v, hits])
csvfile.flush()
print('LOG', ms, v, hits)
elif parsed[0] == 'HIT':
_, ms = parsed
writer.writerow(['HIT', ms, '', ''])
csvfile.flush()
print('HIT', ms)

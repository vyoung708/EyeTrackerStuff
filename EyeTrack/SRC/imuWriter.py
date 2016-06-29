import serial
import time

def get_time_in_ms():
    time_value = time.time()
    return int(np.round(time.time()*1000))

serialPort = serial.Serial(
    port='/dev/tty.SLAB_USBtoUART',
    baudrate=115200)

out_file = open('imu-'+str(get_time_in_ms())+".log",'w')

while True:
    line = serialPort.readline()
    try:
        line = line.decode('utf-8')
    except UnicodeDecodeError:
        continue
    print(line)
    line = line.replace('\n\r','')
    line = line.replace('\r\n', '')
    out_file.write(str(get_time_in_ms())+" "+line+"\n")
    out_file.flush()
    continue
    splt = line.split(' ')
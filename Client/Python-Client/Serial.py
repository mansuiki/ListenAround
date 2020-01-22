import time

import serial
import socketio


def send_command(serial_port, cmd_msg):
    cmd_msg = '@' + cmd_msg.strip()
    crc = 0
    for c in cmd_msg:
        crc = crc ^ ord(c)
    serial_port.write((cmd_msg + '*%02X' % crc + '\r\n').encode())

    #
    # wait for response
    #
    if cmd_msg != '@trig':
        while True:
            line = serial_port.readline().strip()
            ld = line.decode('utf-8')
            print(ld)
            if ld[0] == '~':
                return line


def parse_data_message(data_message, mode):
    if mode is 'rpyimu':
        # $RPYIMU,39,0.42,-0.31,-26.51,-0.0049,-0.0038,-1.0103,-0.0101,0.0014,-0.4001,51.9000,26.7000,11.7000,41.5*1F

        data_message = data_message.decode('utf-8')
        data_message = (data_message.split('*')[0]).strip()  # discard crc field
        fields = [x.strip() for x in data_message.split(',')]

        if fields[0] != '$RPYIMU':
            return None

        sequence_number, roll, pitch, yaw, accelx, accely, accelz, gyrox, gyroy, gyroz, magnetx, magnety, magnetz, temperature = (
            float(x) for x in fields[1:])
        return (
            int(sequence_number),
            roll, pitch, yaw, accelx, accely, accelz, gyrox, gyroy, gyroz, magnetx, magnety, magnetz,
            temperature)

    elif mode is 'quatimu':
        # $QUATIMU,30,-0.1417,-0.0503,0.6582,0.7377,0.0863,0.2696,-0.8973,-0.3619,0.4495,-0.1696,13.8000,11.1000,-95.1000,42.1*78

        data_message = data_message.decode('utf-8')
        data_message = (data_message.split('*')[0]).strip()  # discard crc field
        fields = [x.strip() for x in data_message.split(',')]

        if fields[0] != '$QUATIMU':
            return None

        sequence_number, x, y, z, w, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, magnet_x, magnet_y, magnet_z, temperature = (
            float(x) for x in fields[1:])
        return (
            int(sequence_number), x, y, z, w, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, magnet_x, magnet_y,
            magnet_z, temperature)


def read_example(serial_device, server_url):
    sock = socketio.Client()
    sock.connect(server_url)

    print('START TEST(%s)' % serial_device)

    serial_port = serial.Serial(serial_device, 115200, timeout=1.0)

    #
    # Get version
    #
    rsp = send_command(serial_port, 'version')

    rsp = send_command(serial_port, 'divider,5')

    #
    # Data transfer mode : ASCII, TRIGGER
    #
    rsp = send_command(serial_port, 'mode,AC')
    print(rsp)

    #
    # Select output message type
    #
    rsp = send_command(serial_port, 'asc_out,RPYIMU')
    print(rsp)
    save = []

    while True:
        time.sleep(0.01) #0/01
        #
        # send trigger command
        #
        # send_command(serial_port, 'trig')

        #
        # wait for data message
        #
        line = serial_port.readline().strip()
        # print('DATA MESSAGE : <%s>' % line)

        #
        # parse data message
        #
        items = parse_data_message(line, 'rpyimu')

        #
        # display output
        #
        if items:
            # sequence_number, x, y, z, w, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, magnet_x, magnet_y, magnet_z, temperature = items
            sequence_number, roll, pitch, yaw, accelx, accely, accelz, gyrox, gyroy, gyroz, magnetx, magnety, magnetz, temperature = items

            # if (x or y or z or w or accel_x or accel_y or accel_z) is np.nan:
            #    continue

            # if (roll or pitch or yaw or accelx or accely or accelz) is np.nan:
            #    continue

            # print('#### x:%f y:%f z:%f w:%f accx:%f accy:%f accz:%f \n' % (x, y, z, w, accel_x, accel_y, accel_z))
            print(':::: magnetx::%f, magnety::%f, magnetz::%f' % (magnetx, magnety, magnetz))
            print(':::: roll :: %f, pitch :: %f, yaw :: %f' % (roll, pitch, yaw))

            # sock.emit("putq", [{'x': x, 'y': y, 'z': z, 'w': w}, {'x': accel_x, 'y': accel_y+1, 'z': accel_z}])
            # sock.emit("putq", [{'x': roll, 'y': pitch, 'z': yaw, 'w': 0}, {'x': accelx, 'y': accely + 1, 'z': accelz}])
            sock.emit("putq", [str(roll), str(pitch), str(yaw), magnetx, magnetz])

            # save.append([{'x': x, 'y': y, 'z': z, 'w': w}, {'x': accel_x, 'y': accel_y, 'z': accel_z}])

    sock.disconnect()
    serial_port.close()

    print('END OF TEST')


if __name__ == '__main__':
    serial_device = '/dev/tty.usbmodem0000010100001'
    read_example(serial_device, 'http://192.168.43.187:33333')
6
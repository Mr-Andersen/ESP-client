#!/usr/bin/env python3

import pyqtgraph as pg
import time
import struct

from lib import TigraClient


if __name__ == '__main__':
    conn = TigraClient('http://192.168.13.37/')
    win = pg.GraphicsWindow(title=conn.root)
    plot = win.addPlot()
    plot.setXRange(0, 200)
    plot.setYRange(-100, 350)
    delta_times = []

    curveX = plot.plot(pen='r')
    curveY = plot.plot(pen='g')
    curveZ = plot.plot(pen='y')

    dataX = []
    dataY = []
    dataZ = []

    def update():
        now_time = start_time = time.time()
        net_error = False
        while True:
            try:
                got = conn.device('Acc')
            except Exception:
                if not net_error:
                    print('Network error!', end='')
                else:
                    print('.', end='')
                    time.sleep(1)
                net_error = True
                continue
            if net_error:
                print()
                net_error = False
            if got['ok']:
                prev_time = now_time
                now_time = time.time()

                valueX = struct.unpack('h', bytes(got['X']['value']))[0]
                dataX.append((now_time - start_time, valueX))

                valueY = struct.unpack('h', bytes(got['Y']['value']))[0]
                dataY.append((now_time - start_time, valueY))

                valueZ = struct.unpack('h', bytes(got['Z']['value']))[0]
                dataZ.append((now_time - start_time, valueZ))

                curveX.setData(*zip(*dataX))
                curveY.setData(*zip(*dataY))
                curveZ.setData(*zip(*dataZ))

                delta_times.append(now_time - prev_time)
            else:
                print(f'Error in answer: {got}')

    thread = pg.QtCore.QThread()
    thread.run = update
    thread.start()

    pg.QtGui.QApplication.instance().exec_()

    print('Time between reads:')
    print(f'  aver = {sum(delta_times) / len(delta_times)}s')
    print(f'  min = {min(delta_times)}s')
    print(f'  max = {max(delta_times)}s')

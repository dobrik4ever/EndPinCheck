from scanner.scanner import Scanner
import numpy as np
scanner = Scanner()
scanner.start()
input('GO?')
scanner.arduino.send('HTEST 50')
vals = []
while True:
    scanner.arduino.puk.wait()
    scanner.arduino.puk.clear()
    data = scanner.arduino.serialInput
    if data == 'vse':
        break
    try:
        data = int(data)
        print(data)
        vals.append(data)
    except:
        pass
dev = np.std(vals)
print(f'Standard deviation is: {dev}')
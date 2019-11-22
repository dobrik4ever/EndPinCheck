from scanner.scanner import Scanner
import numpy as np
import matplotlib.pyplot as plt

scanner = Scanner()
scanner.start()
input('GO?')
scanner.arduino.send('HTEST 50')
vals = []
i = 0
while True:
    scanner.arduino.puk.wait()
    scanner.arduino.puk.clear()
    data = scanner.arduino.serialInput
    if data == 'vse':
        break
    try:
        print(f'{i}: {data}')
        Data = int(data)
        vals.append(Data)
    except:
        print('Wow, trouble!')
        pass

plt.scatter(range(len(vals)),vals)
dev = np.std(vals)
print(f'Standard deviation is: {dev}')
# scanner.arduino.terminate()
plt.show()
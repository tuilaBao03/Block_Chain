from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from random import randint
from jechain import Blockchain,Transaction
from ecdsa import SigningKey, SECP256k1, VerifyingKey # hàm 

# đây là node người nhân tiền
# tạo khóa cho node
ec = SECP256k1
from ecdsa import SigningKey, SECP256k1
# Khởi tạo một Blockchain mới
# Tạo một cặp khóa cho người dùng Công
congw = SigningKey.generate(curve=SECP256k1)
congW_public = congw.get_verifying_key().to_string().hex()
print(congW_public)


class Peer(DatagramProtocol):   
    def __init__(self, host, port,public_key):
        if host == "localhost": 
            host = "127.0.0.1"
        self.local_address = host, port  # Địa chỉ local của peer này
        self.server = '127.0.0.1', 9999  # Địa chỉ của Directory Server
        self.remote_address = None  # Địa chỉ của peer mà bạn muốn kết nối đến
        self.public_key = public_key # địa chỉ public key để dùng
        print("Máy đang hoạt động trên địa chỉ: ", self.local_address)
        print("Node có địa chỉ công khai là : ", self.public_key)
        

    def startProtocol(self):
        self.transport.write("sẵn sàng".encode('utf-8'), self.server)
    
    def datagramReceived(self, datagram, addr): 
        holder_public = ""
        mini_public_address = ""
        datagram = datagram.decode('utf-8') # Convert received data to string
        if addr == self.server:
            # Directory server message handling
            print("Chọn Peer để trò chuyện từ danh sách sau:\n", datagram)
            host = "127.0.0.1"
            port = int(input("Nhập port: "))
            self.remote_address = host, port  # Update remote address 
            reactor.callInThread(self.send_message)
        else:
            if 'diachinsh' in datagram and 'diachinguon' in datagram:
                holder_public = datagram[9:137]
                print("Holder public address:", holder_public)
                mini_public_address = datagram[146:274]
                print("Mini public address:", mini_public_address)
                # Create a blockchain instance
                node = Blockchain(mini_public_address, holder_public)
                balance = node.get_balance(holder_public)
                print("Balance:", balance)
            elif 'chuyentien' in datagram:
                holder_public = datagram[10:(128+10)]
                transaction = Transaction(
                        holder_public,
                        congW_public,
                        1)
                transaction.is_valid()
                
                    
                
            
            else:
                if(len(datagram)>0):
                    print("da nhan")
                    print(":::", datagram)
                
        

    def send_message(self): 
        while True:
            message = input("::: ")
            print(message)
            if message.lower() == 'exit':
                self.transport.write("Mất kết nối".encode('utf-8'), self.remote_address)
                self.transport.write('exit'.encode('utf-8'), self.server)
                reactor.stop()
                break
            if message.lower() == 'ccdc': # cung cap dai chi public cua cong
                canchuyen = "diachicuavinguoicanchuyen"+congW_public # 25+128
                self.transport.write(canchuyen.encode('utf-8'), self.remote_address)
                print("da gui dia chi")
            else:
                
                self.transport.write(message.encode('utf-8'), self.remote_address)
                print("da gui")

if __name__ == '__main__':
    port = randint(1000,5000)
    reactor.listenUDP(port, Peer('localhost', port,congW_public))
    reactor.run()

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from random import randint
from jechain import Blockchain
from jechain import Transaction
import time
from ecdsa import SigningKey, SECP256k1, VerifyingKey # hàm 

# đây là node chủ sở hữu

# tạo khóa cho node 
ec = SECP256k1
from ecdsa import SigningKey, SECP256k1
keyPair = SigningKey.generate(curve=ec)

holderKeyPair = SigningKey.generate(curve=ec)
holder_public = holderKeyPair.get_verifying_key().to_string().hex() # chuyển đầu tiên

ec = SECP256k1

# # Tạo một cặp khóa mới cho việc phát hành tiền
MINT_KEY_PAIR = SigningKey.generate(curve=ec)
MINT_PUBLIC_ADDRESS = MINT_KEY_PAIR.get_verifying_key().to_string().hex() # chuyển đầu tiên
print("mint_public: "+MINT_PUBLIC_ADDRESS)

class Peer(DatagramProtocol):   
    def __init__(self, host, port,public_key):
        if host == "localhost": 
            host = "127.0.0.1"
        self.local_address = host, port  # Địa chỉ local của peer này
        self.server = '127.0.0.1', 9999  # Địa chỉ của Directory Server
        self.remote_address = None  # Địa chỉ của peer mà bạn muốn kết nối đến
        self.public_key = public_key # địa chỉ public key để dùng
        print("Máy đang hoạt động trên địa chỉ: ", self.local_address)
        #print("Node có địa chỉ công khai là : ", self.public_key)
        #khai báo blockchain 
        self.node = Blockchain(MINT_PUBLIC_ADDRESS,holder_public)
        #print("Số dư của bạn: ", self.node.get_balance(holder_public))
    def startProtocol(self):
        self.transport.write("sẵn sàng".encode('utf-8'), self.server)

    def datagramReceived(self, datagram, addr): 
        datagram = datagram.decode('utf-8') # thông tin nhận được 
        if addr == self.server:
            print(" Chọn Peer để trò chuyện từ danh sách sau:\n", datagram)
            host = "127.0.0.1"
            port = int(input("Nhập port: "))
            self.remote_address = host, port  # Cập nhật địa chỉ remote 
            reactor.callInThread(self.send_message)
            
        else: 
            if('diachicuavinguoicanchuyen' in datagram): # nhận địa chỉ của công để tạo transaction chuyển tiền 
                cong_public = datagram[26:(128+26)]
                start_time = time.time()
                for i in range(100):

                    print("chuyen")
                    transaction = Transaction(
                            holder_public,
                            cong_public,
                            1
                    )
                    transaction.sign(holderKeyPair)
                    print("chuyen lan "+str(i))
                    # Thêm giao dịch vào Blockchain
                    self.node.add_transaction(transaction,MINT_PUBLIC_ADDRESS)
                    # Khai thác giao dịch bằng địa chỉ của Công
                    self.node.mine_transactions(cong_public,MINT_KEY_PAIR)
                    cangui = "chuyentien"+holder_public
                    self.transport.write(cangui.encode('utf-8'), self.remote_address)
                    # In số dư của các tài khoản liên quan
                    print("Số dư của bạn: ", self.node.get_balance(holder_public))
                end_time = time.time()
                print("Số dư của bạn: ", self.node.get_balance(holder_public))
                print("thời gian : "+str(end_time-start_time))
                

                    


            else: 
                print(addr, ":", datagram)

    def send_message(self): 
        # sotienchuyen = "";
        # self.transport.write(sotienchuyen.encode('utf-8'), self.remote_address)
        # xacnhanchuyen_nhantien = key_pair
        # self.transport.write(xacnhanchuyen_nhantien.encode('utf-8'),self.remote_address)
        
       
        while True: 
        # gửi địa chủ nguồn và địa chỉ chủ sở hữu đầu tiên để phục vụ lần phát hành coin
        # ứng với mỗi node lần đầu connection thì node chủ sẽ gửi địa chủ public của nó và địa chỉ public của nguồn phát hành để khởi tạo blockchain
            print("khởi tạo nút khởi nguyên:( Y/n ):::")
            message = input("chuyển ::: ")
            if message.lower()=='y':
                # tạo 1 tin nhắn gồm 2 khóa 
                cangui = "diachinsh"+holder_public+"diachinguon"+MINT_PUBLIC_ADDRESS 
                self.transport.write(cangui.encode('utf-8'), self.remote_address)
            elif message.lower()=='chuyentien':
                cangui = ""

            else:
                
                if message.lower() == 'exit':
                    self.transport.write("Mất kết nối".encode('utf-8'), self.remote_address)
                    self.transport.write('exit'.encode('utf-8'), self.server)
                    reactor.stop()
                    break
                else:
                    
                    self.transport.write(message.encode('utf-8'), self.remote_address)
                    print("da chuyen ")
                
    
            

            
if __name__ == '__main__':
    port = randint(1000,5000)
    reactor.listenUDP(port, Peer('localhost', port,holder_public))
    reactor.run()
    
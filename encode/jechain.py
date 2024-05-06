import hashlib # import hàm băm
import json # import json
from ecdsa import SigningKey, SECP256k1, VerifyingKey # hàm 

def SHA256(message):
    return hashlib.sha256(message.encode()).hexdigest()

# # Khởi tạo curve elliptic là secp256k1
# ec = SECP256k1

# # # Tạo một cặp khóa mới cho việc phát hành tiền
# MINT_KEY_PAIR = SigningKey.generate(curve=ec)

# MINT_PUBLIC_ADDRESS = MINT_KEY_PAIR.get_verifying_key().to_string().hex()
# print("mint_public: "+MINT_PUBLIC_ADDRESS)
# # Tạo cặp khóa bổ sung
# keyPair = SigningKey.generate(curve=ec)
# holderKeyPair = SigningKey.generate(curve=ec)
# holderKeyPair_address = holderKeyPair.get_verifying_key().to_string().hex()

class Block:
    def __init__(self, timestamp="", data=[]):
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = "" # mã băm của khối liền trước
        self.nonce = 0 # Đây là một số nguyên không âm được sử dụng trong quá trình khai thác khối. Nó được tăng dần cho đến khi một mã hash thỏa mãn điều kiện độ khó được đặt ra
        self.hash = self.calculate_hash() # mã băm của khối

    # def current_time(self): 
    #     from datetime import datetime
    #     return datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    # Hàm calculate_hash trong lớp Block được sử dụng để tính toán mã băm của khối dựa trên các thông tin của khối, bao gồm:
    # prev_hash: Mã băm của khối trước đó trong chuỗi.
    # timestamp: Thời điểm tạo khối.
    # data: Dữ liệu của khối, được chuyển đổi thành một chuỗi JSON và sắp xếp các keys để đảm bảo tính nhất quán.
    # nonce: Giá trị nonce được sử dụng trong quá trình khai thác khối.
    def calculate_hash(self):
        return SHA256(self.prev_hash + self.timestamp + json.dumps(self.data, sort_keys=True) + str(self.nonce))

    def mine(self, difficulty):
        assert difficulty >= 0, "Difficulty should be non-negative"
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

    def has_valid_transactions(self, chain):
        return all(transaction.is_valid(transaction, chain) for transaction in self.data)   
from datetime import datetime

class Blockchain:
    def __init__(self,mint_pulic_address,holderKeyPair_address):
        from_address = mint_pulic_address
        to_address = holderKeyPair_address
        
        phathanhcoin = Transaction(from_address, to_address, 10)
        self.chain = [Block(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), [phathanhcoin.__dict__])]
        self.difficulty = 1
        self.blockTime = 30000
        self.transactions = []
        self.reward = 100

    def get_last_block(self):
        return self.chain[-1]

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.data:
                if transaction['from_address'] == address:
                    balance -= transaction['amount']
                if transaction['to'] == address:
                    balance += transaction['amount']
        return balance

    def add_block(self, block):
        block.prev_hash = self.get_last_block().hash
        block.mine(self.difficulty)
        self.chain.append(block)
        # Adjust difficulty based on the time spent mining the block
        current_time = datetime.now().timestamp()
        last_block_time = datetime.strptime(self.get_last_block().timestamp, "%m/%d/%Y, %H:%M:%S").timestamp()
        if current_time - last_block_time < self.blockTime:
            self.difficulty += 0
        else:
            self.difficulty -= 0

    def add_transaction(self, transaction,mini_public_address):
        if transaction.is_valid(transaction, self,mini_public_address):
            self.transactions.append(transaction)

    def mine_transactions(self, reward_address,mini_key_pair):
        reward_transaction = Transaction(mini_key_pair.get_verifying_key().to_string().hex(), reward_address, self.reward)
        reward_transaction.sign(mini_key_pair)
        new_block = Block(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), [reward_transaction.__dict__] + [tx.__dict__ for tx in self.transactions])
        self.add_block(new_block)
        self.transactions = []

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash() or \
               prev_block.hash != current_block.prev_hash or \
               not current_block.has_valid_transactions(self):
                return False
        return True
import time
class Transaction:
    def __init__(self, from_address, to, amount):
        time.sleep(0.003)
        self.from_address = from_address
        self.to = to
        self.amount = amount
        self.signature = None

    def sign(self, key_pair):
        if key_pair.get_verifying_key().to_string().hex() == self.from_address:
            # Chữ ký được tạo ở định dạng DER và chuyển sang hex
            self.signature = key_pair.sign(SHA256(self.from_address + self.to + str(self.amount)).encode()).hex()
        return self.signature
            
    def is_valid(self, tx, chain,mini_public_address):
        if not tx.from_address or not tx.to or tx.amount <= 0:
            return False
        if tx.from_address == mini_public_address or chain.get_balance(tx.from_address) >= tx.amount:
            verifying_key = VerifyingKey.from_string(bytes.fromhex(tx.from_address), curve=SECP256k1)
            # Verify the signature
            return verifying_key.verify(bytes.fromhex(tx.signature), SHA256(tx.from_address + tx.to + str(tx.amount)).encode())
        return False
from ecdsa import SigningKey, SECP256k1

# # Khởi tạo một Blockchain mới
# jechain = Blockchain(MINT_PUBLIC_ADDRESS,holderKeyPair)

# # Tạo một cặp khóa cho người dùng Công
# congw = SigningKey.generate(curve=SECP256k1)
# print(congw.get_verifying_key().to_string().hex())

# # Tạo một giao dịch mới
# transaction = Transaction(
#     holderKeyPair.get_verifying_key().to_string().hex(),
#     congw.get_verifying_key().to_string().hex(),
#     333
# )
# transaction.sign(holderKeyPair)

# # Thêm giao dịch vào Blockchain
# jechain.add_transaction(transaction,MINT_PUBLIC_ADDRESS)

# # Khai thác giao dịch bằng địa chỉ của Công
# jechain.mine_transactions(congw.get_verifying_key().to_string().hex(),MINT_KEY_PAIR)

# # In số dư của các tài khoản liên quan
# print("Số dư của bạn: ", jechain.get_balance(holderKeyPair.get_verifying_key().to_string().hex()))
# print("Số dư của Công: ", jechain.get_balance(congw.get_verifying_key().to_string().hex()))


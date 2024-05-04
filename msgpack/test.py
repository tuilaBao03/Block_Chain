import hashlib # import hàm băm
import json # import json
from ecdsa import SigningKey, SECP256k1, VerifyingKey # hàm 
ec = SECP256k1
import msgpack
MINT_KEY_PAIR = SigningKey.generate(curve=ec)
MINT_PUBLIC_ADDRESS = MINT_KEY_PAIR.get_verifying_key().to_string().hex() # chuyển đầu tiên
a = "chuyentien"+MINT_PUBLIC_ADDRESS
print("mint_public: "+a)
print(len("chuyentien"))
print(len(MINT_PUBLIC_ADDRESS))
print(a[10:(128+10)])


# Serialize data to MessagePack format
packed_data = msgpack.packb(a)

# Send packed_data over the network

# On the receiving end, unpack the data
unpacked_data = msgpack.unpackb(packed_data)

# Now unpacked_data is the original data
print(unpacked_data)
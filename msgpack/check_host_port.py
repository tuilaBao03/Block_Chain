import socket  # Nhập thư viện socket để làm việc với các kết nối mạng

def get_unused_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET chỉ định sử dụng IPv4. SOCK_STREAM chỉ định sử dụng TCP.
    s.bind(('localhost', 0)) 
    address, port = s.getsockname()  
    s.close()  # Đóng socket, giải phóng tài nguyên
    return address, port  # Trả về địa chỉ IP và port

if __name__ == "__main__":
    host_ip = socket.gethostbyname(socket.gethostname())  # Lấy địa chỉ IP của máy chủ dựa vào tên máy chủ
    unused_port = get_unused_port()[1]  # Gọi hàm get_unused_port để lấy port chưa được sử dụng và lấy phần tử thứ hai (port)
    print("Host IP của bạn là:", host_ip)  
    print("Port chưa được sử dụng:", unused_port) 

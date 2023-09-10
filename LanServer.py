import tkinter as tk
from tkinter import filedialog
import http.server
import socketserver
import threading
import socket

class LANServerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LAN Server")
        self.root.geometry("420x230")  # 设置窗口大小
        
        self.selected_file = tk.StringVar()
        self.selected_file.set("index.html")
        
        self.label = tk.Label(root, text="Select a file to serve:")
        self.label.pack()
        
        self.file_entry = tk.Entry(root, textvariable=self.selected_file, width=40)
        self.file_entry.pack()
        
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack()
        
        self.start_button = tk.Button(root, text="Start Server", command=self.start_server)
        self.start_button.pack()
        
        self.stop_button = tk.Button(root, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack()
        
        self.status_label = tk.Label(root, text="Server is off")
        self.status_label.pack()
        
        self.server_thread = None  # 存储服务器线程的引用
        self.httpd = None  # 存储HTTP服务器实例
        
    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file.set(file_path)
            
    def start_server(self):
        selected_file = self.selected_file.get()
        
        # 创建一个新线程来运行服务器
        self.server_thread = threading.Thread(target=self.run_server, args=(selected_file,))
        self.server_thread.daemon = True  # 设置为守护线程，程序退出时会自动关闭
        self.server_thread.start()
        
        # 禁用开始按钮，启用停止按钮
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
    def stop_server(self):
        if self.httpd:
            # 停止服务器
            self.httpd.shutdown()
            self.httpd.server_close()
        
        # 取消显示IP地址
        self.status_label.config(text="Server is off")
        
        # 启用开始按钮，禁用停止按钮
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
    def run_server(self, selected_file):
        try:
            port = 8080
            server_address = ("", port)
            
            handler = http.server.SimpleHTTPRequestHandler
            handler.extensions_map[".html"] = "text/html"
            
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
            
            self.status_label.config(text=f"Server is on: http://{local_ip}:{port}/")
            
            self.httpd = socketserver.TCPServer(server_address, handler)
            self.httpd.serve_forever()
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LANServerApp(root)
    root.mainloop()

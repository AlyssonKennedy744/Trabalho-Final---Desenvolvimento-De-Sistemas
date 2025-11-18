import threading
import ttkbootstrap as ttk 
from api import run_api
from gui import MovieApp

if __name__ == "__main__":

    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    print("API rodando em http://127.0.0.1:5000/api/filmes")

    root = ttk.Window(themename="cerculean") 
    
    app = MovieApp(root)
    root.mainloop()
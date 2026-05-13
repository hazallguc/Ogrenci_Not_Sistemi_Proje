
import tkinter as tk
from menu import NotSistemiApp  # Arayüz kodlarını menu.py içine koyduğun için oradan çağırıyoruz

def main():
   
    root = tk.Tk()
    
    app = NotSistemiApp(root)
    

    root.mainloop()

if __name__ == "__main__":
    main()


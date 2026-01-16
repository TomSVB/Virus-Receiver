import os
import json
import tkinter as tk
from tkinter import ttk, filedialog
import threading
import time

class DataReceiver:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Virus Empfangs-Tool")
        self.root.geometry("800x600")
        
        # Erstelle die Oberfläche
        self.setup_ui()
        
        # Starte Überwachung im Hintergrund
        self.start_monitoring()
        
    def setup_ui(self):
        # Hauptframe
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Überschrift
        title_label = ttk.Label(main_frame, text="Virus Empfangs-Tool", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        # Statusframe
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.status_label = ttk.Label(status_frame, text="Bereit...", foreground="blue")
        self.status_label.pack()
        
        # Datenframe
        data_frame = ttk.LabelFrame(main_frame, text="Empfangene Daten", padding="10")
        data_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Textarea für Datenanzeige
        self.data_text = tk.Text(data_frame, height=15, width=80)
        scrollbar = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=self.data_text.yview)
        self.data_text.configure(yscrollcommand=scrollbar.set)
        
        self.data_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, pady=(0, 20))
        
        self.refresh_btn = ttk.Button(button_frame, text="Aktualisieren", command=self.update_display)
        self.refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(button_frame, text="Löschen", command=self.clear_data)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Verzeichnis-Button
        self.dir_btn = ttk.Button(button_frame, text="Verzeichnis öffnen", command=self.open_directory)
        self.dir_btn.pack(side=tk.LEFT)
        
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        data_frame.columnconfigure(0, weight=1)
        data_frame.rowconfigure(0, weight=1)
        
    def update_display(self):
        """Aktualisiert die Anzeige mit den aktuellen Daten"""
        self.data_text.delete(1.0, tk.END)
        self.status_label.config(text="Suche nach Daten...")
        
        try:
            # Finde alle txt-Dateien im gleichen Verzeichnis
            current_dir = os.path.dirname(os.path.abspath(__file__))
            files = [f for f in os.listdir(current_dir) if f.endswith('.txt') and not f.startswith('log_')]
            
            if not files:
                self.data_text.insert(tk.END, "Keine Dateien gefunden.\n\n")
                self.status_label.config(text="Keine Dateien gefunden", foreground="orange")
                return
            
            # Sortiere nach Datum (neueste zuerst)
            files.sort(key=lambda x: os.path.getmtime(os.path.join(current_dir, x)), reverse=True)
            
            for filename in files:
                filepath = os.path.join(current_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    self.data_text.insert(tk.END, f"=== {filename} ===\n")
                    self.data_text.insert(tk.END, content + "\n\n")
                    
                except Exception as e:
                    self.data_text.insert(tk.END, f"Fehler beim Lesen von {filename}: {str(e)}\n\n")
            
            self.status_label.config(text=f"{len(files)} Dateien gefunden", foreground="green")
            
        except Exception as e:
            self.data_text.insert(tk.END, f"Fehler bei der Aktualisierung: {str(e)}\n")
            self.status_label.config(text="Fehler aufgetreten", foreground="red")

    def clear_data(self):
        """Löscht den Inhalt des Textbereichs"""
        self.data_text.delete(1.0, tk.END)
        
    def open_directory(self):
        """Öffnet das Verzeichnis mit dem Empfangs-Tool"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            # Versuche, das Verzeichnis zu öffnen (Windows)
            if os.name == 'nt':
                os.startfile(current_dir)
            else:
                # Für Linux/Mac
                subprocess.run(['xdg-open', current_dir])
        except Exception as e:
            print(f"Konnte Verzeichnis nicht öffnen: {e}")
    
    def start_monitoring(self):
        """Startet die Überwachung im Hintergrund"""
        def monitor():
            while True:
                try:
                    self.update_display()
                    time.sleep(2)  # Alle 2 Sekunden aktualisieren
                except Exception as e:
                    print(f"Überwachungsfehler: {e}")
                    time.sleep(2)
        
        monitoring_thread = threading.Thread(target=monitor, daemon=True)
        monitoring_thread.start()

def main():
    app = DataReceiver()
    
    # Starte die Anwendung
    try:
        app.root.mainloop()
    except KeyboardInterrupt:
        print("Programm beendet")

if __name__ == "__main__":
    main()

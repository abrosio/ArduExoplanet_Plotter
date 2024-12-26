import serial
import time
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime
import serial.tools.list_ports
import ttkbootstrap as ttkb
import threading
from queue import Queue
from matplotlib.animation import FuncAnimation
import os

# Variabili per il grafico
times = []
values = []

# Variabili per la connessione seriale
ser = None
start_time = None
log_directory = None
update_interval = 50  # Intervallo di aggiornamento del grafico in ms (default 50ms)

# Lista globale per accumulare tutti i dati ricevuti
logged_data = []

# Coda per gestire i dati
data_queue = Queue()
previous_value = None  # Memorizza il valore precedente della fotoresistenza

# Funzione per leggere il dato dalla porta seriale e metterlo nella coda
def read_data():
    global times, values, previous_value, logged_data
    try:
        if ser and ser.is_open:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                current_time = time.time() - start_time
                try:
                    value = float(line)  # Assumiamo che Arduino invii valori numerici
                    variation = value - previous_value if previous_value is not None else 0
                    previous_value = value  # Aggiorna il valore precedente

                    # Aggiungi dati alla coda
                    data_queue.put((current_time, value, variation))

                    # Accumula i dati nella lista globale
                    logged_data.append((current_time, value))
                except ValueError:
                    pass  # Ignora righe non numeriche
    except Exception as e:
        print(f"Errore durante la lettura dei dati: {e}")

    # Richiama questa funzione dopo l'intervallo impostato
    root.after(update_interval, read_data)

# Funzione per aggiornare il grafico con i nuovi dati
def update_graph(frame):
    global times, values
    # Controlla se ci sono nuovi dati nella coda
    while not data_queue.empty():
        current_time, value, variation = data_queue.get()
        times.append(current_time)
        values.append(value)

        # Mantieni il numero di dati nella lista limitato (esempio 100 punti)
        if len(times) > 100:
            times.pop(0)
            values.pop(0)
    
    # Aggiorna il grafico
    ax.clear()
    ax.plot(times, values)
    ax.set_xlabel("Tempo (s)", fontsize=10)
    ax.set_ylabel("Luce", fontsize=10)
    ax.set_title("ArduExo - Photometry Simulation", fontsize=12)
    ax.grid(True)
    return ax,

# Funzione per salvare il log su un file
def save_log():
    global log_directory, logged_data
    if not log_directory:
        log_directory = filedialog.askdirectory(title="Seleziona la directory di salvataggio")
        if not log_directory:
            print("Errore: Nessuna directory selezionata.")
            return
    
    filename = f"{log_directory}/fotoresistenza_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    try:
        with open(filename, 'w') as f:  # Usa 'w' per sovrascrivere il file
            # Scrivi l'intestazione
            f.write("Tempo (s);  Valore Fotoresistenza\n")
            
            # Scrivi tutti i dati registrati finora
            for t, v in logged_data:
                f.write(f"{t:.2f};       {v:.2f}\n")
        
        print(f"Log salvato in {filename}")
    except Exception as e:
        print(f"Errore durante il salvataggio del log: {e}")

# Funzione per iniziare la comunicazione seriale
def start_serial():
    global ser, start_time
    port = port_combobox.get()
    baud_rate = int(baud_combobox.get())
    
    if not port or not baud_rate:
        print("Errore: Selezionare una porta e un baud rate.")
        return
    
    try:
        ser = serial.Serial(port, baud_rate)
        start_time = time.time()

        # Avvia la lettura dei dati in un thread separato
        threading.Thread(target=read_data, daemon=True).start()

        start_button.config(text="Ferma", command=stop_serial)
        print("Comunicazione avviata.")
    except Exception as e:
        print(f"Errore durante l'inizializzazione: {e}")

# Funzione per fermare la comunicazione seriale
def stop_serial():
    global ser
    if ser and ser.is_open:
        ser.close()
        start_button.config(text="Avvia", command=start_serial)
        print("Comunicazione fermata.")

# Ottieni le porte seriali disponibili
def get_available_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# Funzione per aggiornare il menù a tendina delle porte
def update_ports():
    available_ports = get_available_ports()
    if not available_ports:
        print("Errore: Nessuna porta seriale disponibile.")
        return
    port_combobox['values'] = available_ports
    if not port_combobox.get() in available_ports:
        port_combobox.set('')  # Svuota se la porta selezionata non è disponibile
    if available_ports:
        port_combobox.set(available_ports[0])  # Seleziona la prima porta disponibile

# Funzione per aggiornare la velocità del plot (intervallo in ms)
def update_plot_speed():
    global update_interval
    try:
        update_interval = int(speed_entry.get())
        if update_interval <= 0:
            raise ValueError("Il valore deve essere positivo.")
        print(f"Velocità del plot impostata su {update_interval} ms")
    except ValueError:
        print("Errore: Inserisci un valore numerico valido per la velocità del plot.")

# Configurazione del grafico
fig, ax = plt.subplots(figsize=(8, 6))  # Ingrandito il grafico per evitare che i titoli siano tagliati

# Funzione per resettare e cancellare il plot
def reset_plot():
    global times, values, logged_data
    times.clear()  # Svuota i dati del tempo
    values.clear()  # Svuota i valori della fotoresistenza
    logged_data.clear()  # Svuota i dati registrati
    ax.clear()  # Cancella il grafico
    ax.set_xlabel("Tempo (s)", fontsize=10)
    ax.set_ylabel("Luce", fontsize=10)
    ax.set_title("ArduExo - Photometry Simulation", fontsize=12)
    ax.grid(True)
    canvas.draw()  # Ridisegna il grafico

# Funzione per salvare uno screenshot del grafico
def save_screenshot():
    global canvas
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        title="Scegli dove salvare lo screenshot"
    )
    if file_path:
        try:
            fig.savefig(file_path, dpi=300)
        except Exception as e:
            print(f"Errore durante il salvataggio dello screenshot: {e}")

# Configurazione dell'interfaccia grafica
def start_gui():
    global canvas, root, speed_entry
    root = ttkb.Window(themename="superhero")
    root.title("ArduExo 1.0")

    # Imposta l'icona della finestra
    try:
        # Ottieni il percorso assoluto dell'icona
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
        root.iconbitmap(icon_path)
    except Exception as e:
        print(f"Errore durante il caricamento dell'icona: {e}")

    # Frame per le opzioni di porta e baud rate (sullo stesso rigo)
    frame_ports = ttk.Frame(root)
    frame_ports.pack(padx=10, pady=10, fill="x")

    # Seleziona la porta COM e il baud rate su un unico rigo
    tk.Label(frame_ports, text="Seleziona la Porta COM:", font=('Arial', 10)).pack(side="left", padx=5)
    global port_combobox
    port_combobox = ttk.Combobox(frame_ports, width=10, font=('Arial', 10), state="readonly", height=5)
    port_combobox.pack(side="left", padx=5)

    # Aggiungi un pulsante per la scansione delle porte accanto al menù a tendina
    scan_button = ttkb.Button(frame_ports, text="Scansiona", command=update_ports, style="TButton", width=12, takefocus=False)
    scan_button.pack(side="left", padx=5)

    tk.Label(frame_ports, text="Seleziona il Baud Rate:", font=('Arial', 10)).pack(side="left", padx=5)
    baud_rates = [9600, 115200, 19200, 38400, 57600, 4800, 250000]  # Aggiunti 4800 e 250000
    global baud_combobox
    baud_combobox = ttk.Combobox(frame_ports, values=baud_rates, width=10, font=('Arial', 10), state="readonly", height=5)
    baud_combobox.set(9600)  # Imposta il valore predefinito
    baud_combobox.pack(side="left", padx=5)

    # Frame per i pulsanti e velocità del plot (tutto sullo stesso rigo)
    frame_buttons = ttk.Frame(root)
    frame_buttons.pack(padx=10, pady=10, fill="x")

    # Pulsante per avviare e fermare la comunicazione seriale
    global start_button
    start_button = ttkb.Button(frame_buttons, text="Avvia", command=start_serial, style="TButton", width=12, takefocus=False)
    start_button.pack(side="left", padx=5)

    # Pulsante per salvare il log
    save_button = ttkb.Button(frame_buttons, text="Salva Log", command=save_log, style="TButton", width=12, takefocus=False)
    save_button.pack(side="left", padx=5)

    # Pulsante per resettare il grafico
    reset_button = ttkb.Button(frame_buttons, text="Reset Plot", command=reset_plot, style="TButton", width=12, takefocus=False)
    reset_button.pack(side="left", padx=5)

    # Pulsante per salvare uno screenshot
    screenshot_button = ttkb.Button(frame_buttons, text="Screenshot", command=save_screenshot, style="TButton", width=12, takefocus=False)
    screenshot_button.pack(side="left", padx=5)

    # Aggiungi il campo di input per la velocità del plot
    tk.Label(frame_buttons, text="Velocità del Plot (ms):", font=('Arial', 10)).pack(side="left", padx=5)
    speed_entry = ttk.Entry(frame_buttons, width=8, font=('Arial', 10))
    speed_entry.insert(0, "50")  # Valore di default 50ms
    speed_entry.pack(side="left", padx=5)

    # Pulsante per aggiornare la velocità
    speed_button = ttkb.Button(frame_buttons, text="Aggiorna Velocità", command=update_plot_speed, style="TButton", width=16, takefocus=False)
    speed_button.pack(side="left", padx=5)

    # Aggiungi il grafico Matplotlib all'interfaccia Tkinter con padding
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(padx=20, pady=20)  # Aggiungi spazio ai bordi

    # Avvia la scansione delle porte
    update_ports()

    # Avvia la GUI
    ani = FuncAnimation(fig, update_graph, interval=update_interval, cache_frame_data=False)

    root.mainloop()

# Mostra il grafico con padding interno
plt.tight_layout(pad=2.0)  # Aggiungi margini interni al grafico

# Avvia l'interfaccia grafica
start_gui()

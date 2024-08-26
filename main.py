import socket
import tkinter as tk
from tkinter import messagebox


def check_if_is_a_well_known_port(port, protocol='tcp'):
    try:
        service_name = socket.getservbyport(port, protocol)
        return service_name
    except:
        return None


def scan_ports(host, ports, text_widget):
    open_ports = {}
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            conn = s.connect_ex((host, port))
            if conn == 0:
                service = check_if_is_a_well_known_port(port)
                open_ports[port] = service if service else "Unknown Service"
                text_widget.insert(tk.END, f"Port {port}: Opened on service: {open_ports[port]}\n")
            else:
                text_widget.insert(tk.END, f"Port {port}: Closed\n")
            text_widget.update() 
        except:
            pass
        finally:
            s.close()
    return open_ports


def main():
    def scan():
        host = entry.get()
        try:
            start_port = int(entry2.get())
            end_port = int(entry3.get())
            if start_port < 0 or end_port > 65535:
                raise ValueError("Portas devem estar entre 0 e 65535.")
            if start_port > end_port:
                raise ValueError("A porta inicial deve ser menor ou igual à porta final.")
            ports_range = range(start_port, end_port + 1)
            result_text.delete(1.0, tk.END) 
            scan_ports(host, ports_range, result_text)
        except ValueError as ve:
            messagebox.showerror('Erro de Entrada', str(ve))
        except Exception as e:
            messagebox.showerror('Erro', f"Ocorreu um erro: {e}")


    root = tk.Tk()
    root.title('Port Scanner')

    label = tk.Label(root, text='Host:')
    label.pack()
    entry = tk.Entry(root)
    entry.pack()
    
    label2 = tk.Label(root, text='Porta Inicial:')
    label2.pack()
    entry2 = tk.Entry(root)
    entry2.pack()

    label3 = tk.Label(root, text='Porta Final:')
    label3.pack()
    entry3 = tk.Entry(root)
    entry3.pack()

    button = tk.Button(root, text='Scan', command=scan)
    button.pack()

    result_text = tk.Text(root, height=15, width=50)
    result_text.pack()

    root.mainloop()


if __name__ == '__main__':
    main()

import tkinter as tk
from tkinter import messagebox
import ipaddress
import math

Network = None

def calculIP():
    global Network
    ip_with_prefix = entry_ip.get()

    try:
        network = ipaddress.ip_network(ip_with_prefix, strict=False)
        output = (
            f"Network: {network.network_address}\n"
            f"Masca de rețea: {network.netmask}\n"
            f"Prefix: /{network.prefixlen}\n"
            f"Broadcast: {network.broadcast_address}\n"
            f"Hosts: {network.num_addresses - 2}\n"
            f"Primul IP: {network.network_address + 1}\n"
            f"Ultimul IP: {network.broadcast_address - 1}\n"
        )

        Network = int(network.network_address) + 1
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, output)
        text_tabela.delete(1.0, tk.END)
        tabela = "LAN/WAN  H    Network    Prefix   Broadcast      1st IP         Last IP        Masca\n"
        text_tabela.insert(tk.END, tabela)
    except ValueError as e:
        messagebox.showerror("Eroare", f"Adresă IP, prefix sau număr de gazde invalid: {e}")


def calculPrefix(h):
    prefix = 32 - math.ceil(math.log2(h + 2))
    return prefix

def calculTabela():
    global Network
    try:
        num_hosts = int(entry_HOST.get())
        p = calculPrefix(num_hosts)
        adresaIP = f"{ipaddress.IPv4Address(Network)}/{p}"
        net = ipaddress.ip_network(adresaIP, strict=False)
        tabelaS = (
            f"\n{entry_LAN_WAN.get()} |{num_hosts}| {net.network_address} |/{net.prefixlen}| "
            f"{net.broadcast_address}  |{net.network_address + 1}| {net.broadcast_address - 1} |{net.netmask}"
        )
        text_tabela.insert(tk.END, tabelaS)
        Network = int(net.broadcast_address) + 1
    except ValueError as e:
        messagebox.showerror("Eroare", f"A apărut o eroare: {e}")
    except Exception as e:
        messagebox.showerror("Eroare", f"A apărut o eroare: {e}")



root = tk.Tk()
root.title("Tabela de Subnetare")
root.geometry("800x700")

label_ip = tk.Label(root, text="IP cu prefix")
label_ip.grid(row=0, column=0, padx=5, pady=10, sticky='w')
entry_ip = tk.Entry(root, width=30)
entry_ip.grid(row=0, column=1, padx=5, pady=10, sticky='w')

label_LAN_WAN = tk.Label(root, text="LAN/WAN:")
label_LAN_WAN.grid(row=0, column=2, padx=5, pady=10, sticky='w')
entry_LAN_WAN = tk.Entry(root, width=10)
entry_LAN_WAN.grid(row=0, column=3, padx=5, pady=10, sticky='w')

label_HOST = tk.Label(root, text="Host:")
label_HOST.grid(row=0, column=4, padx=5, pady=10, sticky='w')
entry_HOST = tk.Entry(root, width=10)
entry_HOST.grid(row=0, column=5, padx=5, pady=10, sticky='w')

button = tk.Button(root, text="Generează Tabela", command=calculIP)
button.grid(row=1, column=0, columnspan=2, pady=10)

button = tk.Button(root, text="Sub Tab", command=calculTabela)
button.grid(row=1, column=2, columnspan=2, pady=10)

text_output = tk.Text(root, height=10, width=32)
text_output.grid(row=2, column=0, columnspan=6, padx=10, pady=10, sticky='w')

text_tabela = tk.Text(root, height=25, width=93)
text_tabela.grid(row=3, column=0, columnspan=6, padx=10, pady=10, sticky='w')

root.mainloop()

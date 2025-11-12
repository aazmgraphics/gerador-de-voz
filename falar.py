import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import edge_tts
from datetime import datetime
import os
import threading
from playsound import playsound  # 🔊 substitui o pygame

# Função assíncrona para gerar o áudio
async def gerar_audio(texto, voz):
    nome_arquivo = f"voz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    comunicador = edge_tts.Communicate(texto, voz)
    await comunicador.save(nome_arquivo)
    return nome_arquivo

# Atualiza a lista de arquivos mp3
def atualizar_lista():
    lista.delete(0, tk.END)
    arquivos = sorted(
        [f for f in os.listdir() if f.endswith(".mp3")],
        key=os.path.getmtime,
        reverse=True
    )
    for arquivo in arquivos:
        lista.insert(tk.END, arquivo)

# Função principal de geração de voz
def gerar():
    texto = entrada_texto.get("1.0", tk.END).strip()
    voz = combo_vozes.get()
    if not texto:
        messagebox.showwarning("Aviso", "Digite um texto para gerar a narração.")
        return
    if not voz:
        messagebox.showwarning("Aviso", "Escolha uma voz antes de gerar.")
        return

    def tarefa():
        try:
            asyncio.run(gerar_audio(texto, voz))
            messagebox.showinfo("Sucesso", "Arquivo de voz gerado com sucesso!\n\nSalvo no mesmo diretório.")
            atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")

    threading.Thread(target=tarefa).start()

# Função para tocar o áudio
def tocar_audio(event):
    selecao = lista.curselection()
    if not selecao:
        return
    arquivo = lista.get(selecao[0])

    def tocar():
        try:
            playsound(arquivo)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível tocar o áudio:\n{e}")

    threading.Thread(target=tocar).start()

# Interface principal
janela = tk.Tk()
janela.title("Gerador de Voz - edge-tts")
janela.geometry("420x500")
janela.resizable(False, False)

tk.Label(janela, text="Digite o texto:", font=("Arial", 10, "bold")).pack(pady=5)
entrada_texto = tk.Text(janela, height=6, width=50)
entrada_texto.pack(padx=10, pady=5)

tk.Label(janela, text="Escolha a voz:", font=("Arial", 10, "bold")).pack(pady=5)
vozes_disponiveis = [
    "pt-BR-AntonioNeural",
    "pt-BR-FranciscaNeural",
    "pt-BR-ThalitaNeural",
    "pt-PT-DuarteNeural",
    "pt-PT-RaquelNeural"
]
combo_vozes = ttk.Combobox(janela, values=vozes_disponiveis, state="readonly", width=35)
combo_vozes.set(vozes_disponiveis[0])
combo_vozes.pack(pady=5)

botao = tk.Button(janela, text="Gerar Voz", width=35, height=2, bg="#4CAF50", fg="white", command=gerar)
botao.pack(pady=10)

tk.Label(janela, text="Arquivos gerados:", font=("Arial", 10, "bold")).pack(pady=5)
frame_lista = tk.Frame(janela)
frame_lista.pack(padx=10, pady=5, fill="both", expand=True)

scrollbar = tk.Scrollbar(frame_lista)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista = tk.Listbox(frame_lista, height=10, width=50, yscrollcommand=scrollbar.set)
lista.pack(side=tk.LEFT, fill="both", expand=True)
scrollbar.config(command=lista.yview)

lista.bind("<Double-Button-1>", tocar_audio)

atualizar_lista()

janela.mainloop()

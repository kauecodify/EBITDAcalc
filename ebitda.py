import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

def calculate_ebitda():
    try:
        revenue = float(entry_revenue.get())
        expenses = float(entry_expenses.get())
        depreciation = float(entry_depreciation.get())
        amortization = float(entry_amortization.get())
        
        ebitda = revenue - expenses + depreciation + amortization
        result_label.config(text=f"EBITDA Calculado: R$ {ebitda:,.2f}")
        update_values_on_tabs(revenue, expenses, depreciation, amortization, ebitda)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")

def update_values_on_tabs(revenue, expenses, depreciation, amortization, ebitda):
    summary_text = (
        f"### Resumo dos Dados Financeiros ###\n\n"
        f"1. **Receita Total**: R$ {revenue:,.2f}\n"
        f"2. **Despesas Operacionais**: R$ {expenses:,.2f}\n"
        f"3. **Depreciação**: R$ {depreciation:,.2f}\n"
        f"4. **Amortização**: R$ {amortization:,.2f}\n"
        f"5. **EBITDA**: R$ {ebitda:,.2f}"
    )
    summary_label.config(text=summary_text)
    generate_dynamic_allocations(ebitda)
    plot_risk()

def generate_dynamic_allocations(ebitda):
    allocation_categories = {
        "CDB": 0.4,
        "EMERGÊNCIA": 0.3,
        "INSUMOS": 0.2,
        "BTC": 0.1
    }
    allocations = {category: ebitda * percentage for category, percentage in allocation_categories.items()}
    plot_allocations(allocations)

def plot_risk():
    try:
        initial_value = float(entry_revenue.get())
        risk_factor = float(entry_risk.get())
        if initial_value <= 0 or risk_factor <= 0:
            raise ValueError("Os valores iniciais devem ser maiores que zero.")
        
        times = range(1, 13)
        values = [initial_value]
        
        for t in times[1:]:
            growth_rate = random.uniform(0.01, 0.05)
            new_value = values[-1] * (1 + growth_rate)
            values.append(new_value)
        
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(times, values, marker='o', linestyle='-', color='blue', linewidth=2)
        ax.set_title(f"Crescimento com Oscilação - Risco de {risk_factor}%", fontsize=14)
        ax.set_xlabel("Meses", fontsize=12)
        ax.set_ylabel("Valor (R$)", fontsize=12)
        ax.set_xticks([])
        
        for i, value in enumerate(values):
            ax.annotate(f"R$ {value:,.2f}", (times[i], values[i]), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=9, color='black')
        
        ax.grid(alpha=0.3)
        for widget in tab_risk.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=tab_risk)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos de receita e risco.")

def plot_allocations(allocations):
    try:
        total = sum(allocations.values())
        allocations_percent = {key: (value / total) * 100 for key, value in allocations.items()}
        
        fig, ax = plt.subplots(figsize=(5, 4))
        wedges, texts, autotexts = ax.pie(allocations_percent.values(), labels=allocations_percent.keys(),
                                          autopct='%1.1f%%', startangle=90, colors=plt.cm.tab20.colors)
        
        for i, wedge in enumerate(wedges):
            value_text = f"R$ {allocations[list(allocations.keys())[i]]:,.2f}"
            texts[i].set_text(f"{texts[i].get_text()}\n{value_text}")
        
        ax.set_title("Distribuição de Aportes")
        for widget in tab_allocations.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=tab_allocations)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar o gráfico: {e}")

root = tk.Tk()
root.title("Calculadora de EBITDA com Gráficos")
root.geometry("850x650")

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook.Tab", font=("Helvetica", 12), padding=[20, 10])

notebook = ttk.Notebook(root)
notebook.pack(pady=20, expand=True)

tab_calculator = ttk.Frame(notebook, padding=20)
tab_summary = ttk.Frame(notebook, padding=20)
tab_risk = ttk.Frame(notebook, padding=20)
tab_allocations = ttk.Frame(notebook, padding=20)

notebook.add(tab_calculator, text="Calculadora")
notebook.add(tab_summary, text="Resumo")
notebook.add(tab_risk, text="Risco de Investimento")
notebook.add(tab_allocations, text="Distribuição de Aportes")

ttk.Label(tab_calculator, text="Receita Total (R$):", font=("Helvetica", 11)).grid(row=0, column=0, sticky="w", pady=5)
entry_revenue = ttk.Entry(tab_calculator, width=30)
entry_revenue.grid(row=0, column=1, pady=5)

ttk.Label(tab_calculator, text="Despesas Operacionais (R$):", font=("Helvetica", 11)).grid(row=1, column=0, sticky="w", pady=5)
entry_expenses = ttk.Entry(tab_calculator, width=30)
entry_expenses.grid(row=1, column=1, pady=5)

ttk.Label(tab_calculator, text="Depreciação (R$):", font=("Helvetica", 11)).grid(row=2, column=0, sticky="w", pady=5)
entry_depreciation = ttk.Entry(tab_calculator, width=30)
entry_depreciation.grid(row=2, column=1, pady=5)

ttk.Label(tab_calculator, text="Amortização (R$):", font=("Helvetica", 11)).grid(row=3, column=0, sticky="w", pady=5)
entry_amortization = ttk.Entry(tab_calculator, width=30)
entry_amortization.grid(row=3, column=1, pady=5)

calculate_button = ttk.Button(tab_calculator, text="Calcular EBITDA", command=calculate_ebitda)
calculate_button.grid(row=4, column=0, columnspan=2, pady=20)

result_label = ttk.Label(tab_calculator, text="", font=("Helvetica", 12, "bold"))
result_label.grid(row=5, column=0, columnspan=2, pady=10)

summary_label = ttk.Label(tab_summary, text="", justify="left", wraplength=500, font=("Helvetica", 11))
summary_label.pack(pady=10)

ttk.Label(tab_risk, text="Risco (%) ao Ano:", font=("Helvetica", 11)).pack(pady=5)
entry_risk = ttk.Entry(tab_risk, width=30)
entry_risk.pack(pady=5)

risk_button = ttk.Button(tab_risk, text="Gerar Gráfico de Risco", command=plot_risk)
risk_button.pack(pady=10)

allocations_button = ttk.Button(tab_allocations, text="Gerar Gráfico de Aportes", command=lambda: generate_dynamic_allocations(float(entry_revenue.get()) - float(entry_expenses.get()) + float(entry_depreciation.get()) + float(entry_amortization.get())))
allocations_button.pack(pady=10)

root.mainloop()

import streamlit as st
import pandas as pd
from datetime import datetime

# --- (Mantendo a Classe ICHCalculator anterior) ---
class ICHCalculator:
    def __init__(self):
        self.base_unit_cost = 500.00
        self.ich_members = {
            "USA": {"name": "Estados Unidos (FDA)", "tax_index": 1.0, "labor_index": 1.2, "ppp": 1.0},
            "BRA": {"name": "Brasil (ANVISA)", "tax_index": 1.6, "labor_index": 0.8, "ppp": 2.4},
            "CHE": {"name": "Suíça (Swissmedic)", "tax_index": 1.0, "labor_index": 1.5, "ppp": 1.1},
            "JPN": {"name": "Japão (MHLW/PMDA)", "tax_index": 1.1, "labor_index": 1.1, "ppp": 90.0},
            "CHN": {"name": "China (NMPA)", "tax_index": 1.2, "labor_index": 0.7, "ppp": 3.8}
        }

    def calculate(self, iso_code, num_samples):
        m = self.ich_members[iso_code]
        cost_global = (self.base_unit_cost * 0.50) * m["tax_index"]
        cost_local = (self.base_unit_cost * 0.35) * m["ppp"] * m["labor_index"]
        quality = (cost_global + cost_local) * 0.15
        total = (cost_global + cost_local + quality) * num_samples
        return {
            "Total": round(total, 2),
            "Hardware": round(cost_global * num_samples, 2),
            "Operacional": round(cost_local * num_samples, 2),
            "Qualidade": round(quality * num_samples, 2)
        }

calc = ICHCalculator()

# --- Interface Streamlit ---
st.title("🔬 Monitor de Gastos: Análise de Polimorfismo (XRPD)")

with st.sidebar:
    st.header("Parâmetros")
    pais_cod = st.selectbox("Membro ICH:", list(calc.ich_members.keys()))
    amostras = st.number_input("Número de Amostras:", min_value=1, value=1)
    
# Execução
res = calc.calculate(pais_cod, amostras)

# Cards de Resumo
col1, col2, col3 = st.columns(3)
col1.metric("Custo Total (USD)", f"$ {res['Total']:,.2f}")
col2.metric("Tecnologia", f"$ {res['Hardware']:,.2f}")
col3.metric("Mão de Obra/PPP", f"$ {res['Operacional']:,.2f}")

st.divider()

# --- Seção de Exportação ---
st.subheader("📊 Relatório de Precificação")

# Criando DataFrame para o Relatório
report_data = {
    "Data do Relatório": [datetime.now().strftime("%d/%m/%Y %H:%M")],
    "País/Agência": [calc.ich_members[pais_cod]['name']],
    "Qtd Amostras": [amostras],
    "Custo Tecnologia (USD)": [res['Hardware']],
    "Custo Operacional (USD)": [res['Operacional']],
    "Custo Qualidade/BPL (USD)": [res['Qualidade']],
    "Total Estimado (USD)": [res['Total']]
}
df_report = pd.DataFrame(report_data)

# Exibe a tabela no Dashboard
st.table(df_report.T.rename(columns={0: "Valores Estimados"}))

# Botão de Download
csv = df_report.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Baixar Orçamento (CSV)",
    data=csv,
    file_name=f"orcamento_xrpd_{pais_cod}_{datetime.now().strftime('%Y%m%d')}.csv",
    mime='text/csv',
)

st.success("Cálculo realizado seguindo os pesos de hardware dolarizado e operação via PPP.")

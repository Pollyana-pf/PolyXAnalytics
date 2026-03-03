/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState } from 'react';
import { Activity, BarChart3, Search, Settings, FileText, FlaskConical, BookOpen } from 'lucide-react';
import { Dashboard } from './components/Dashboard';
import { AnalysisSearch } from './components/AnalysisSearch';
import { Resources } from './components/Resources';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="flex h-screen bg-slate-50 text-slate-900 font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col">
        <div className="p-6 border-b border-slate-100 flex items-center gap-3 text-indigo-600">
          <FlaskConical className="w-8 h-8" />
          <span className="text-xl font-bold tracking-tight text-slate-900">PolyX Analytics</span>
        </div>
        
        <nav className="flex-1 p-4 space-y-1">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors ${
              activeTab === 'dashboard'
                ? 'bg-indigo-50 text-indigo-700'
                : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
            }`}
          >
            <BarChart3 className="w-5 h-5" />
            Market Overview
          </button>
          <button
            onClick={() => setActiveTab('search')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors ${
              activeTab === 'search'
                ? 'bg-indigo-50 text-indigo-700'
                : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
            }`}
          >
            <Search className="w-5 h-5" />
            Company Analysis
          </button>
          <button
            onClick={() => setActiveTab('resources')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors ${
              activeTab === 'resources'
                ? 'bg-indigo-50 text-indigo-700'
                : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
            }`}
          >
            <BookOpen className="w-5 h-5" />
            Resources & APIs
          </button>
          <button
            onClick={() => setActiveTab('reports')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors ${
              activeTab === 'reports'
                ? 'bg-indigo-50 text-indigo-700'
                : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
            }`}
          >
            <FileText className="w-5 h-5" />
            Saved Reports
          </button>
        </nav>

        <div className="p-4 border-t border-slate-100">
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-slate-600 hover:bg-slate-50 hover:text-slate-900 transition-colors">
            <Settings className="w-5 h-5" />
            Settings
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'search' && <AnalysisSearch />}
        {activeTab === 'resources' && <Resources />}
        {activeTab === 'reports' && (
          <div className="p-8">
            <h1 className="text-2xl font-bold text-slate-900 mb-6">Saved Reports</h1>
            <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center">
              <Activity className="w-12 h-12 text-slate-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-slate-900 mb-2">No reports saved yet</h3>
              <p className="text-slate-500">Run an analysis and save it to view it here later.</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}    pais_cod = st.selectbox("Membro ICH:", list(calc.ich_members.keys()))
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

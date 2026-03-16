import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

# --- 1. CONFIGURAÇÃO DA PÁGINA WEB ---
st.set_page_config(page_title="Dashboard de Comissões 2026", layout="wide")
st.title("📊 Cenários de Comissionamento")

# Mapeamento do nome das abas no Excel
ABAS_MAPEAMENTO = {
    "Lucas": "Analise Individual Lucas",
    "Amandio": "Analise Individual Amandio",
    "Fernando": "Analise Individual Fernando"
}

# --- 2. UPLOAD DO ARQUIVO ---
st.markdown("### 📂 1. Importação de Dados")
arquivo_excel = st.file_uploader("Faça o upload do arquivo consolidado (Excel) com os 3 cenários:", type=["xlsx"])

# Só renderiza o painel se o arquivo for carregado
if arquivo_excel is not None:
    
    # --- 3. CARREGAMENTO DOS DADOS (Com Cache) ---
    @st.cache_data
    def carregar_todos_dados(file):
        xls = pd.ExcelFile(file)
        dados = {}
        for nome_cenario, nome_aba in ABAS_MAPEAMENTO.items():
            if nome_aba in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=nome_aba)
                df.columns = df.columns.str.lower()
                if 'competencia' in df.columns:
                    df['competencia_dt'] = pd.to_datetime(df['competencia'])
                    df['competencia_str'] = df['competencia_dt'].dt.strftime('%m/%Y')
                dados[nome_cenario] = df
        return dados

    dados_completos = carregar_todos_dados(arquivo_excel)

    if not dados_completos:
        st.error("❌ As abas não foram encontradas no arquivo. Verifique se os nomes das abas estão corretos.")
        st.stop()

    # --- 4. MENU LATERAL DE FILTROS ---
    st.sidebar.header("⚙️ Configurações do Painel")
    
    visao_escolhida = st.sidebar.radio(
        "Selecione a Visão:",
        ["Comparativo Geral (Os 3 Cenários)", "Lucas", "Amandio", "Fernando"]
    )

    # =========================================================================
    # VISÃO 1: COMPARATIVO GERAL
    # =========================================================================
    if visao_escolhida == "Comparativo Geral (Os 3 Cenários)":
        st.markdown("---")
        st.header("🏆 Comparativo de Impacto Final (Acumulado do Ano)")
        
        # Consolida as métricas principais
        resumo_metricas = []
        for cenario, df in dados_completos.items():
            fat_total = df['faturamento_individual'].sum()
            custo_atual = df['comissão individual'].sum()
            custo_novo = df['comissao_final_garantida'].sum()
            invest_garantia = df['investimento_protecao'].sum()
            qtd_garantia = len(df[df['investimento_protecao'] > 0])
            
            impacto_final_pct = (custo_novo / fat_total) * 100 if fat_total > 0 else 0
            
            resumo_metricas.append({
                "Cenário": cenario,
                "Custo Atual (R$)": custo_atual,
                "Novo Custo c/ Garantia (R$)": custo_novo,
                "Aumento de Despesa (R$)": custo_novo - custo_atual,
                "Impacto Final (%)": impacto_final_pct,
                "Pessoas na Garantia": qtd_garantia,
                "Gasto Exclusivo c/ Garantia (R$)": invest_garantia
            })
            
        df_resumo = pd.DataFrame(resumo_metricas)
        
        # Exibição dos KPIs em Colunas
        cols = st.columns(3)
        for idx, row in df_resumo.iterrows():
            with cols[idx]:
                st.info(f"### Modelo: {row['Cenário']}")
                st.metric("Impacto Final (%)", f"{row['Impacto Final (%)']:.2f}%")
                st.metric("Aumento de Despesa", f"R$ {row['Aumento de Despesa (R$)']:,.2f}")
                valor = ((row['Pessoas na Garantia'] / 12) / 5889) * 100
                st.metric("Vol. Pessoas na Garantia", f"{row['Pessoas na Garantia'] / 12:.0f} pessoas/mês", f"{valor:.2f}% da base")

        st.markdown("#### Detalhamento Financeiro")
        # Formata o dataframe para exibição
        df_exibicao = df_resumo.copy()
        for col in ["Custo Atual (R$)", "Novo Custo c/ Garantia (R$)", "Aumento de Despesa (R$)", "Gasto Exclusivo c/ Garantia (R$)"]:
            df_exibicao[col] = df_exibicao[col].apply(lambda x: f"R$ {x:,.2f}")
        df_exibicao["Impacto Final (%)"] = df_exibicao["Impacto Final (%)"].apply(lambda x: f"{x:.2f}%")
        st.dataframe(df_exibicao, use_container_width=True)

        # Gráfico Comparativo
        fig_comp = px.bar(
            df_resumo, x="Cenário", y="Aumento de Despesa (R$)", color="Cenário",
            text_auto=".3s", title="Aumento Total de Despesa por Cenário (R$)",
            template="plotly_white"
        )
        st.plotly_chart(fig_comp, use_container_width=True)


    # =========================================================================
    # VISÃO 2: ANÁLISE INDIVIDUAL (LUCAS, AMANDIO OU FERNANDO)
    # =========================================================================
    else:
        df_estudo = dados_completos[visao_escolhida]
        
        st.markdown("---")
        st.header(f"🔍 Análise Profunda: Modelo {visao_escolhida}")
        
        # --- NOVO FILTRO DE COMPETÊNCIA
        # Ordena as datas cronologicamente para o slider funcionar direito
        df_estudo = df_estudo.sort_values('competencia_dt')
        competencias_disponiveis = df_estudo['competencia_str'].unique().tolist()
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("**Filtro de Período**")
        
        if len(competencias_disponiveis) > 1:
            comp_inicial, comp_final = st.sidebar.select_slider(
                "Arraste para selecionar os meses:",
                options=competencias_disponiveis,
                value=(competencias_disponiveis[0], competencias_disponiveis[-1])
            )
            # Fatiar a lista para pegar todos os meses entre o início e o fim escolhido
            idx_inicio = competencias_disponiveis.index(comp_inicial)
            idx_fim = competencias_disponiveis.index(comp_final)
            comps_selecionadas = competencias_disponiveis[idx_inicio:idx_fim+1]
        else:
            comps_selecionadas = competencias_disponiveis
            
        df_filtrado = df_estudo[df_estudo['competencia_str'].isin(comps_selecionadas)]

        # --- Gráfico 1: Dispersão ---
        st.subheader("1. Dispersão: Comissão Atual vs Nova Garantida")
        LIMITE_VISUAL = 6000
        fig_scatter = px.scatter(
            df_filtrado, x="comissão individual", y="comissao_final_garantida", color="cargo",
            hover_data=["nome", "ganho_nominal", "%atingimento_meta"],
            labels={"comissão individual": "Pagamento Atual (R$)", "comissao_final_garantida": "Novo Pagamento Garantido (R$)"},
            template="plotly_white", range_x=[0, LIMITE_VISUAL], range_y=[0, LIMITE_VISUAL]
        )
        fig_scatter.add_shape(type="line", line=dict(dash="dash", color="red", width=2), x0=0, y0=0, x1=LIMITE_VISUAL, y1=LIMITE_VISUAL)
        fig_scatter.add_annotation(x=LIMITE_VISUAL * 0.70, y=LIMITE_VISUAL * 0.90, showarrow=False, font=dict(color="green", size=13))
        st.plotly_chart(fig_scatter, use_container_width=True)

        # --- Gráfico 2: Ganhos Extras ---
        st.subheader("2. Evolução de Ganhos Extras")
        df_barras = df_filtrado.copy()
        cortes = [-1, 0.01, 99.99, 300.99, 500.99, 1000.99, float('inf')]
        nomes_grupos = ["R$ 0 (S/ ganho extra)", "R$ 1 a R$ 99", "R$ 100 a R$ 300", "R$ 301 a R$ 500", "R$ 501 a R$ 1000", "> R$ 1000"]
        df_barras['grupo_ganho'] = pd.cut(df_barras['ganho_nominal'], bins=cortes, labels=nomes_grupos)
        df_resumo_ganhos = df_barras.groupby(['competencia_str', 'grupo_ganho']).size().reset_index(name='Quantidade de Pessoas')
        df_resumo_ganhos['grupo_ganho'] = pd.Categorical(df_resumo_ganhos['grupo_ganho'], categories=nomes_grupos, ordered=True)
        df_resumo_ganhos = df_resumo_ganhos.sort_values(['competencia_str', 'grupo_ganho'])

        fig_barras = px.bar(
            df_resumo_ganhos, x='competencia_str', y='Quantidade de Pessoas', color='grupo_ganho', barmode='group',
            text='Quantidade de Pessoas', labels={"competencia_str": "Mês", "grupo_ganho": "Faixa de Ganho"},
            template="plotly_white", color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_barras.update_traces(textposition='outside', textfont_size=12)
        fig_barras.update_layout(xaxis_type='category')
        st.plotly_chart(fig_barras, use_container_width=True)

        # --- Gráfico 3 e 4: Projeção Financeira ---
        st.subheader("3. Projeção Financeira e Payback (Turnover limite: 3.960)")
        
        meses_selecionados_qtd = df_estudo["competencia_dt"].nunique()
        ultima_comp = df_estudo["competencia_dt"].max()
        total_colaboradores = len(df_estudo[df_estudo["competencia_dt"] == ultima_comp])
        if total_colaboradores == 0: total_colaboradores = len(df_estudo) / meses_selecionados_qtd

        custo_mensal_atual = df_estudo["comissão individual"].sum() / meses_selecionados_qtd
        custo_mensal_meritocratico = df_estudo["vl_comissao_cenario"].sum() / meses_selecionados_qtd
        garantia_mensal_inicial = df_estudo["investimento_protecao"].sum() / meses_selecionados_qtd

        saidas_mes = 150
        meses = np.arange(0, 120)
        custos_novos, economias_acumuladas = [], []

        for mes in meses:
            turnover_acumulado = min(mes * saidas_mes, 3960)
            qtd_com_garantia = max(0, total_colaboradores - turnover_acumulado)
            proporcao_ativos = qtd_com_garantia / total_colaboradores
            
            garantia_no_mes = garantia_mensal_inicial * proporcao_ativos
            custo_total_mes = custo_mensal_meritocratico + garantia_no_mes
            custos_novos.append(custo_total_mes)

            if mes == 0:
                economias_acumuladas.append(0)
            else:
                saldo_mes = custo_mensal_atual - custo_total_mes
                economias_acumuladas.append(economias_acumuladas[-1] + saldo_mes)

        df_proj = pd.DataFrame({"mes": meses, "novo_custo": custos_novos, "custo_atual": [custo_mensal_atual] * len(meses), "economia_acumulada": economias_acumuladas})

        col1, col2 = st.columns(2)
        with col1:
            fig_proj = px.line(df_proj, x="mes", y=["novo_custo", "custo_atual"], title="Projeção de Custo Mensal (R$)", markers=True, template="plotly_white")
            fig_proj.add_hline(y=custo_mensal_atual, line_dash="dot", line_color="red", annotation_text="Custo Atual da Empresa")
            st.plotly_chart(fig_proj, use_container_width=True)

        with col2:
            fig_payback = px.bar(df_proj, x="mes", y="economia_acumulada", title="Economia Acumulada Projetada", text_auto=".2s", template="plotly_white")
            st.plotly_chart(fig_payback, use_container_width=True)

        payback_mes = next((m for m, v in enumerate(custos_novos) if v <= custo_mensal_atual), "Nunca")
        st.info(f"**Base Média Ativa:** {total_colaboradores:.0f} colaboradores | **Custo Médio Mensal (Filtro):** R$ {custo_mensal_atual:,.2f} | **Payback Projetado:** Mês {payback_mes}")
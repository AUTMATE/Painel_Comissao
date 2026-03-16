import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(
    page_title="Dashboard Executivo - Comissões",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Caminho único da Logo Verde exigido
CAMINHO_LOGO = r"C:\Users\996086\Desktop\ScriptComissaoVendas_v2\img\logoVerde.png"

# =========================================================
# ESTILO VISUAL CORPORATIVO (CSS AVANÇADO)
# =========================================================

st.markdown("""
<style>
    /* Ajuste de margens do topo para ganhar espaço de tela */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* Títulos padronizados com a cor da marca */
    h1, h2, h3, h4 {
        color: #0B7A3E;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
    }

    /* Barra lateral limpa e elegante */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e9ecef;
    }

    /* Estilização Premium para os Cards de Métricas (KPIs) */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #eef0f2;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    /* Efeito de interatividade ao passar o mouse nos Cards */
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.08);
    }

    /* Valor do KPI em destaque */
    div[data-testid="stMetricValue"] > div {
        color: #0B7A3E !important;
        font-size: 28px;
        font-weight: 700;
    }

    /* Rótulo do KPI mais neutro para contraste */
    div[data-testid="stMetricLabel"] > div {
        color: #6c757d !important;
        font-size: 15px;
        font-weight: 500;
    }
    
    /* Linhas divisórias mais suaves */
    hr {
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        border: 0;
        border-top: 1px solid #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER COM LOGO
# =========================================================

col_logo, col_title = st.columns([1, 6])


with col_title:
    st.title("Projeto  de Comissionamento")
    st.markdown("<p style='color: #6c757d; font-size: 1.1rem; margin-top: -15px;'>Simulação Estratégica e Impacto Financeiro de Cenários de Comissão</p>", unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

try:
    # Utilizando a mesma logo verde na sidebar para reforçar a marca
    st.sidebar.image(CAMINHO_LOGO, width=160)
except:
    pass

st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.header("⚙️ Configurações do Painel")

# =========================================================
# MAPEAMENTO DAS ABAS E REGRAS
# =========================================================

ABAS_INDIVIDUAL = {
    "Lucas": "Analise Individual Lucas",
    "Amandio": "Analise Individual Amandio",
    "Fernando": "Analise Individual Fernando"
}

ABAS_RESUMO = {
    "Lucas": "Resumo por Faixa Lucas",
    "Amandio": "Resumo por Faixa Amandio",
    "Fernando": "Resumo por Faixa Fernando"
}

TABELAS_REGRAS = {
    "Lucas": [
        {"Faixa": "0% a 59,99%", "Fator": "Fixo em 0,50%", "Comentário": "Fixo"},
        {"Faixa": "60% a 79,99%", "Fator": "0,50% até 0,55%", "Comentário": "Progressivo"},
        {"Faixa": "80% a 99,99%", "Fator": "0,55% até 0,66%", "Comentário": "Progressivo"},
        {"Faixa": "100%", "Fator": "0,66%", "Comentário": "Cravado"},
        {"Faixa": "100,01% a 119,99%", "Fator": "0,66% até 0,70%", "Comentário": "Progressivo"},
        {"Faixa": "120% a 139,99%", "Fator": "0,70% até 0,73%", "Comentário": "Progressivo"},
        {"Faixa": "140% a 159,99%", "Fator": "0,73% até 0,75%", "Comentário": "Progressivo"},
        {"Faixa": "160% a 179,99%", "Fator": "0,75% até 0,78%", "Comentário": "Progressivo"},
        {"Faixa": "180% a 199,99%", "Fator": "0,78% até 0,80%", "Comentário": "Progressivo"},
        {"Faixa": "> 200%", "Fator": "0,80%", "Comentário": "Teto Fixo"},
        {"Faixa": "PIVÔS", "Fator": "Fixo 0,60%", "Comentário": "Pivô"}
    ],
    "Fernando": [
        {"Faixa": "0% a 19,99%", "Fator": "0,50%", "Comentário": "Faixa Fixa"},
        {"Faixa": "20% a 39,99%", "Fator": "0,50%", "Comentário": "Faixa Fixa"},
        {"Faixa": "40% a 59,99%", "Fator": "0,50%", "Comentário": "Faixa Fixa"},
        {"Faixa": "60% a 79,99%", "Fator": "0,50%", "Comentário": "Faixa Fixa"},
        {"Faixa": "80% a 99,99%", "Fator": "0,60%", "Comentário": "Faixa Fixa"},
        {"Faixa": "100% a 119,99%", "Fator": "0,70%", "Comentário": "Faixa Fixa"},
        {"Faixa": "120% a 139,99%", "Fator": "0,75%", "Comentário": "Faixa Fixa"},
        {"Faixa": "140% a 159,99%", "Fator": "0,80%", "Comentário": "Faixa Fixa"},
        {"Faixa": "160% a 179,99%", "Fator": "0,85%", "Comentário": "Faixa Fixa"},
        {"Faixa": "180% a 199,99%", "Fator": "0,90%", "Comentário": "Faixa Fixa"},
        {"Faixa": "> 200%", "Fator": "1,00%", "Comentário": "Faixa Fixa"},
        {"Faixa": "PIVÔS", "Fator": "Fixo 0,60%", "Comentário": "Pivô"}
    ],
    "Amandio": [
        {"Faixa": "0% a 19,99%", "Fator": "0,50%", "Comentário": "Fixo"},
        {"Faixa": "20% a 39,99%", "Fator": "0,50%", "Comentário": "Fixo"},
        {"Faixa": "40% a 59,99%", "Fator": "0,50%", "Comentário": "Fixo"},
        {"Faixa": "60% a 79,99%", "Fator": "0,50% até 0,60%", "Comentário": "Rampa Progressiva"},
        {"Faixa": "80% a 99,99%", "Fator": "0,60% até 0,70%", "Comentário": "Rampa Progressiva"},
        {"Faixa": "100% a 119,99%", "Fator": "0,70% até 0,75%", "Comentário": "Rampa Progressiva"},
        {"Faixa": "120% a 139,99%", "Fator": "0,75% até 0,80%", "Comentário": "Rampa Progressiva"},
        {"Faixa": "140% a 159,99%", "Fator": "0,80% até 0,85%", "Comentário": "Rampa Progressiva"},
        {"Faixa": "160% a 179,99%", "Fator": "0,85% até 0,90%", "Comentário": "Rampa Progressiva"},
        {"Faixa": "180% a 199,99%", "Fator": "0,90% até 1,00%", "Comentário": "Rampa Progressiva"},
        {"Faixa": "> 200%", "Fator": "1,00%", "Comentário": "Teto Rampa"},
        {"Faixa": "PIVÔS", "Fator": "Fixo 0,60%", "Comentário": "Pivô"}
    ]
}

# =========================================================
# UPLOAD
# =========================================================

arquivo_excel = st.file_uploader(
    "📥 Arraste e solte a base consolidada (.xlsx) aqui",
    type=["xlsx"]
)

if arquivo_excel is not None:
    
    # --- CARREGAMENTO DOS DADOS (Com Cache) ---
    @st.cache_data
    def carregar_todos_dados(file):
        xls = pd.ExcelFile(file)
        dados = {'individual': {}, 'resumo': {}}
        
        for nome_cenario, nome_aba in ABAS_INDIVIDUAL.items():
            if nome_aba in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=nome_aba)
                df.columns = df.columns.str.strip().str.lower()
                if 'competencia' in df.columns:
                    df['competencia_dt'] = pd.to_datetime(df['competencia'], errors='coerce')
                    df = df.dropna(subset=['competencia_dt'])
                    df['competencia_str'] = df['competencia_dt'].dt.strftime('%m/%Y')
                dados['individual'][nome_cenario] = df
                
        for nome_cenario, nome_aba in ABAS_RESUMO.items():
            if nome_aba in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=nome_aba)
                df.columns = df.columns.str.strip().str.lower()
                if 'competencia' in df.columns:
                    df['competencia_dt'] = pd.to_datetime(df['competencia'], errors='coerce')
                    df = df.dropna(subset=['competencia_dt'])
                    df['competencia_str'] = df['competencia_dt'].dt.strftime('%m/%Y')
                dados['resumo'][nome_cenario] = df
                
        return dados

    dados_completos = carregar_todos_dados(arquivo_excel)

    if not dados_completos['individual'] or not dados_completos['resumo']:
        st.error("❌ As abas necessárias não foram encontradas no arquivo. Verifique se o Excel possui as nomenclaturas corretas.")
        st.stop()

    lista_resumos = []
    for cenario, df in dados_completos['resumo'].items():
        df_temp = df.copy()
        df_temp['Cenário'] = cenario
        lista_resumos.append(df_temp)
    df_resumo_all = pd.concat(lista_resumos, ignore_index=True)
    df_resumo_clean = df_resumo_all[~df_resumo_all['faixa_atingimento'].astype(str).str.contains("total", case=False, na=False)]


    # --- FILTROS LATERAIS ---
    visao_escolhida = st.sidebar.radio(
        "👁️ Selecione a Visão Analítica:",
        ["Comparativo Geral (Os 3 Cenários)", "Lucas", "Amandio", "Fernando"]
    )

    st.sidebar.markdown("<hr/>", unsafe_allow_html=True)
    st.sidebar.markdown("**📅 Período de Análise:**")
    
    todas_competencias = sorted(dados_completos['individual']['Lucas']['competencia_str'].dropna().unique())
    
    col_data1, col_data2 = st.sidebar.columns(2)
    with col_data1:
        mes_inicial = st.selectbox("Início:", options=todas_competencias, index=0)
    with col_data2:
        mes_final = st.selectbox("Fim:", options=todas_competencias, index=len(todas_competencias)-1)

    idx_ini = todas_competencias.index(mes_inicial)
    idx_fim = todas_competencias.index(mes_final)

    if idx_ini > idx_fim:
        st.sidebar.error("⚠️ O mês inicial não pode ser posterior ao mês final.")
        st.stop()

    comps_selecionadas = todas_competencias[idx_ini:idx_fim+1]

    if visao_escolhida == "Comparativo Geral (Os 3 Cenários)":
        st.sidebar.markdown("<br>", unsafe_allow_html=True)
        st.sidebar.markdown("**📊 Cruzamento Específico:**")
        todas_faixas = sorted(df_resumo_clean['faixa_atingimento'].dropna().unique())
        faixas_selecionadas = st.sidebar.multiselect(
            "Filtrar por Faixa(s):", 
            options=todas_faixas, 
            default=todas_faixas,
            help="Desmarque faixas para isolar análises específicas nos gráficos de comparação."
        )


    # =========================================================================
    # VISÃO 1: COMPARATIVO GERAL
    # =========================================================================
    if visao_escolhida == "Comparativo Geral (Os 3 Cenários)":
        
        st.subheader("🏆 Comparativo de Impacto Final", divider="green")
        st.caption(f"Analisando o período filtrado: **{mes_inicial}** até **{mes_final}**")
        
        with st.expander("📖 Visualizar Políticas de Comissionamento Aplicadas", expanded=False):
            col_t1, col_t2, col_t3 = st.columns(3)
            with col_t1:
                st.markdown("<h4 style='text-align: center; color: #0B7A3E;'>Cenário LUCAS</h4>", unsafe_allow_html=True)
                st.dataframe(pd.DataFrame(TABELAS_REGRAS['Lucas']), use_container_width=True, hide_index=True)
            with col_t2:
                st.markdown("<h4 style='text-align: center; color: #0B7A3E;'>Cenário AMANDIO</h4>", unsafe_allow_html=True)
                st.dataframe(pd.DataFrame(TABELAS_REGRAS['Amandio']), use_container_width=True, hide_index=True)
            with col_t3:
                st.markdown("<h4 style='text-align: center; color: #0B7A3E;'>Cenário FERNANDO</h4>", unsafe_allow_html=True)
                st.dataframe(pd.DataFrame(TABELAS_REGRAS['Fernando']), use_container_width=True, hide_index=True)
        
        resumo_metricas = []
        for cenario, df_full in dados_completos['individual'].items():
            df = df_full[df_full['competencia_str'].isin(comps_selecionadas)]
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
            
        df_resumo_kpi = pd.DataFrame(resumo_metricas)
        
        cols = st.columns(3)
        qtd_meses = len(comps_selecionadas)
        for idx, row in df_resumo_kpi.iterrows():
            with cols[idx]:
                st.markdown(f"<h3 style='font-size: 20px;'>Cenário {row['Cenário'].upper()}</h3>", unsafe_allow_html=True)
                st.metric("Impacto Final (%)", f"{row['Impacto Final (%)']:.2f}%")
                st.metric("Aumento de Despesa", f"R$ {row['Aumento de Despesa (R$)']:,.2f}")
                valor_base = ((row['Pessoas na Garantia'] / qtd_meses) / 5889) * 100 if qtd_meses > 0 else 0
                st.metric("Necessidade de Garantia", f"{row['Pessoas na Garantia'] / qtd_meses:.0f} p/mês", f"{valor_base:.2f}% da equipe")
        
        st.write("")

        # --- SEÇÃO: ANÁLISE COMPARATIVA POR FAIXA ---
        st.subheader("🎯 Comparativo Detalhado por Faixa de Atingimento", divider="green")
        
        if not faixas_selecionadas:
            st.warning("⚠️ Selecione pelo menos uma Faixa de Atingimento no menu lateral.")
        else:
            df_res_filtrado = df_resumo_clean[
                (df_resumo_clean['competencia_str'].isin(comps_selecionadas)) &
                (df_resumo_clean['faixa_atingimento'].isin(faixas_selecionadas))
            ]
            
            df_agrupado_cenario = df_res_filtrado.groupby('Cenário').agg({
                'comissao total (cenario antigo)': 'sum',
                'custo real empresa (com garantia)': 'sum',
                'qtd pessoas na garantia': 'sum',
                'total pessoas (únicas)': 'sum',
                'faturamento total': 'sum'
            }).reset_index()
            
            df_agrupado_cenario['Custo Extra (R$)'] = df_agrupado_cenario['custo real empresa (com garantia)'] - df_agrupado_cenario['comissao total (cenario antigo)']
            df_agrupado_cenario['Custo Extra (R$)'] = df_agrupado_cenario['Custo Extra (R$)'].apply(lambda x: x if x > 0 else 0)
            df_agrupado_cenario['% na Garantia Médio'] = (df_agrupado_cenario['qtd pessoas na garantia'] / df_agrupado_cenario['total pessoas (únicas)']) * 100
            
            col_graf1, col_graf2 = st.columns(2)
            
            # Paleta de cores corporativa padronizada para os modelos
            cor_modelos = {"Lucas": "#0B7A3E", "Amandio": "#F2A900", "Fernando": "#005baa"}

            with col_graf1:
                fig_custo = px.bar(
                    df_agrupado_cenario, x='Cenário', y='Custo Extra (R$)', color='Cenário',
                    text_auto=".3s", title="Aumento de Custo (Nas faixas filtradas)",
                    template="plotly_white", color_discrete_map=cor_modelos
                )
                fig_custo.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False)
                fig_custo.update_layout(showlegend=False, xaxis_title="", yaxis_title="R$ Custo Adicional")
                st.plotly_chart(fig_custo, use_container_width=True)
                
            with col_graf2:
                fig_garantia = px.bar(
                    df_agrupado_cenario, x='Cenário', y='% na Garantia Médio', color='Cenário',
                    text_auto=".2f", title="% Base de Vendas Necessitando de Garantia",
                    template="plotly_white", color_discrete_map=cor_modelos
                )
                fig_garantia.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False)
                fig_garantia.update_layout(showlegend=False, xaxis_title="", yaxis_title="% da Equipe")
                st.plotly_chart(fig_garantia, use_container_width=True)
            
            with st.expander("📊 Abrir Detalhamento Financeiro em Tabela"):

                df_table_show = df_res_filtrado.groupby(['Cenário', 'faixa_atingimento']).agg({
                    'qtd pessoas na garantia': 'sum',
                    'comissao total (cenario antigo)': 'sum',
                    'custo real empresa (com garantia)': 'sum'
                }).reset_index()

                df_table_show['Custo Extra / Diferença (R$)'] = (
                    df_table_show['custo real empresa (com garantia)'] -
                    df_table_show['comissao total (cenario antigo)']
                )

                # formatação monetária
                df_table_show['custo real empresa (com garantia)'] = df_table_show['custo real empresa (com garantia)'].apply(lambda x: f"R$ {x:,.2f}")
                df_table_show['comissao total (cenario antigo)'] = df_table_show['comissao total (cenario antigo)'].apply(lambda x: f"R$ {x:,.2f}")
                df_table_show['Custo Extra / Diferença (R$)'] = df_table_show['Custo Extra / Diferença (R$)'].apply(lambda x: f"R$ {x:,.2f}")


                # função de cores por cenário
                def colorir_cenario(row):

                    if row['Cenário'] == "Lucas":
                        return ['background-color:#E8F5E9'] * len(row)

                    elif row['Cenário'] == "Amandio":
                        return ['background-color:#E3F2FD'] * len(row)

                    elif row['Cenário'] == "Fernando":
                        return ['background-color:#FFF3E0'] * len(row)

                    else:
                        return [''] * len(row)


                styled_df = df_table_show.style.apply(colorir_cenario, axis=1)

                st.dataframe(styled_df, use_container_width=True)

    # =========================================================================
    # VISÃO 2: ANÁLISE INDIVIDUAL PROFUNDA
    # =========================================================================
    else:
        df_estudo = dados_completos['individual'][visao_escolhida]
        
        st.subheader(f"🔍 Análise Modelo {visao_escolhida.upper()}", divider="green")
        st.caption(f"Analisando o período filtrado: **{mes_inicial}** até **{mes_final}**")
        
        with st.expander(f"📌 Visualizar Tabela de Comissionamento ({visao_escolhida})", expanded=False):
            st.dataframe(pd.DataFrame(TABELAS_REGRAS[visao_escolhida]), use_container_width=True, hide_index=True)
            
        df_filtrado = df_estudo[df_estudo['competencia_str'].isin(comps_selecionadas)]

        # --- Gráficos lado a lado para aproveitar o layout "wide" ---
        

        # --- GRÁFICO 1 ---
        st.markdown("**1. Dispersão: Pagamento Atual vs Nova Regra**")

        LIMITE_VISUAL = 6000

        fig_scatter = px.scatter(
            df_filtrado,
            x="comissão individual",
            y="comissao_final_garantida",
            color="cargo",
            hover_data={"nome": True, "ganho_nominal": ":.2f", "%atingimento_meta": ":.2f"},
            labels={
                "comissão individual": "Atual (R$)",
                "comissao_final_garantida": "Novo (R$)"
            },
            template="plotly_white",
            range_x=[0, LIMITE_VISUAL],
            range_y=[0, LIMITE_VISUAL]
        )

        # Linha Break-even
        fig_scatter.add_shape(
            type="line",
            line=dict(dash="dash", color="#d9534f", width=2),
            x0=0, y0=0,
            x1=LIMITE_VISUAL, y1=LIMITE_VISUAL
        )

        fig_scatter.add_annotation(
            x=LIMITE_VISUAL * 0.70,
            y=LIMITE_VISUAL * 0.95,
            text=" ",
            showarrow=False,
            font=dict(color="#0B7A3E", size=12)
        )

        fig_scatter.update_layout(
            showlegend=False
        )

        st.plotly_chart(fig_scatter, use_container_width=True)


        # --- GRÁFICO 2 ---
        st.markdown("**2. Volume de Colaboradores por Faixa de Ganho Extra**")

        df_barras = df_filtrado.copy()

        cortes = [-1, 0.01, 99.99, 300.99, 500.99, 1000.99, float('inf')]
        nomes_grupos = [
            "R$ 0 (Garantia)",
            "R$ 1 a 99",
            "R$ 100 a 300",
            "R$ 301 a 500",
            "R$ 501 a 1000",
            "> R$ 1000"
        ]

        df_barras['grupo_ganho'] = pd.cut(
            df_barras['ganho_nominal'],
            bins=cortes,
            labels=nomes_grupos
        )

        df_resumo_ganhos = df_barras.groupby(
            ['competencia_str', 'grupo_ganho']
        ).size().reset_index(name='Quantidade')

        df_resumo_ganhos['grupo_ganho'] = pd.Categorical(
            df_resumo_ganhos['grupo_ganho'],
            categories=nomes_grupos,
            ordered=True
        )

        df_resumo_ganhos = df_resumo_ganhos.sort_values(
            ['competencia_str', 'grupo_ganho']
        )

        fig_barras = px.bar(
            df_resumo_ganhos,
            x='competencia_str',
            y='Quantidade',
            color='grupo_ganho',
            barmode='group',
            labels={
                "competencia_str": "Mês",
                "grupo_ganho": "Faixa de Ganho"
            },
            template="plotly_white",
            color_discrete_sequence=["#B0BEC5", "#63B3ED", "#20C997", "#F6C23E", "#FD7E14", "#6F42C1"]
        )

        fig_barras.update_layout(
            xaxis_type='category',
            legend_title="Ganho Extra (R$)"
        )

        st.plotly_chart(fig_barras, use_container_width=True)

        # =========================================================================
        # SEÇÃO 3: PROJEÇÃO FINANCEIRA GLOBAL
        # =========================================================================
        st.subheader("3. Projeção Financeira e Payback Global (Turnover Limite: 3.960)", divider="green")
        st.info("💡 **Nota:** Esta projeção é um modelo anual preditivo global. Ela considera a média de todo o histórico da base de dados fornecida e **NÃO** sofre alterações pelos filtros de data selecionados.")
        
        total_num_all_meses = df_estudo["competencia_dt"].nunique()
        ultima_comp_global = df_estudo["competencia_dt"].max()
        
        if ultima_comp_global is not None:
            total_num_colab_headcount = len(df_estudo[df_estudo["competencia_dt"] == ultima_comp_global])
        else:
            total_num_colab_headcount = 0
            
        if total_num_colab_headcount == 0 and total_num_all_meses > 0: 
            total_num_colab_headcount = len(df_estudo) / total_num_all_meses

        global_custo_mensal_atual = df_estudo["comissão individual"].sum() / total_num_all_meses if total_num_all_meses > 0 else 0
        global_custo_mensal_meritocratico = df_estudo["vl_comissao_cenario"].sum() / total_num_all_meses if total_num_all_meses > 0 else 0
        global_garantia_mensal_inicial = df_estudo["investimento_protecao"].sum() / total_num_all_meses if total_num_all_meses > 0 else 0

        saidas_mes_simul = 150
        meses_simul_range = np.arange(0, 120)
        custos_novos_simul, economias_acumuladas_simul = [], []

        for mes in meses_simul_range:
            turnover_acumulado_simul = min(mes * saidas_mes_simul, 3960)
            qtd_com_garantia_simul = max(0, total_num_colab_headcount - turnover_acumulado_simul)
            proporcao_ativos_simul = qtd_com_garantia_simul / total_num_colab_headcount if total_num_colab_headcount > 0 else 0
            
            garantia_no_mes_simul = global_garantia_mensal_inicial * proporcao_ativos_simul
            custo_total_mes_simul = global_custo_mensal_meritocratico + garantia_no_mes_simul
            custos_novos_simul.append(custo_total_mes_simul)

            if mes == 0:
                economias_acumuladas_simul.append(0)
            else:
                saldo_mes_simul = global_custo_mensal_atual - custo_total_mes_simul
                economias_acumuladas_simul.append(economias_acumuladas_simul[-1] + saldo_mes_simul)

        df_proj_global = pd.DataFrame({
            "Mês": meses_simul_range, 
            "Novo Custo Total": custos_novos_simul, 
            "Custo Atual Médio": [global_custo_mensal_atual] * len(meses_simul_range), 
            "Economia Acumulada": economias_acumuladas_simul
        })

        col_glob1, col_glob2 = st.columns(2)
        
        with col_glob1:
            fig_proj_glob = px.line(
                df_proj_global, x="Mês", y=["Novo Custo Total", "Custo Atual Médio"], 
                title="Evolução do Custo Mensal (R$)", template="plotly_white",
                color_discrete_map={"Novo Custo Total": "#0B7A3E", "Custo Atual Médio": "#6c757d"}
            )
            fig_proj_glob.add_hline(y=global_custo_mensal_atual, line_dash="dash", line_color="#d9534f", annotation_text="Teto do Custo Atual")
            fig_proj_glob.update_traces(hovertemplate='Mês %{x}<br>R$ %{y:,.2f}')
            fig_proj_glob.update_layout(yaxis_title="Investimento Mensal (R$)", legend_title="", hovermode="x unified")
            st.plotly_chart(fig_proj_glob, use_container_width=True)

        with col_glob2:
            fig_payback_glob = px.bar(
                df_proj_global, x="Mês", y="Economia Acumulada", title="Retorno sobre Investimento (Payback)", 
                template="plotly_white", color="Economia Acumulada", color_continuous_scale=px.colors.diverging.RdYlGn
            )
            fig_payback_glob.add_hline(y=0, line_dash="solid", line_color="black", line_width=1.5)
            fig_payback_glob.update_traces(hovertemplate='Mês %{x}<br>Saldo R$ %{y:,.2f}')
            fig_payback_glob.update_layout(yaxis_title="Saldo Caixa Acumulado (R$)", coloraxis_showscale=False)
            st.plotly_chart(fig_payback_glob, use_container_width=True)

        payback_mes_glob = next((m for m, v in enumerate(custos_novos_simul) if v <= global_custo_mensal_atual), "Nunca")
        st.markdown(f"**Resumo Estratégico do Cenário Global:** Base Ativa de **{total_num_colab_headcount:.0f}** colaboradores | Custo Médio Atual de **R$ {global_custo_mensal_atual:,.2f}** | Ponto de Equilíbrio Projetado: **Mês {payback_mes_glob}**")

import streamlit as st
import json

# ===== FUNÇÕES =====
def calcular_alvenaria(altura, largura):
    return altura * largura


def calcular_revestimento(comprimento, largura):
    return comprimento * largura


# ===== CONFIG =====
st.set_page_config(page_title="Orçamento de Obras", layout="centered")

st.title("🏗️ Orçamento de Obras")

# ===== MEMÓRIA =====
if "dados_obra" not in st.session_state:
    st.session_state.dados_obra = []

# ===== NOME DA OBRA =====
nome_obra = st.text_input("Nome da Obra")

# ===== ESCOLHA =====
tipo = st.radio("O que deseja calcular?", ("Alvenaria", "Revestimento"))

st.divider()

# ===== ALVENARIA =====
if tipo == "Alvenaria":

    st.subheader("🧱 Dados da Alvenaria")

    col1, col2 = st.columns(2)

    with col1:
        altura = st.number_input("Altura (m)", min_value=0.0)
        largura = st.number_input("Largura (m)", min_value=0.0)

    with col2:
        preco_bloco = st.number_input("Preço do bloco (R$)", min_value=0.0)
        ambiente = st.text_input("Ambiente")

    if st.button("Calcular Alvenaria"):

        if ambiente == "":
            st.error("Digite o nome do ambiente")
        else:
            area = calcular_alvenaria(altura, largura)

            rendimento_bloco = 25
            qtd_blocos = int(area * rendimento_bloco)
            custo_total = qtd_blocos * preco_bloco

            st.success("Cálculo realizado!")

            st.metric("Área (m²)", f"{area:.2f}")
            st.metric("Blocos", f"{qtd_blocos}")
            st.metric("Custo Total (R$)", f"{custo_total:.2f}")

            st.session_state.dados_obra.append({
                "Ambiente": ambiente,
                "Tipo": "Alvenaria",
                "Área": area,
                "Quantidade": qtd_blocos,
                "Unidade": "blocos",
                "Custo": custo_total
            })

# ===== REVESTIMENTO =====
if tipo == "Revestimento":

    st.subheader("🟦 Dados do Revestimento")

    col1, col2 = st.columns(2)

    with col1:
        comprimento = st.number_input("Comprimento (m)", min_value=0.0)
        largura = st.number_input("Largura (m)", min_value=0.0)
        ambiente = st.text_input("Ambiente")

    with col2:
        preco_m2 = st.number_input("Preço por m² (R$)", min_value=0.0)
        perda = st.number_input("Perda (%)", min_value=0.0, value=10.0)

    if st.button("Calcular Revestimento"):

        if ambiente == "":
            st.error("Digite o nome do ambiente")
        else:
            area = calcular_revestimento(comprimento, largura)

            area_final = area * (1 + perda / 100)
            custo_total = area_final * preco_m2

            st.success("Cálculo realizado!")

            st.metric("Área (m²)", f"{area:.2f}")
            st.metric("Área final", f"{area_final:.2f}")
            st.metric("Custo Total (R$)", f"{custo_total:.2f}")

            st.session_state.dados_obra.append({
                "Ambiente": ambiente,
                "Tipo": "Revestimento",
                "Área": area_final,
                "Quantidade": area_final,
                "Unidade": "m²",
                "Custo": custo_total
            })

# ===== LISTA =====
st.divider()
st.subheader("📋 Resumo da Obra")

for i, item in enumerate(st.session_state.dados_obra):

    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])

    with col1:
        st.write(f"**{item['Ambiente']}** - {item['Tipo']}")

    with col2:
        if item["Unidade"] == "blocos":
            st.write(f"{int(item['Quantidade'])} blocos")
        else:
            st.write(f"{item['Quantidade']:.2f} m²")

    with col3:
        st.write(f"R$ {item['Custo']:.2f}")

    with col4:
        if st.button("✏️", key=f"edit_{i}"):
            st.session_state["editando"] = i

    with col5:
        if st.button("❌", key=f"del_{i}"):
            st.session_state.dados_obra.pop(i)
            st.rerun()

# ===== EDITAR =====
if "editando" in st.session_state:
    i = st.session_state["editando"]
    item = st.session_state.dados_obra[i]

    st.subheader("✏️ Editar Item")

    novo_ambiente = st.text_input("Ambiente", value=item["Ambiente"])
    nova_qtd = st.number_input("Quantidade", value=float(item["Quantidade"]))
    novo_custo = st.number_input("Custo", value=float(item["Custo"]))

    if st.button("Salvar"):
        item["Ambiente"] = novo_ambiente
        item["Quantidade"] = nova_qtd
        item["Custo"] = novo_custo

        del st.session_state["editando"]
        st.rerun()

# ===== TOTAL =====
total = sum(item["Custo"] for item in st.session_state.dados_obra)

st.subheader("💰 Total da Obra")
st.success(f"R$ {total:.2f}")

# ===== SALVAR JSON =====
if st.button("💾 Salvar Orçamento"):
    with open("orcamento.json", "w") as f:
        json.dump(st.session_state.dados_obra, f)
    st.success("Orçamento salvo!")

# ===== LIMPAR =====
if st.button("🗑️ Limpar Tudo"):
    st.session_state.dados_obra = []
    st.rerun()
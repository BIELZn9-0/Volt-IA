import streamlit as st
from google import genai

# Configuração da página (agora forçando a barra lateral a abrir)
st.set_page_config(page_title="Ia Studio", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>""", unsafe_allow_html=True)

if "tela_atual" not in st.session_state:
    st.session_state.tela_atual = "login"
if "banco_de_dados" not in st.session_state:
    st.session_state.banco_de_dados = {"kaio": "123"}

# -----------------------------------------
# TELAS DE LOGIN E CADASTRO (Mantidas iguais)
# -----------------------------------------
if st.session_state.tela_atual == "login":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Acesso ao Sistema: Ia")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Entrar", use_container_width=True):
                if usuario in st.session_state.banco_de_dados and st.session_state.banco_de_dados[usuario] == senha:
                    st.session_state.tela_atual = "chat"
                    st.rerun()
                else:
                    st.error("❌ Acesso negado!")
        with btn_col2:
            if st.button("Criar Conta", use_container_width=True):
                st.session_state.tela_atual = "cadastro"
                st.rerun()

elif st.session_state.tela_atual == "cadastro":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Criar Nova Chave 🔑")
        novo_usuario = st.text_input("Novo Usuário")
        nova_senha = st.text_input("Nova Senha", type="password")
        if st.button("Cadastrar", use_container_width=True):
            if novo_usuario and nova_senha:
                st.session_state.banco_de_dados[novo_usuario] = nova_senha
                st.success("✅ Conta criada! Clique em Voltar.")
        if st.button("Voltar", use_container_width=True):
            st.session_state.tela_atual = "login"
            st.rerun()

# -----------------------------------------
# TELA 3: O CHAT (AGORA COM BARRA LATERAL!)
# -----------------------------------------
elif st.session_state.tela_atual == "chat":
    
    # --- BARRA LATERAL (SIDEBAR) ---
    with st.sidebar:
        st.title("⚡ Menu")
        
        # Botão de Novo Chat (Apaga a memória da conversa atual)
        if st.button("➕ Novo Chat", use_container_width=True):
            st.session_state.mensagens = []
            st.session_state.chat = st.session_state.client.chats.create(model='gemini-2.5-flash')
            st.rerun()
            
        st.divider()
        st.write("Recentes:")
        # Criando botões falsos só para dar o visual de histórico (como no Gemini)
        st.button("💬 Teste", use_container_width=True)
        st.button("💬 Teste 2", use_container_width=True)
        st.button("💬 Teste 3", use_container_width=True)
        
        st.divider()
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.tela_atual = "login"
            st.rerun()

    # --- ÁREA PRINCIPAL DO CHAT ---
    st.markdown("### Sistema Principal")

    # ATENÇÃO: COLOQUE SUA CHAVE AQUI
    if "client" not in st.session_state:
        st.session_state.client = genai.Client(api_key="CHAVE_GOOGLE")
    if "chat" not in st.session_state:
        st.session_state.chat = st.session_state.client.chats.create(model='gemini-2.5-flash')
    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []

    for msg in st.session_state.mensagens:
        icone = "🧑‍💻" if msg["papel"] == "user" else "✨"
        with st.chat_message(msg["papel"], avatar=icone):
            st.write(msg["texto"])

    pergunta = st.chat_input("Pergunte algo para mim")
    if pergunta:
        st.chat_message("user", avatar="🧑").write(pergunta)
        st.session_state.mensagens.append({"papel": "user", "texto": pergunta})
        
        with st.spinner("Analisando..."):
            resposta = st.session_state.chat.send_message(pergunta)
            
        st.chat_message("assistant", avatar="🤖").write(resposta.text)
        st.session_state.mensagens.append({"papel": "assistant", "texto": resposta.text})

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def buscar_vagas_links():
    print("🔎 Iniciando busca de oportunidades...")
    
    # Exemplo: Buscando no site de vagas (ajustado para ser leve)
    # Nota: LinkedIn/Indeed exigem headers para não bloquearem
    url = "https://www.trabalhabrasil.com.br/vagas-vagas-em-sao-paulo-sp/estagio-ti"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    novas_vagas = []
    
    # Lógica de extração de tags (exemplo para o site Trabalha Brasil)
    cards = soup.find_all('div', class_='jg-vagas')[:5] # Pega as 5 primeiras
    
    for card in cards:
        titulo = card.find('h2').text.strip()
        link = "https://www.trabalhabrasil.com.br" + card.find('a')['href']
        empresa = "Confidencial" # Muitos sites ocultam na vitrine
        
        # Filtro de interesse
        if any(keyword in titulo.lower() for keyword in ["dados", "ti", "estágio", "assistente"]):
            novas_vagas.append({
                "Data": datetime.now().strftime("%d/%m/%Y"),
                "Título": titulo,
                "Empresa": empresa,
                "Link": link
            })
            
    return novas_vagas

def atualizar_base(vagas):
    arquivo = "vagas_consolidado.csv"
    df_novas = pd.DataFrame(vagas)
    
    if not os.path.isfile(arquivo):
        df_novas.to_csv(arquivo, index=False, encoding='utf-8-sig')
    else:
        df_existente = pd.read_csv(arquivo)
        # Evita duplicar links que já salvamos
        df_final = pd.concat([df_existente, df_novas]).drop_duplicates(subset=['Link'], keep='first')
        df_final.to_csv(arquivo, index=False, encoding='utf-8-sig')
    
    print(f"📊 Planilha atualizada! Total de vagas na base: {len(pd.read_csv(arquivo))}")

if __name__ == "__main__":
    vagas_encontradas = buscar_vagas_links()
    if vagas_encontradas:
        atualizar_base(vagas_encontradas)
    else:
        print("📭 Nenhuma vaga nova compatível hoje.")
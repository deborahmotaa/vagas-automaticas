import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

def buscar_vagas_links():
    print("🔎 Iniciando busca turbinada de oportunidades...")
    
    # Lista de termos que você aceita (ampliada para garantir resultados)
    termos_interesse = [
        "dados", "data", "ti", "it", "estágio", "estagiário", 
        "assistente", "auxiliar", "junior", "júnior", "python", "excel"
    ]
    
    # Site de busca (Trabalha Brasil é bom para automação simples)
    url = "https://www.trabalhabrasil.com.br/vagas-vagas-em-sao-paulo-sp/estagio-ti"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        novas_vagas = []
        
        # Encontra os cards de vagas
        cards = soup.find_all('div', class_='jg-vagas')
        
        for card in cards:
            titulo = card.find('h2').text.strip()
            link = "https://www.trabalhabrasil.com.br" + card.find('a')['href']
            
            # Filtro Dinâmico: Se qualquer palavra da nossa lista estiver no título, a gente quer!
            if any(termo in titulo.lower() for termo in termos_interesse):
                novas_vagas.append({
                    "Data": datetime.now().strftime("%d/%m/%Y"),
                    "Título": titulo,
                    "Empresa": "Ver no link",
                    "Link": link
                })
        
        return novas_vagas

    except Exception as e:
        print(f"❌ Erro na busca: {e}")
        return []

def atualizar_base(vagas):
    arquivo = "vagas_consolidado.csv"
    df_novas = pd.DataFrame(vagas)
    
    if not os.path.isfile(arquivo):
        df_novas.to_csv(arquivo, index=False, encoding='utf-8-sig')
    else:
        df_existente = pd.read_csv(arquivo)
        # Remove duplicatas baseadas no Link para não encher a planilha de repetidos
        df_final = pd.concat([df_existente, df_novas]).drop_duplicates(subset=['Link'], keep='first')
        df_final.to_csv(arquivo, index=False, encoding='utf-8-sig')
    
    print(f"✅ Sucesso! Total de vagas na sua base: {len(pd.read_csv(arquivo))}")

if __name__ == "__main__":
    vagas_reais = buscar_vagas_links()
    
    if vagas_reais:
        atualizar_base(vagas_reais)
    else:
        print("📭 Nenhuma vaga nova encontrada com os filtros atuais.")
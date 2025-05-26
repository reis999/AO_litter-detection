# Dicionário completo de classes para ecoponto
category_to_bin = {
    # Plástico e Metal (Ecoponto Amarelo)
    "Aluminium foil": "Amarelo - Plástico/Metal",
    "Aluminium blister pack": "Amarelo - Plástico/Metal",
    "Other plastic bottle": "Amarelo - Plástico/Metal",
    "Clear plastic bottle": "Amarelo - Plástico/Metal",
    "Plastic bottle cap": "Amarelo - Plástico/Metal",
    "Metal bottle cap": "Amarelo - Plástico/Metal",
    "Food Can": "Amarelo - Plástico/Metal",
    "Aerosol": "Amarelo - Plástico/Metal (vazio)",
    "Drink can": "Amarelo - Plástico/Metal",
    "Plastic lid": "Amarelo - Plástico/Metal",
    "Metal lid": "Amarelo - Plástico/Metal",
    "Other plastic": "Amarelo - Plástico/Metal",
    "Plastic film": "Amarelo - Plástico/Metal",
    "Six pack rings": "Amarelo - Plástico/Metal",
    "Single-use carrier bag": "Amarelo - Plástico/Metal",
    "Polypropylene bag": "Amarelo - Plástico/Metal",
    "Crisp packet": "Amarelo - Plástico/Metal",
    "Spread tub": "Amarelo - Plástico/Metal",
    "Tupperware": "Amarelo - Plástico/Metal",
    "Disposable food container": "Amarelo - Plástico/Metal",
    "Other plastic container": "Amarelo - Plástico/Metal",
    "Plastic glooves": "Amarelo - Plástico/Metal",
    "Plastic utensils": "Amarelo - Plástico/Metal",
    "Pop tab": "Amarelo - Plástico/Metal",
    "Scrap metal": "Amarelo - Plástico/Metal",
    "Squeezable tube": "Amarelo - Plástico/Metal (vazio)",
    "Plastic straw": "Amarelo - Plástico/Metal",
    
    # Papel e Cartão (Ecoponto Azul)
    "Toilet tube": "Azul - Papel/Cartão",
    "Other carton": "Azul - Papel/Cartão",
    "Egg carton": "Azul - Papel/Cartão",
    "Corrugated carton": "Azul - Papel/Cartão",
    "Paper cup": "Azul - Papel/Cartão (limpo)",
    "Magazine paper": "Azul - Papel/Cartão",
    "Wrapping paper": "Azul - Papel/Cartão",
    "Normal paper": "Azul - Papel/Cartão",
    "Paper bag": "Azul - Papel/Cartão",
    "Paper straw": "Azul - Papel/Cartão",
    
    # Vidro (Ecoponto Verde)
    "Glass bottle": "Verde - Vidro",
    "Broken glass": "Verde - Vidro",
    "Glass cup": "Verde - Vidro",
    "Glass jar": "Verde - Vidro",
    
    # Resíduos Específicos/Especiais
    "Battery": "Pilhão/Ponto Eletrão",
    "Carded blister pack": "Pilhão/Ponto Eletrão",
    "Drink carton": "Amarelo - Embalagens (ECAL)",
    "Meal carton": "Amarelo - Embalagens (ECAL)",
    
    # Resíduos Indiferenciados (Lixo Comum)
    "Pizza box": "Comum (se sujo)/Azul (se limpo)",
    "Disposable plastic cup": "Amarelo - Plástico/Metal",
    "Foam cup": "Comum",
    "Other plastic cup": "Amarelo - Plástico/Metal",
    "Food waste": "Castanho - Orgânico/Comum",
    "Tissues": "Comum",
    "Plastified paper bag": "Comum",
    "Garbage bag": "Comum",
    "Other plastic wrapper": "Amarelo - Plástico/Metal",
    "Foam food container": "Comum",
    "Rope & strings": "Comum",
    "Shoe": "Ecocentro/Ponto de Recolha",
    "Styrofoam piece": "Comum",
    "Unlabeled litter": "Comum (Verificar)",
    "Cigarette": "Comum"
}

# Cores para visualização (BGR)
bin_colors = {
    "Amarelo": (0, 255, 255), 
    "Azul": (255, 0, 0),
    "Verde": (0, 255, 0),
    "Comum": (128, 128, 128),
    "Pilhão": (0, 0, 255),
    "Ponto Eletrão": (165, 42, 42),
    "Castanho": (0, 75, 150),
    "Ecocentro": (255, 165, 0)
}

# Informações adicionais sobre reciclagem em Portugal
recycling_info = {
    "Amarelo": "Ecoponto Amarelo: Para embalagens de plástico e metal.",
    "Azul": "Ecoponto Azul: Para papel e cartão.",
    "Verde": "Ecoponto Verde: Para vidro.",
    "Comum": "Contentor de resíduos indiferenciados.",
    "Pilhão": "Pilhão: Para pilhas e baterias.",
    "Ponto Eletrão": "Ponto Eletrão: Para equipamentos elétricos e eletrónicos.",
    "Castanho": "Contentor Castanho: Para resíduos orgânicos (disponível em alguns municípios).",
    "Ecocentro": "Ecocentro: Para resíduos de maior dimensão ou especiais."
}

def get_bin_color(category_bin):
    # Extrai o tipo principal do ecoponto
    main_bin = category_bin.split(" - ")[0]
    return bin_colors.get(main_bin, (255, 255, 255))

def get_advice(category_name):
    """Retorna conselhos específicos para determinados materiais"""
    advice = ""
    name = category_name.lower()

    if "bottle" in name or "can" in name:
        advice = "Esvaziar e espalmar antes de reciclar."
    elif "glass" in name:
        advice = "Remover tampas antes de reciclar. Não colocar loiça ou espelhos."
    elif "pizza box" in name:
        advice = "Se estiver sujo com gordura, vai para o lixo comum."
    elif "battery" in name or "blister" in name:
        advice = "Nunca colocar em lixo comum! Levar ao Pilhão ou Ponto Eletrão."
    elif "aerosol" in name or "squeezable tube" in name:
        advice = "Certificar que está vazio antes de reciclar."
    elif "cup" in name:
        if "plastic" in name:
            advice = "Pode ir para o ecoponto amarelo, se estiver limpo."
        elif "foam" in name:
            advice = "Vai para o lixo comum. Não reciclável."
        elif "paper" in name:
            advice = "Reciclável no azul, se não estiver plastificado ou sujo."
        elif "glass" in name:
            advice = "Evitar loiça de vidro no ecoponto verde. Verificar se é reciclável."
    elif "bag" in name:
        if "plastic" in name or "carrier" in name or "polypropylene" in name:
            advice = "Utilizar várias vezes antes de reciclar no amarelo."
        elif "paper" in name:
            advice = "Reciclar no azul se estiver limpo e sem gordura."
        elif "garbage" in name:
            advice = "Lixo comum. Não reciclável."
        elif "plastified" in name:
            advice = "Vai para o lixo comum. Papel plastificado não é reciclável."
    elif "straw" in name:
        advice = "Prefira reutilizáveis. Reciclar conforme o material (papel/plástico)."
    elif "film" in name or "wrapper" in name:
        advice = "Verificar se é reciclável. Em caso de dúvida, colocar no comum."
    elif "shoe" in name:
        advice = "Levar a um ponto de recolha ou ecocentro."
    elif "tissues" in name:
        advice = "Lixo comum. Não reciclável devido a contaminação orgânica."
    elif "food waste" in name:
        advice = "Se disponível, usar contentor castanho (resíduos orgânicos)."
    elif "carton" in name:
        if "meal" in name or "drink" in name:
            advice = "Vai para o amarelo. Esvaziar antes de reciclar."
        else:
            advice = "Reciclável no azul se estiver limpo."
    elif "electronic" in name or "scrap metal" in name:
        advice = "Levar ao ecocentro ou ponto eletrão apropriado."
    elif "tub" in name or "container" in name or "tupperware" in name:
        advice = "Esvaziar e limpar antes de colocar no ecoponto amarelo."
    elif "foil" in name:
        advice = "Evitar colocar folhas muito sujas. Esfregar ou descartar se estiver com gordura."
    elif "metal lid" in name or "plastic lid" in name:
        advice = "Separar da embalagem principal antes de reciclar."
    elif "pop tab" in name:
        advice = "Pode reciclar junto com a lata, mas preferencialmente separado."
    elif "glove" in name:
        advice = "Se estiver sujo, colocar no lixo comum. Caso contrário, pode ir para o amarelo."
    elif "utensil" in name:
        advice = "Evitar descartáveis. Se limpos, podem ser reciclados no amarelo."
    elif "cigarette" in name:
        advice = "Nunca deitar no chão. Colocar no lixo comum."
    elif "rope" in name or "string" in name:
        advice = "Não reciclável. Colocar no lixo comum."
    elif "magazine" in name or "normal paper" in name:
        advice = "Evitar papéis plastificados. Retirar agrafos se possível."
    elif "jar" in name:
        advice = "Remover tampa e lavar se possível antes de reciclar no vidro."
    elif "unlabeled litter" in name:
        advice = "Categoria não reconhecida. Verificar manualmente destino adequado."
    elif "egg carton" in name:
        advice = "Pode ser reciclado no azul se for de cartão. Se for de esferovite, vai para o comum."

    return advice

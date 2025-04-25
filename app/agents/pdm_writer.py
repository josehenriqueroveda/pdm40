import openai


class PDMWriter:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def write_pdm(self, description: str) -> str:
        try:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "Você é um especialista em engenharia de materiais e cadastro técnico de itens em sistemas ERP como o SAP. "
                        "Sua tarefa é gerar descrições técnicas curtas e padronizadas para materiais seguindo normas técnicas brasileiras. "
                        "Nunca inclua comentários, apenas a descrição final do item."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "A partir da solicitação de material abaixo, gere um PDM (Padrão Descritivo do Material) conforme normas técnicas brasileiras, com as seguintes regras:\n\n"
                        "- A descrição deve ter no máximo 40 caracteres.\n"
                        "- Deve estar em CAIXA ALTA.\n"
                        "- Sem acentos ou sinais diacríticos (ex: NÃO usar ç, á, ê, etc.)\n"
                        "- Não use caracteres especiais ou pontuação.\n"
                        "- Não use artigos ou preposições.\n"
                        "- Apenas letras (A-Z) e números (0-9) são permitidos.\n"
                        "- Use apenas abreviações reconhecidas e padronizadas (ex: 'KG' para quilograma, 'MM' para milímetro)."
                        "- Ordem lógica: começar com a característica mais relevante (ex: tipo do material → forma → dimensão → uso).\n"
                        "- Não usar nomes comerciais ou marcas.\n"
                        "- Evitar redundâncias e subjetividades (ex: ALTA QUALIDADE, NOVO, PADRÃO).\n"
                        "- Seja claro e técnico.\n"
                        "- Não inclua comentários ou explicações.\n"
                        "- A resposta deve conter apenas a string final do PDM, nada mais.\n\n"
                        f"Solicitação:\n{description}"
                    ),
                },
            ]
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0,
                max_tokens=60,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["\n"],
            )

            pdm = response.choices[0].message.content.strip()
            pdm = pdm.upper()

            if len(pdm) > 40:
                pdm = pdm[:40]
            return pdm
        except Exception as e:
            print(f"Error: {e}")
            return None

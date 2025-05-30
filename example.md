Requests Example of All Pages:

Method: POST
Endpoint: http://127.0.0.1:12315/api
Headers: Authorization - Bearer auth254
Body:
{
"method": "logseq.Editor.getAllPages"
}
Response:
[
{
"id": 9031,
"createdAt": 1747778845769,
"journal?": false,
"name": "luiz paulo fávero",
"originalName": "Luiz Paulo Fávero",
"updatedAt": 1747778845769,
"uuid": "682cfd1d-2604-495f-a4c5-67ab64f03913"
},
{
"id": 12160,
"createdAt": 1747778857784,
"journal?": false,
"name": "vídeos do tcc",
"originalName": "Vídeos do TCC",
"updatedAt": 1747778857784,
"uuid": "682fa28b-1e93-472a-b043-f1b9dda11670"
},
{
"properties": {
"relacionado": "",
"curso": [
"MBA Engenharia de Software"
],
"tags": "",
"tecnologias": [
"HTML",
"CSS"
],
"tipo": [
"aula"
],
"professor": [
"Guilherme Bezerra de Lima"
],
"livros": [
"Código Limpo"
],
"data": [
"May 7th, 2024"
],
"materia": [
"Módulo Introdutório"
]
},
"updatedAt": 1747778835932,
"createdAt": 1747778835932,
"id": 3160,
"propertiesTextValues": {
"relacionado": "",
"curso": "[[MBA Engenharia de Software]]",
"tags": "",
"tecnologias": "[[HTML]], [[CSS]]",
"tipo": "#aula",
"professor": "[[Guilherme Bezerra de Lima]]",
"livros": "[[Código Limpo]]",
"data": "[[May 7th, 2024]]",
"materia": "[[Módulo Introdutório]]"
},
"name": "desenvolvimento frontend i",
"uuid": "682cfd13-76e0-4150-a33a-4e8d2af27b2b",
"journal?": false,
"originalName": "Desenvolvimento Frontend I",
"file": {
"id": 3159
}
},
]

Requests Example of Page Blocks:

Method: POST
Endpoint: http://127.0.0.1:12315/api
Headers: Authorization - Bearer auth254
Body:
{
"method": "logseq.Editor.getPageBlocksTree",
"args": [
"IoT I"
]
}
Response:
[
{
"properties": {
"relacionado": "",
"curso": [
"MBA Engenharia de Software"
],
"tags": "",
"tecnologias": "",
"tipo": [
"aula"
],
"professor": [
"Fernando Henrique Vieira Trindade"
],
"livros": "",
"ordem": "",
"data": [
"Apr 24th, 2025"
],
"materia": [
"IoT I"
]
},
"parent": {
"id": 7605
},
"children": [
{
"properties": {
"heading": 1
},
"parent": {
"id": 7618
},
"children": [
{
"parent": {
"id": 7633
},
"children": [],
"id": 7623,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 3,
"uuid": "682cfd1c-97da-4bb5-85ff-ea31ea8281b7",
"content": "",
"page": {
"id": 7605
},
"left": {
"id": 7633
},
"format": "markdown"
}
],
"id": 7633,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 2,
"uuid": "682cfd1c-17e4-4f33-aa6a-77cb59d85024",
"content": "# Resumo",
"page": {
"id": 7605
},
"propertiesOrder": [],
"left": {
"id": 7618
},
"format": "markdown"
},
{
"properties": {
"heading": 1
},
"parent": {
"id": 7618
},
"children": [
{
"parent": {
"id": 7627
},
"children": [],
"id": 7622,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 3,
"uuid": "682cfd1c-a83b-4992-af8c-bb0be6136307",
"content": "",
"page": {
"id": 7605
},
"left": {
"id": 7627
},
"format": "markdown"
}
],
"id": 7627,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 2,
"uuid": "682cfd1c-7874-40e8-8f43-a4f7b0841754",
"content": "# Material Complementar",
"page": {
"id": 7605
},
"propertiesOrder": [],
"left": {
"id": 7633
},
"format": "markdown"
},
{
"properties": {
"heading": 1
},
"parent": {
"id": 7618
},
"children": [
{
"parent": {
"id": 7632
},
"children": [],
"id": 7640,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 3,
"uuid": "682cfd1c-1d41-45de-a18c-9a0785e43dce",
"content": "",
"page": {
"id": 7605
},
"left": {
"id": 7632
},
"format": "markdown"
}
],
"id": 7632,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 2,
"uuid": "682cfd1c-841c-4696-8bb6-8f95470c7c9a",
"content": "# Tópicos",
"page": {
"id": 7605
},
"propertiesOrder": [],
"left": {
"id": 7627
},
"format": "markdown"
},
{
"properties": {
"heading": 1
},
"parent": {
"id": 7618
},
"children": [
{
"parent": {
"id": 7635
},
"children": [],
"id": 7615,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 3,
"uuid": "682cfd1c-6bbf-433d-aa99-154187f06356",
"content": "",
"page": {
"id": 7605
},
"left": {
"id": 7635
},
"format": "markdown"
}
],
"id": 7635,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 2,
"uuid": "682cfd1c-bbcd-4fd9-8dda-d7ff5b1f72e8",
"content": "# Anotações",
"page": {
"id": 7605
},
"propertiesOrder": [],
"left": {
"id": 7632
},
"format": "markdown"
},
{
"properties": {
"heading": 1
},
"parent": {
"id": 7618
},
"children": [
{
"parent": {
"id": 7614
},
"children": [],
"id": 7619,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 3,
"uuid": "682cfd1c-482b-43e5-a0b5-5409207cd69a",
"content": "",
"page": {
"id": 7605
},
"left": {
"id": 7614
},
"format": "markdown"
}
],
"id": 7614,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 2,
"uuid": "682cfd1c-b4e4-42ec-a18c-a66f6742a8ee",
"content": "# Referências Bibliográficas",
"page": {
"id": 7605
},
"propertiesOrder": [],
"left": {
"id": 7635
},
"format": "markdown"
},
{
"properties": {
"heading": 1
},
"parent": {
"id": 7618
},
"children": [
{
"parent": {
"id": 7616
},
"children": [],
"id": 7625,
"pathRefs": [
{
"id": 7
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 3,
"uuid": "682cfd1c-d358-4f88-86e5-86259d4e04fd",
"content": "DONE Fazer a avaliação da aula [[IoT I]]",
"marker": "DONE",
"page": {
"id": 7605
},
"left": {
"id": 7616
},
"format": "markdown",
"refs": [
{
"id": 7
},
{
"id": 7605
}
]
}
],
"id": 7616,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 2,
"uuid": "682cfd1c-c72d-4c48-b884-28c85f41858f",
"content": "# Avaliação",
"page": {
"id": 7605
},
"propertiesOrder": [],
"left": {
"id": 7614
},
"format": "markdown"
},
{
"properties": {
"heading": 1
},
"parent": {
"id": 7618
},
"children": [
{
"parent": {
"id": 7621
},
"children": [
{
"parent": {
"id": 7628
},
"children": [],
"id": 7611,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 4,
"uuid": "682cfd1c-14f6-4765-97d9-749251cbf228",
"content": "Resposta Correta: LGPD",
"page": {
"id": 7605
},
"left": {
"id": 7628
},
"format": "markdown"
}
],
"id": 7628,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 3,
"uuid": "682cfd1c-d650-4cb6-ba11-c2e00ee6df80",
"content": "Qual norma é citada para garantir conformidade com privacidade de dados em IoT no Brasil? #card\n + [ ] NIST 800-53\n + [ ] GDPR\n + [ ] ISO 9001\n + [ ] LGPD",
"page": {
"id": 7605
},
"left": {
"id": 7621
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"parent": {
"id": 7621
},
"children": [
{
"parent": {
"id": 7608
},
"children": [],
"id": 7609,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 4,
"uuid": "682cfd1c-6d5b-4ce6-a02b-5bcde1935334",
"content": "Resposta Correta: Processamento local, próximo à origem dos dados.",
"page": {
"id": 7605
},
"left": {
"id": 7608
},
"format": "markdown"
}
],
"id": 7608,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 3,
"uuid": "682cfd1c-8bb5-4a82-8700-0cb109e1591b",
"content": "Edge Computing é caracterizado por: #card\n + [ ] Processamento local, próximo à origem dos dados.\n + [ ] Processamento remoto em data centers.\n + [ ] Processamento distribuído entre diversos servidores globais.\n + [ ] Dependência total da nuvem para operação.",
"page": {
"id": 7605
},
"left": {
"id": 7628
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"parent": {
"id": 7621
},
"children": [
{
"parent": {
"id": 7629
},
"children": [],
"id": 7624,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 4,
"uuid": "682cfd1c-0413-4f6e-8031-9fcc66fc8728",
"content": "Resposta Correta: Combinação de nuvem pública e privada.",
"page": {
"id": 7605
},
"left": {
"id": 7629
},
"format": "markdown"
}
],
"id": 7629,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 3,
"uuid": "682cfd1c-1061-48d0-9f49-f3737e10d0ee",
"content": "O que caracteriza a computação em nuvem híbrida? #card\n + [ ] Combinação de nuvem pública e privada.\n + [ ] Uso exclusivo de servidores locais.\n + [ ] Exclusividade para empresas privadas.\n + [ ] Uso apenas de infraestrutura pública.",
"page": {
"id": 7605
},
"left": {
"id": 7608
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"parent": {
"id": 7621
},
"children": [
{
"parent": {
"id": 7641
},
"children": [],
"id": 7639,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 4,
"uuid": "682cfd1c-48e8-49f6-ad2e-ff4f8ec7780d",
"content": "Resposta Correta: TPM (Trusted Platform Module)",
"page": {
"id": 7605
},
"left": {
"id": 7641
},
"format": "markdown"
}
],
"id": 7641,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 3,
"uuid": "682cfd1c-f3fa-41fd-90a3-f6ed532b31b4",
"content": "Qual componente de hardware é essencial para armazenar chaves criptográficas com segurança em IoT? #card\n + [ ] Sensor DHT11\n + [ ] Microcontrolador ESP32\n + [ ] TPM (Trusted Platform Module)\n + [ ] Gateway LoRa",
"page": {
"id": 7605
},
"left": {
"id": 7629
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"parent": {
"id": 7621
},
"children": [
{
"parent": {
"id": 7636
},
"children": [],
"id": 7626,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 4,
"uuid": "682cfd1c-6b83-4efe-b188-d9e2e218cbde",
"content": "Resposta Correta: Validação",
"page": {
"id": 7605
},
"left": {
"id": 7636
},
"format": "markdown"
}
],
"id": 7636,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 3,
"uuid": "682cfd1c-3bf3-45e6-8949-1c7d4ac1a4f6",
"content": "Qual das opções abaixo NÃO é um dos 5 Vs do Big Data? #card\n + [ ] Valor\n + [ ] Variedade\n + [ ] Validação\n + [ ] Velocidade",
"page": {
"id": 7605
},
"left": {
"id": 7641
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"parent": {
"id": 7621
},
"children": [
{
"parent": {
"id": 7638
},
"children": [],
"id": 7620,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 4,
"uuid": "682cfd1c-f173-42d7-97f6-1e27859905d0",
"content": "Resposta Correta: Como camada intermediária entre Cloud e dispositivos locais.",
"page": {
"id": 7605
},
"left": {
"id": 7638
},
"format": "markdown"
}
],
"id": 7638,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 3,
"uuid": "682cfd1c-4599-42b8-a49a-86012d118559",
"content": "Fog Computing se posiciona: #card\n + [ ] No nível do usuário final exclusivamente.\n + [ ] Como camada intermediária entre Cloud e dispositivos locais.\n + [ ] Dentro da nuvem apenas.\n + [ ] Apenas em data centers distantes.",
"page": {
"id": 7605
},
"left": {
"id": 7636
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"parent": {
"id": 7621
},
"children": [
{
"parent": {
"id": 7634
},
"children": [],
"id": 7613,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 4,
"uuid": "682cfd1c-f254-4526-be3a-8528bb3416cf",
"content": "Resposta Correta: Está mais próxima da fonte dos dados, reduzindo latência.",
"page": {
"id": 7605
},
"left": {
"id": 7634
},
"format": "markdown"
}
],
"id": 7634,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 3,
"uuid": "682cfd1c-b6dc-4de6-8d92-cb5a136f9810",
"content": "A Fog Computing se diferencia da Cloud Computing porque: #card\n + [ ] Está localizada no mesmo local da cloud.\n + [ ] Processa dados diretamente no dispositivo final.\n + [ ] É mais cara e menos eficiente.\n + [ ] Está mais próxima da fonte dos dados, reduzindo latência.",
"page": {
"id": 7605
},
"left": {
"id": 7638
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"parent": {
"id": 7621
},
"children": [
{
"parent": {
"id": 7637
},
"children": [],
"id": 7617,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 4,
"uuid": "682cfd1c-390f-48d6-b4ec-42bb5d70cabe",
"content": "Resposta Correta: Integração homem-máquina com foco em personalização.",
"page": {
"id": 7605
},
"left": {
"id": 7637
},
"format": "markdown"
}
],
"id": 7637,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 3,
"uuid": "682cfd1c-5fbd-4d63-95c6-cc703c6cf9bb",
"content": "Qual é uma característica central da Indústria 5.0? #card\n + [ ] Uso de máquinas a vapor.\n + [ ] Integração homem-máquina com foco em personalização.\n + [ ] Linhas de montagem em larga escala.\n + [ ] Automação de processos industriais.",
"page": {
"id": 7605
},
"left": {
"id": 7634
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"parent": {
"id": 7621
},
"children": [
{
"parent": {
"id": 7630
},
"children": [],
"id": 7631,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 4,
"uuid": "682cfd1c-f010-4727-b8e7-a191515b5117",
"content": "Resposta Correta: Diversidade de protocolos e ausência de padrões universais.",
"page": {
"id": 7605
},
"left": {
"id": 7630
},
"format": "markdown"
}
],
"id": 7630,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 3,
"uuid": "682cfd1c-bb9f-4877-9e2b-2c728f382deb",
"content": "O que dificulta a interoperabilidade em sistemas IoT? #card\n + [ ] Diversidade de protocolos e ausência de padrões universais.\n + [ ] Falta de energia nos sensores.\n + [ ] Limitações de hardware nos gateways.\n + [ ] Falta de conectividade com redes móveis.",
"page": {
"id": 7605
},
"left": {
"id": 7637
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"parent": {
"id": 7621
},
"children": [
{
"parent": {
"id": 7610
},
"children": [],
"id": 7612,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 4,
"uuid": "682cfd1c-8280-438a-9c73-b1be83321988",
"content": "Resposta Correta: Automação com controle por computador.",
"page": {
"id": 7605
},
"left": {
"id": 7610
},
"format": "markdown"
}
],
"id": 7610,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 3,
"uuid": "682cfd1c-a3e6-4a3a-af04-0c81e02cc320",
"content": "A Indústria 3.0 é marcada por qual característica principal? #card\n + [ ] Eletricidade como força motriz.\n + [ ] Integração entre humanos e máquinas.\n + [ ] Automação com controle por computador.\n + [ ] Impressão 3D em massa.",
"page": {
"id": 7605
},
"left": {
"id": 7630
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
}
],
"id": 7621,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"level": 2,
"uuid": "682cfd1c-fc4b-4243-a826-e326791e5c38",
"content": "# Flashcards",
"page": {
"id": 7605
},
"propertiesOrder": [],
"left": {
"id": 7616
},
"format": "markdown"
}
],
"invalidProperties": [],
"id": 7618,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"propertiesTextValues": {
"relacionado": "",
"curso": "[[MBA Engenharia de Software]]",
"tags": "",
"tecnologias": "",
"tipo": "#aula",
"professor": "[[Fernando Henrique Vieira Trindade]]",
"livros": "",
"ordem": "",
"data": "[[Apr 24th, 2025]]",
"materia": "[[IoT I]]"
},
"level": 1,
"uuid": "682cfd1c-3c9a-40cb-b79f-da14dc37fcec",
"content": "tipo:: #aula\ncurso:: [[MBA Engenharia de Software]] \nmateria:: [[IoT I]]\ndata:: [[Apr 24th, 2025]] \nordem:: \nprofessor:: [[Fernando Henrique Vieira Trindade]]\ntecnologias::\nlivros::\ntags:: \nrelacionado::\n\n",
"page": {
"id": 7605
},
"preBlock?": true,
"propertiesOrder": [
"tipo",
"curso",
"materia",
"data",
"ordem",
"professor",
"tecnologias",
"livros",
"tags",
"relacionado"
],
"left": {
"id": 7605
},
"format": "markdown",
"refs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
]
}
]

Requests Example of Page Links:

Method: POST
Endpoint: http://127.0.0.1:12315/api
Headers: Authorization - Bearer auth254
Body:
{
"method": "logseq.Editor.getPageLinkedReferences",
"args": [
"IoT I"
]
}

Response:
[
[
{
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
[
{
"properties": {
"heading": 1
},
"parent": {
"id": 7651
},
"id": 7655,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-55a9-42d5-b865-12e3ee3ee7d6",
"content": "# Referências Bibliográficas",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"propertiesOrder": [],
"left": {
"id": 7678
},
"format": "markdown"
},
{
"properties": {
"relacionado": [
"IoT I"
],
"curso": [
"MBA Engenharia de Software"
],
"tags": "",
"tecnologias": "",
"tipo": [
"aula"
],
"professor": [
"Fernando Henrique Vieira Trindade"
],
"livros": "",
"ordem": "",
"data": [
"May 8th, 2025"
],
"materia": [
"IoT II"
]
},
"parent": {
"id": 7643
},
"id": 7651,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"propertiesTextValues": {
"relacionado": "[[IoT I]]",
"curso": "[[MBA Engenharia de Software]]",
"tags": "",
"tecnologias": "",
"tipo": "#aula",
"professor": "[[Fernando Henrique Vieira Trindade]]",
"livros": "",
"ordem": "",
"data": "[[May 8th, 2025]]",
"materia": "[[IoT II]]"
},
"uuid": "682cfd1c-c956-4797-906d-0e711cd6726b",
"content": "tipo:: #aula\ncurso:: [[MBA Engenharia de Software]] \nmateria:: [[IoT II]]\ndata:: [[May 8th, 2025]] \nordem:: \nprofessor:: [[Fernando Henrique Vieira Trindade]] \ntecnologias::\nlivros::\ntags:: \nrelacionado:: [[IoT I]]\n\n",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"preBlock?": true,
"propertiesOrder": [
"tipo",
"curso",
"materia",
"data",
"ordem",
"professor",
"tecnologias",
"livros",
"tags",
"relacionado"
],
"left": {
"id": 7643
},
"format": "markdown",
"refs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
]
},
{
"parent": {
"id": 7665
},
"id": 7674,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-7334-4eb6-bb75-e9fd530aa59b",
"content": "O protocolo CoAP é ideal para: #card\n + [ ] Transmissão de vídeos.\n + [ ] Dispositivos com alta largura de banda.\n + [ ] Conexões HTTP em servidores corporativos.\n + [ ] Dispositivos com restrição energética.",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"left": {
"id": 7665
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"parent": {
"id": 7665
},
"id": 7664,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-aeb7-4ee6-a11d-c8cfdc7c70b3",
"content": "No ciclo CRISP-DM, a fase final é: #card\n + [ ] Implementação\n + [ ] Avaliação\n + [ ] Coleta de dados\n + [ ] Modelagem",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"left": {
"id": 7671
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"parent": {
"id": 7646
},
"id": 7669,
"pathRefs": [
{
"id": 7
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-0229-47b7-9a7b-c7463707ecb5",
"content": "DONE Fazer a avaliação da aula [[IoT II]]",
"marker": "DONE",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"left": {
"id": 7646
},
"format": "markdown",
"refs": [
{
"id": 7
},
{
"id": 7643
}
]
},
{
"content": "Resposta Correta: O nível de garantia na entrega da mensagem.",
"format": "markdown",
"left": {
"id": 7671
},
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"parent": {
"id": 7671
},
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-accd-45d0-91f0-cd952b2d7cb3",
"id": 7649
},
{
"content": "Resposta Correta: Dispositivos com restrição energética.",
"format": "markdown",
"left": {
"id": 7674
},
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"parent": {
"id": 7674
},
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-d7a4-43b0-976f-482bce09fb2c",
"id": 7654
},
{
"parent": {
"id": 7665
},
"id": 7650,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-5d3f-4b21-a82b-4f8db12b722e",
"content": "O modelo de 5 camadas em IoT adiciona qual camada à tradicional de 3 camadas? #card\n + [ ] Camada de Monitoramento\n + [ ] Camada de Negócio\n + [ ] Camada de Visualização\n + [ ] Camada de Transporte",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"left": {
"id": 7660
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"content": "Resposta Correta: Camada de Negócio",
"format": "markdown",
"left": {
"id": 7650
},
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"parent": {
"id": 7650
},
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-f1a9-4257-88bc-50fc0953fcdb",
"id": 7656
},
{
"content": "Resposta Correta: Execução assíncrona baseada em eventos.",
"format": "markdown",
"left": {
"id": 7647
},
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"parent": {
"id": 7647
},
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-fbc8-4f23-8bdc-bca00813a904",
"id": 7668
},
{
"parent": {
"id": 7665
},
"id": 7658,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-b169-40f3-9bf2-d92b330d3b0b",
"content": "Analytics Preditivo responde à pergunta: #card\n + [ ] O que aconteceu?\n + [ ] O que devo fazer?\n + [ ] Por que aconteceu?\n + [ ] O que pode acontecer?",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"left": {
"id": 7661
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"content": "Resposta Correta: Executar tarefas específicas.",
"format": "markdown",
"left": {
"id": 7660
},
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"parent": {
"id": 7660
},
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-5f51-4af5-9361-6b02bd1e28f1",
"id": 7667
},
{
"parent": {
"id": 7665
},
"id": 7661,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-b58f-4452-8140-23a7c524b1c6",
"content": "Qual das tecnologias abaixo é usada na faixa ISM e permite comunicação de baixa potência em até 15 km? #card\n + [ ] Wi-Fi\n + [ ] Bluetooth\n + [ ] ZigBee\n + [ ] LoRa",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"left": {
"id": 7675
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"parent": {
"id": 7665
},
"id": 7675,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-e92a-463c-adb8-42ba3d63e17d",
"content": "O protocolo que permite sensores comunicarem sem bateria, refletindo sinais, é conhecido como: #card\n + [ ] BLE\n + [ ] Backscatter\n + [ ] NFC\n + [ ] UWB",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"left": {
"id": 7664
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"parent": {
"id": 7665
},
"id": 7671,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-0e23-4177-b805-b4b804fbb64e",
"content": "O QoS no protocolo MQTT define: #card\n + [ ] A segurança do dispositivo.\n + [ ] O número máximo de assinantes.\n + [ ] O tamanho máximo da mensagem.\n + [ ] O nível de garantia na entrega da mensagem.",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"left": {
"id": 7650
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"properties": {
"heading": 1
},
"parent": {
"id": 7651
},
"id": 7659,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-0a42-4818-897d-96c8e47627e4",
"content": "# Resumo",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"propertiesOrder": [],
"left": {
"id": 7651
},
"format": "markdown"
},
{
"content": "",
"format": "markdown",
"left": {
"id": 7678
},
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"parent": {
"id": 7678
},
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-a5cb-4e54-b0f6-a0d6741b5e93",
"id": 7673
},
{
"content": "Resposta Correta: Backscatter",
"format": "markdown",
"left": {
"id": 7675
},
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"parent": {
"id": 7675
},
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-7cc2-493e-b675-c06c87208d4f",
"id": 7677
},
{
"properties": {
"heading": 1
},
"parent": {
"id": 7651
},
"id": 7646,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-e676-487e-91a9-92e1522a6f61",
"content": "# Avaliação",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"propertiesOrder": [],
"left": {
"id": 7655
},
"format": "markdown"
},
{
"content": "",
"format": "markdown",
"left": {
"id": 7655
},
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"parent": {
"id": 7655
},
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-9f49-4e01-ba54-83053fd764bd",
"id": 7670
},
{
"content": "Resposta Correta: O que pode acontecer?",
"format": "markdown",
"left": {
"id": 7658
},
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"parent": {
"id": 7658
},
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-9b25-4ff3-91ea-0fe7f17d56f3",
"id": 7653
},
{
"content": "Resposta Correta: Implementação",
"format": "markdown",
"left": {
"id": 7664
},
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"parent": {
"id": 7664
},
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-ccc3-4f64-97bf-279c8cbe9fcd",
"id": 7657
},
{
"content": "",
"format": "markdown",
"left": {
"id": 7662
},
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"parent": {
"id": 7662
},
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-c5ac-4297-ab17-74ffb225fb0b",
"id": 7645
},
{
"parent": {
"id": 7665
},
"id": 7663,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-93a4-43ed-9a4b-77d2398e0e04",
"content": "Um middleware pode realizar todas as funções abaixo, EXCETO: #card\n + [ ] Decisão autônoma de negócios.\n + [ ] Agregação de dados.\n + [ ] Tradução de protocolos.\n + [ ] Gerenciamento de segurança.",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"left": {
"id": 7647
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"properties": {
"heading": 1
},
"parent": {
"id": 7651
},
"id": 7648,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-1ede-4828-b8ac-76b72bd537ff",
"content": "# Material Complementar",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"propertiesOrder": [],
"left": {
"id": 7659
},
"format": "markdown"
},
{
"content": "Resposta Correta: Decisão autônoma de negócios.",
"format": "markdown",
"left": {
"id": 7663
},
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"parent": {
"id": 7663
},
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-1387-4fe3-9d54-5d81777295e3",
"id": 7676
},
{
"content": "",
"format": "markdown",
"left": {
"id": 7659
},
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"parent": {
"id": 7659
},
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-1686-46e0-94e2-766b9e30cb2c",
"id": 7652
},
{
"content": "Resposta Correta: LoRa",
"format": "markdown",
"left": {
"id": 7661
},
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"parent": {
"id": 7661
},
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-b2a5-4911-8282-9725674d1cd6",
"id": 7666
},
{
"parent": {
"id": 7665
},
"id": 7647,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-5c7d-4630-b3d5-73ff0e60411f",
"content": "Uma característica dos SOEs (Sistemas Orientados a Eventos) é: #card\n + [ ] Processamento em lotes.\n + [ ] Baixa escalabilidade.\n + [ ] Execução assíncrona baseada em eventos.\n + [ ] Acoplamento rígido entre módulos.",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"left": {
"id": 7674
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
},
{
"properties": {
"heading": 1
},
"parent": {
"id": 7651
},
"id": 7662,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-cea3-49c0-8556-7b00603beddc",
"content": "# Tópicos",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"propertiesOrder": [],
"left": {
"id": 7648
},
"format": "markdown"
},
{
"properties": {
"heading": 1
},
"parent": {
"id": 7651
},
"id": 7678,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-fc0e-440d-82a2-e42da1fe3322",
"content": "# Anotações",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"propertiesOrder": [],
"left": {
"id": 7662
},
"format": "markdown"
},
{
"content": "",
"format": "markdown",
"left": {
"id": 7648
},
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"parent": {
"id": 7648
},
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-a25f-495e-9d1b-34e66ac288c6",
"id": 7672
},
{
"properties": {
"heading": 1
},
"parent": {
"id": 7651
},
"id": 7665,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-8637-4a15-bcf2-f58cbff76073",
"content": "# Flashcards",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"propertiesOrder": [],
"left": {
"id": 7646
},
"format": "markdown"
},
{
"parent": {
"id": 7665
},
"id": 7660,
"pathRefs": [
{
"id": 2
},
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7643
},
{
"id": 7644
}
],
"uuid": "682cfd1c-5253-4b7d-9430-095c255e4726",
"content": "IA fraca é caracterizada por: #card\n + [ ] Executar tarefas específicas.\n + [ ] Ser uma simulação de redes peer-to-peer.\n + [ ] Ter consciência e emoções.\n + [ ] Aprender sozinha sem dados.",
"page": {
"name": "iot ii",
"originalName": "IoT II",
"id": 7643
},
"left": {
"id": 7663
},
"format": "markdown",
"refs": [
{
"id": 2
}
]
}
]
]
]

Requests Example of Get Block:

Method: POST
Endpoint: http://127.0.0.1:12315/api
Headers: Authorization - Bearer auth254
Body:
{
"method": "logseq.Editor.getBlock",
"args": [
"682cfd1c-7874-40e8-8f43-a4f7b0841754"
]
}
Response:
{
"properties": {
"heading": 1
},
"parent": {
"id": 7618
},
"children": [
[
"uuid",
"682cfd1c-a83b-4992-af8c-bb0be6136307"
]
],
"id": 7627,
"pathRefs": [
{
"id": 170
},
{
"id": 287
},
{
"id": 7605
},
{
"id": 7606
},
{
"id": 7607
}
],
"uuid": "682cfd1c-7874-40e8-8f43-a4f7b0841754",
"content": "# Material Complementar",
"page": {
"id": 7605
},
"propertiesOrder": [],
"left": {
"id": 7633
},
"format": "markdown"
}

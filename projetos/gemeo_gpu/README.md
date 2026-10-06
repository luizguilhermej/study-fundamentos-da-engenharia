# Gêmeo Digital Térmico de Hardware Computacional

## Placa GPU de Inferência de IA em Operação Contínua

Projeto acadêmico de Sistematização desenvolvido para a disciplina de **Fundamentos de Engenharia — CEUB**, com o objetivo de desenvolver um **gêmeo digital térmico** para uma GPU destinada à inferência de Inteligência Artificial em operação contínua.

O projeto integra **CAD, transferência de calor, ciência dos materiais, mecânica dos sólidos, química, sustentabilidade e simulação computacional**.

---

## 🎯 Objetivo

Avaliar uma solução de dissipação térmica capaz de manter a GPU abaixo de um **limite de projeto de 80 °C**, considerando desempenho térmico, massa, fabricação, custo, confiabilidade e sustentabilidade.

A **NVIDIA L4** foi utilizada como referência, com potência térmica de **72 W** e temperatura ambiente nominal de **25 °C**.

> O limite de 80 °C é um critério interno e conservador definido para este projeto, não o limite oficial de operação da NVIDIA L4.

---

## 🧱 Solução proposta

Foi desenvolvido um dissipador de **Alumínio 6061** com:

* Base: **170 × 70 × 5 mm**
* **12 aletas**
* Altura das aletas: **25 mm**
* Espessura das aletas: **2 mm**
* Altura total: **30 mm**
* Ventilação forçada

### Por que Alumínio 6061?

O cobre possui maior condutividade térmica (≈388 W/m·K), mas também possui maior densidade e custo.

O Alumínio 6061 (≈160 W/m·K) oferece melhor equilíbrio entre:

**massa + custo + fabricação + desempenho térmico + reciclabilidade.**

---

## 🌡️ Simulação térmica

O modelo considera:

* condução no dissipador;
* convecção para o ar;
* regime permanente;
* potência de 72 W;
* ambiente a 25 °C;
* diferentes coeficientes de convecção;
* limite de projeto de 80 °C.

### Resultados

| h (W/m²·K) |        Tmax | Resultado |
| ---------: | ----------: | :-------: |
|          5 |    140,7 °C |     ❌     |
|         10 |     84,2 °C |     ❌     |
|         15 |     65,3 °C |     ✅     |
|         20 |     55,9 °C |     ✅     |
|         30 |     46,5 °C |     ✅     |
|         40 | **41,7 °C** |     ✅     |

Na condição de ventilação forçada adotada (**h = 40 W/m²·K**), a temperatura máxima foi de aproximadamente **41,7 °C**, proporcionando uma margem de **38,3 °C** até o limite de projeto.

O estudo também demonstrou que o **fluxo de ar é um dos parâmetros mais críticos do sistema**: com h = 10 W/m²·K, a temperatura ultrapassa o limite de 80 °C.

---

## ⚙️ Outras análises

O projeto também aborda:

### Mecânica

Avaliação da dilatação térmica do dissipador e dos efeitos dos ciclos de temperatura.

### Química

Análise da interface térmica, pasta térmica, oxidação e corrosão do alumínio.

### Sustentabilidade

Estimativa de consumo energético e emissões, além de propostas como:

* controle PWM dos ventiladores;
* power capping;
* uso de alumínio reciclado;
* projeto para desmontagem;
* reutilização da GPU;
* reciclagem adequada.

---

## 📐 Estrutura do projeto

```text
gemeo-digital-gpu/
│
├── README.md
├── relatorio/
│   └── relatorio_final.pdf
│
├── cad/
│   ├── dissipador_gpu.step
│   ├── dissipador_gpu.stl
│   └── gerar_dissipador_freecad.py
│
├── simulacao/
│   ├── simulacao_termica_gpu.ipynb
│
└── figuras/
    └── *.png
```

---

## 💻 Reprodutibilidade

A simulação está disponível em **Jupyter Notebook/Google Colab**, permitindo alterar parâmetros como:

* potência da GPU;
* material;
* geometria;
* coeficiente de convecção;
* temperatura ambiente.

Os modelos CAD são disponibilizados em **STEP/STL**, permitindo visualização e edição em softwares compatíveis, como o FreeCAD.

---

## ⚠️ Limitações

O modelo possui caráter acadêmico e simplificado. Não são representados em detalhe:

* turbulência tridimensional;
* recirculação real do ar;
* radiação;
* encapsulamento completo da GPU;
* memória e VRMs;
* anisotropia da PCB.

Como evolução, podem ser utilizados **CFD, FEA 3D e validação experimental**.

---

## 🏁 Conclusão

O projeto demonstrou que um dissipador de **Alumínio 6061 com 12 aletas e ventilação forçada** pode atender ao critério térmico definido para a condição analisada.

Mais importante, o estudo demonstra que o desempenho de uma solução térmica depende da integração entre:

**Material + Geometria + Transferência de Calor + Ventilação + Mecânica + Sustentabilidade.**

---

## 👥 Autores

**Breno Lopes Souza**
**Luiz Guilherme Oliveira Jardim**

**Engenharia de Software — 1º Semestre - CEUB**
**Fundamentos de Engenharia — 2026.2**

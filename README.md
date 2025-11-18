# 🎬 CineManager - Sistema de Gerenciamento de Filmes

Este projeto é um sistema completo de gerenciamento de filmes (CRUD) desenvolvido em **Python**. Ele integra uma interface gráfica moderna (Desktop) com uma API Local, compartilhando o mesmo banco de dados SQLite.

O projeto foi desenvolvido para atender aos requisitos do **Trabalho Final de LTP2**, demonstrando conceitos de Programação Orientada a Objetos, Banco de Dados Relacional e integração de sistemas.

---

## 👥 Integrantes do Grupo

* **Alysson Kennedy De Oliveira Carvalho**
* **Matheus Costas Pessanha**

---

## 🚀 Funcionalidades

* **Interface Gráfica (GUI):** Visual moderno e intuitivo (tema *Cerculean*) para gerenciar o catálogo.
* **Banco de Dados Relacional:** Uso de SQLite com duas tabelas (`filmes` e `categorias`) ligadas por Chave Estrangeira (Foreign Key).
* **API RESTful:** API local rodando em paralelo (Flask) que permite consultar e manipular os dados via requisições HTTP.
* **CRUD Completo:** Criar, Ler, Atualizar e Deletar filmes tanto pela interface quanto pela API.
* **Multithreading:** A interface e a API rodam simultaneamente sem travamentos.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Interface:** Tkinter + `ttkbootstrap` (para estilização moderna)
* **API:** Flask
* **Banco de Dados:** SQLite3 (Nativo do Python)

---

## 📂 Estrutura do Projeto

| Arquivo | Descrição |
| :--- | :--- |
| `main.py` | Ponto de entrada. Inicia a API em uma thread separada e lança a Interface Gráfica. |
| `db.py` | Camada de persistência. Gerencia a conexão SQLite, criação de tabelas e queries SQL. |
| `gui.py` | Camada de visualização. Contém a classe da interface gráfica e lógica dos botões. |
| `api.py` | Camada de serviço. Contém as rotas da API Flask (Endpoints). |

---
## 📦 Como Executar

### 1. Pré-requisitos
Instale as dependências necessárias:

```bash
pip install flask ttkbootstrap

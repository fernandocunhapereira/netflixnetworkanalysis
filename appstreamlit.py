# -*- coding: utf-8 -*-
"""AppStreamlit.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BZz051R4kWsiS36tONU4sDcF6FrvQa4Q
"""

"""!pip install networkx pyvis nxviz streamlit -U --quiet"""

from pyvis.network import Network
from IPython.core.display import display, HTML
import pandas as pd
import csv
import numpy as np
# import matplotlib.pyplot as plt
import nxviz as nv
import networkx as nx
import streamlit as st
import streamlit.components.v1 as components

# Set header title
st.title('Atores que contracenaram entre si nos filmes da Netflix lançados em 2020')

netflixDataFrame = pd.read_csv("https://github.com/fernandocunhapereira/netflixnetworkanalysis/raw/master/netflix_titles.csv")
netflixDataFrame.head()
netflixDataList = netflixDataFrame.values.tolist()

atores = set()

for row in netflixDataList:
    if row[7] == 2020 and row[1] == 'Movie' and row[5] == 'United States':  # Filmes lançados em 2020 produzidos no EUA
      if pd.isna(row[4]) != True: # Checar se o campo de atores não é nulo
        atoresDoFilme = row[4].split(', ') # Atores que participaram do filme
        for ator in atoresDoFilme:
          if ator not in atores:
            atores.add(ator)

listaAtores = list(atores)

grafo = nx.Graph()

for ator in listaAtores:
  for row in netflixDataList: # Verificar quais filmes o ator participou conforme o criterio da busca e com quem contracenou
    if pd.isna(row[4]) != True and row[7] == 2020 and row[1] == 'Movie' and row[5] == 'United States':
      atoresDoFilme = row[4].split(', ')
      if ator in atoresDoFilme:
        if ator not in grafo:
          grafo.add_node(ator)
        for elemento in atoresDoFilme:
          if elemento not in grafo:
            grafo.add_node(elemento)
          if ator!= elemento:
            grafo.add_edge(ator, elemento)

nodesSozinhos = []

for node in grafo:
  if len(list(grafo.neighbors(node))) == 0: # Selecionar os nós que estão sozinhos
    nodesSozinhos.append(node)
for node in nodesSozinhos: # Excluir nós sozinhos
  grafo.remove_node(node)

def networkx_para_pyvis(G):
  grafo_gerado=Network(height='400px', width='',heading='', notebook=True, cdn_resources='in_line')

  for node in G:
    grafo_gerado.add_node(node)

  eoi = [(u, v) for u, v in G.edges()]
  for u, v in eoi:
    grafo_gerado.add_edge(u, v)

  return grafo_gerado

gNetflix = networkx_para_pyvis(grafo)

def gerar_subgrafo(node1, G):
  grafo_gerado = nx.Graph()
  visited_nodes = set()
  queue = [node1]

  while len(queue) > 0:
    node = queue.pop()
    neighbors = list(G.neighbors(node))

    if node not in grafo_gerado or visited_nodes:
      grafo_gerado.add_node(node)
      visited_nodes.add(node)
      for vizinho in neighbors:
        grafo_gerado.add_edge(node, vizinho)
      nbrs = [n for n in neighbors if n not in visited_nodes]
      queue = nbrs + queue

  return grafo_gerado

sub_grafo_netflix = gerar_subgrafo('Anna Camp', grafo) # usando Anna Camp gera o maior subgrafo a partir do grafo original

netflix_subnetwork = networkx_para_pyvis(sub_grafo_netflix)

netflix_subnetwork.show('netflix_subnetwork.html')
display(HTML('netflix_subnetwork.html'))

#Save and read graph as HTML file (on Streamlit Sharing)
try:
  path = '/tmp'
  netflix_subnetwork.save_graph(f'{path}/pyvis_graph.html')
  HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

# Save and read graph as HTML file (locally)
except:
  path = '/html_files'
  netflix_subnetwork.save_graph(f'{path}/pyvis_graph.html')
  HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
components.html(HtmlFile.read(), height=435)
from this import d
import numpy as np
import pandas as pd
import streamlit as st 
import pandas as pd
import numpy as np
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

df = pd.read_csv('pdssimilar (2).csv')

G = nx.read_gpickle("G.gpickle")

n = list(G.nodes) 
n =  np.array(n)
n = np.unique(n)


def getsimilar(arr):
    indarr = []
    counter = 0
    st.write("  ")
    st.write("Similar Products are:")
    for i in arr:
        indx = df.index[df['ASIN'] == i][0]
        if(indx in n):
            st.text(G.nodes[indx]['Title'])
            indarr.append(indx)
        else:
            counter = counter+1
    st.write("   ")
    st.write("   ")
    return counter, indarr

def getclean(pro_id):    
    l = str(list(G.edges(pro_id)))
    l = l.replace('[','')
    l = l.replace(']','')
    l = l.replace(',','')
    l = l.replace('(','')
    l = l.replace(')','')
    l = l.replace(str(pro_id), '')
    b = l.split()
    b = np.array(b)
    b = b.astype(int)
    return b

def search(s):
  s = s.lower()
  indx = df.index[(df['Title'].str.contains(s, case = False))==True]   
  indx = np.array(indx)
  indx = indx.astype(int)
  return indx


def check(val):
    temp = int(val)
    if(temp in n):
        pro_id = temp
        # st.write("Selected product is", pro_id)
        pro_dict = G.nodes[pro_id]
        # st.write(pro_dict)
        arr = pro_dict['Copurchased']
        arr = arr.split(' ')
        arr = np.array(arr)
        counter, indarr = getsimilar(arr)
        print(counter,"nodes have been removed from the graph")
        print(pro_dict)
    else:
        st.write("Empty node has been removed from the graph!")



def main():
    st.title("Product Recommendation")
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Recommender System</h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    val = st.text_input("Enter a Product ID")
    iarray = search(val)
    iarray_names = []
    if len(iarray) == 0:
        st.write("Product Does Not Exist")
    else:
        for i in range(0, len(iarray)):
            if(iarray[i] in n):
                pro_id = int(iarray[i])
                iarray_names.append(G.nodes[iarray[i]]['Title'])
        name = st.selectbox("Select", iarray_names)

        prod_id = search(name)
        st.write(pro_id)
        check(prod_id)
        #         check(pro_id)
    
    # st.write(indarr)
        
    # st.write(result)
    # if st.button("About"):
    #     st.text("Recommendations generated using Item-based collaborative filtering")

if __name__=='__main__':
    main()
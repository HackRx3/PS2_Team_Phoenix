from asyncio.windows_events import NULL
import numpy as np
import pandas as pd
import streamlit as st 
import pandas as pd
import numpy as np
import networkx as nx

# Datasets of Similarities and Recommendations
df = pd.read_csv('pdssimilar (2).csv')
df_rec = pd.read_csv('finalpreprocesseddata.csv')

# Graphs of Similarities and Recommendations based on Above Datasets
G_Sim = nx.read_gpickle("G.gpickle")
G_Rec = nx.read_gpickle("G_Rec.gpickle")

# Unique Nodes of Similarity Graph
n_sim = list(G_Sim.nodes) 
n_sim =  np.array(n_sim)
n_sim = np.unique(n_sim)

# Unique Nodes of Recommendation Graph
n_rec = list(G_Rec.nodes)
n_rec = np.array(n_rec)
n_rec = np.unique(n_rec)

# Function to Get Similar Nodes
def getsimilar(arr):
    indarr = []
    counter = 0
    st.write("  ")
    # st.markdown("**Similar Products are:**")
    for i in arr:
        indx = df.index[df['ASIN'] == i][0]
        if(indx in n_sim):
            st.text(G_Sim.nodes[indx]['Title'])
            indarr.append(indx)
        else:
            counter = counter+1
    st.write("   ")
    st.write("   ")
    return counter, indarr

# Cleaning the Product ID Output
def getclean(pro_id):    
    l = str(list(G_Sim.edges(pro_id)))
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

# Searching for Index With Respect to Title
def search(s):
  s = s.lower()
  indx = df.index[(df['Title'].str.contains(s, case = False))==True]   
  indx = np.array(indx)
  indx = indx.astype(int)
  return indx

# Main Function for Similar Noes
def check_sim(val):
    if val == NULL:
        st.write("Hello")
    else:
        temp = int(val)
        if(temp in n_sim):
            pro_id = temp
            pro_dict = G_Sim.nodes[pro_id]
            arr = pro_dict['Copurchased']
            arr = arr.split(' ')
            arr = np.array(arr)
            if len(arr) == 0:
                st.write("No results")
            else:
                html_temp = """
                <div style="background-color:tomato;padding:10px">
                <h2 style="color:white;text-align:center;">Similar Products</h2>
                </div>
                """
                st.markdown(html_temp,unsafe_allow_html=True)
                counter, indarr = getsimilar(arr)
                print(counter,"nodes have been removed from the graph")
                print(pro_dict)
        else:
            st.write("Empty node has been removed from the graph!")

# Function to Show Titles
def showtitles(array):
    titles = []
    for i in range(len(array)):
        titles.append(G_Rec.nodes[array[i]]['title'])
    return titles

# Function to Show ASIN
def showasin(array):
    asins = []
    for i in range(len(array)):
        asins.append(G_Rec.nodes[array[i]]['ASIN'])
    asins = np.array(asins)
    #asins = asins.astype(int)
    return asins

# Main Function for Recommended Nodes
def check_rec(val):
    if val == NULL:
        st.write("Hello")
    else:
        temp = int(val)
        if(temp in n_rec):
            pro_id = temp
            finalresult = []
            resultarray = np.unique(getclean(pro_id))
            for i in range(1, len(resultarray)):
                if(resultarray[i] in n_rec):
                    finalresult.append(resultarray[i])
                else:
                    st.write("Empty node has been removed from the graph!")
    t = showtitles(finalresult)
    finaldictjaccard = gethighestjaccard(pro_id, finalresult)
    finaldictjaccard = dict(sorted(finaldictjaccard.items(), key=lambda item: item[1], reverse = True))
    top5jac = np.array(list(finaldictjaccard.keys()))[:5]
    st.write("   ")
    # st.markdown("**Recommended Products Are:**")
    values = showtitles(top5jac)
    for top5 in values:
        st.write(top5)

# Getting a Sub Dictionary
def getsubdict(d):
    required_keys = ('group' ,'num_categories', 'totalreviews', 'downloadedreviews', 'avg_rating')
    subdict = {x: d[x] for x in required_keys if x in d}
    return subdict

# Function to Find Jaccard Similarity Between 2 Lists
def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(set(list1)) + len(set(list2))) - intersection
    return float(intersection) / union

# Getting Highest Jaccard Similarity using jaccard function
def gethighestjaccard(pro_id, finalresult):
  jaccdict = {}    
  for i in range(0,len(finalresult)):     
    if(pro_id != i):      
      tempneighbours = []
      resarray = getclean(finalresult[i])        
      jaccdict[finalresult[i]] = jaccard_similarity(finalresult, resarray)
  return jaccdict

# Main Function to Wrap all Things
def main():
    st.text("Made By Pratinav Seth, Yaswanth B, Siddharth Singh")
    st.title("Product Recommendation")

    # Similar Products
    val = st.text_input("Enter Product Name")
    iarray = search(val)
    iarray_names = []
    if len(iarray) == 0:
        st.write("Product Does Not Exist")
    else:
        for i in range(0, len(iarray)):
            if(iarray[i] in n_sim):
                pro_id = int(iarray[i])
                iarray_names.append(G_Sim.nodes[iarray[i]]['Title'])
        name = st.selectbox("Select", iarray_names)
        st.write("    ")
        prod_id = search(name)
        check_sim(prod_id)

    # Recommended Products
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Recommended Products</h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    if len(iarray) == 0:
        st.write("Product Does Not Exist")
    else:
        for i in range(0, len(iarray)):
            if(iarray[i] in n_sim):
                pro_id = int(iarray[i])
                iarray_names.append(G_Rec.nodes[iarray[i]]['title'])
        prod_id = search(name)
        check_rec(prod_id)


if __name__=='__main__':
    main()
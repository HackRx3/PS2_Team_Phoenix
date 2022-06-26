from asyncio.windows_events import NULL
import numpy as np
import pandas as pd
import streamlit as st
import networkx as nx
from PIL import Image
from streamlit_option_menu import option_menu

img = Image.open('download.png')
st.set_page_config(page_title='Product Recommender Engine' , page_icon=img, layout="centered",initial_sidebar_state="expanded")
hide_st_style = """
            <style>
            #MainMenu {visibility: visible;}
            footer {visibility: visible;}
            footer:after{
                background-color:#99CCCC;
                font-size:12px;
                font-weight:8px;
                height:30px;
                margin:1rem;
                padding:0.8rem;
                content:'By Pratinav Seth, Yaswanth B, Siddharth Singh';
                display: flex;
                align-items:center;
                justify-content:center;
                color:black;
            }
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu(
                menu_title="Team Phoenix",  
                options=["Recommendations", "About"],  
                icons=["main", "person-square"],  
                menu_icon="cast",
                default_index=0,  
                 styles={
                "container": {"padding": "3", "background-color": "#f0f2f6" , "Font-family":"Monospace"},
                "icon": {"color": "#31333f", "font-size": "25px"}, 
                "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px","Font-family":"Monospace"},
                "nav-link-selected": {"background-color": "#0072bc"},
                }
                )

    if selected == "Recommendations":
      st.empty()
    
    if selected == "About":
        st.markdown("""<div style='
            background-color:#99CCCC; 
            padding:1rem;
            font-size:17px;
            border-radius:8px;
            text-align: justify;
           '>
Build an app with a simple UI which will allow the user to search for products and give recommendations and similar products.
            <a href="https://github.com/HackRx3/PS2_Team_Phoenix">Github Repository</a>
</div>
        <br>
       """
        ,unsafe_allow_html=True,)


# Datasets of Similarities and Recommendations
df = pd.read_csv('pdssimilar (2).csv')
df_rec = pd.read_csv('finalpreprocesseddata.csv')
df1 = pd.read_csv("customer_insights_recommendations2.csv")

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

title_cluster0 = ["Change Your Child's Behavior by Changing Yours...",
                  "Practical Aspects of Interview and Interrogati...",
                  "Practical Aspects of Interview and Interrogati...",
                  "Results-Oriented Job Descriptions: More Than 2...",
                  "Decorative Letters CD-ROM and Book (Dover Elec...",
                  "Log Cabins (Architecture and Design Library)"     ,
                  "Berlioz: Symphonie fantastique",
                  "Smith & Hawken: Hands On Gardener: Composting ...",
                  "Beauty in Exile: The Artists, Models, and Nobi...",
                  "Grammar Wars: 179 Games and Improvs for Learni..."
                ]

title_cluster1 = ["Visualizing Data	",
                  "Remembering Farley",
                  "Northrop Frye on Shakespeare",
                  "Zappa in N.Y.	",
                  "Where the Birds Are: The 100 Best Birdwatching...	",
                  "The Wasp Cookbook	",
                  "The Supreme Court's Greatest Hits",
                  "I Know Why the Caged Bird Sings (Cliffs Notes)",
                  "Color, Environment, & Human Response",
                  "Miles to Go",
                ]

title_cluster2 = ["Thief of Hearts",
                  "Harry Potter and the Goblet of Fire (Book 4 Au...",
                  "Harry Potter and the Goblet of Fire (Book 4, A...	",
                  "Harry Potter and the Goblet of Fire (Book 4)",
                  "Harry Potter and the Goblet of Fire (Book 4)",
                  "Harry Potter and the Goblet of Fire (Book 4)",
                  "Looking For-Best of David Hasselhoff",
                  "Harry Potter and the Sorcerer's Stone (Book 1 ...",
                  "Harry Potter and the Sorcerer's Stone (Book 1 ...",
]

top5_rec = ["Harry Potter and the Goblet of Fire (Book 4)",
            "Looking For-Best of David Hasselhoff	",
            "Harry Potter and the Sorcerer's Stone (Book 1 ...",
            "Remembering Farley",
            "The Supreme Court's Greatest Hits"
]

flag = 0

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

# Main Function for Similar Nodes
def check_sim(val):
    
    val = val[0]
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
                st.write("No Similar Products were Found")
                st.write("Here are Top 5 Products")
                st.write("")
            else:
                html_temp = """
                <div style="background-color:#0072bc;padding:10px">
                <h2 style="color:white;text-align:center;">Similar Products</h2>
                </div>
                """
                st.markdown(html_temp,unsafe_allow_html=True)
                counter, indarr = getsimilar(arr)
                print(counter,"nodes have been removed from the graph")
                print(pro_dict)
        else:
            flag = 1
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
    if flag == 1:
        st.write("Empty Node has been removed from the graph")
        return
    val = val[0]
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

# Jaccard Function
def jaccard(a, b):
    a = set((str(a)).split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

def prod_label_recomm(x_counter):
    if flag == 1:
        st.write("Empty Node has been removed from the graph")
        return
    else:
        if x_counter == NULL:
             print("Hello")
        else:
            # get label of asin
            df_counter = df1.loc[df1['ASIN'] == x_counter]
            x = int(df_counter['label_code'])
            y = set((str(df_counter['Categories'])).split())
            df_counter = df1.loc[df1['label_code'] == x]
            df_counter = df_counter.loc[df_counter['AvgRating']>=4.5]
            df_counter['score_cat_inter']= df_counter['Categories'].apply(lambda x: jaccard(x,y))
            sorted_df = df_counter.sort_values(["score_cat_inter"], ascending=False)
            return sorted_df[1:6]['ASIN'].tolist()

def show(values):
    t = []
    for i in range(len(values)):
        t.append(df1['Title'][i])
    return t

# Main Function to Wrap all Things
def main():
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
        name = st.selectbox("Select Product", iarray_names)
        st.write("    ")
        prod_id = search(name)
        if len(prod_id) == 0:
            st.write("Product Not Found")
            st.write("**You Might Like These Products**")
            for t in top5_rec:
                st.write(t)
            return
        check_sim(prod_id)

    # Recommended Products
    html_temp = """
    <div style="background-color:#0072bc;padding:10px">
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
        if len(prod_id) == 0:
            st.write("Product Not Found")
            st.write("**You Might Like These Products**")
            for t in top5_rec:
                st.write(t)
            return
        check_rec(prod_id)

    # Clustering Products
    html_temp = """
    <div style="background-color:#0072bc;padding:10px">
    <h2 style="color:white;text-align:center;">Clustering Products</h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    asin_val = (showasin(prod_id))
    st.write("  ")
    st.markdown("**Customer Might Also Like**")
    for val in asin_val:
        values = (prod_label_recomm(val))
    val = show(values)
    if len(val) == 0:
        st.write("Product Not Found")
        st.write("**You Might Like These Products**")
        for t in top5_rec:
            st.write(t)
        return
    for v in val:
        st.write(v)

    st.write(" ")
    st.write(" ")
    st.markdown("**Top Products of Cluster 1**")
    for title in title_cluster0:
        st.write(title)
    
    st.write(" ")
    st.write(" ")
    st.markdown("**Top Products of Cluster 2**")
    for title in title_cluster1:
        st.write(title)

    st.write(" ")
    st.write(" ")
    st.markdown("**Top Products of Cluster 3**")
    for title in title_cluster2:
        st.write(title)

if __name__=='__main__':
    main()
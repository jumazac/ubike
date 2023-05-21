import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



# Load your data

# Load your data
df = pd.read_csv("TOTAL1.csv")

# Reduce to two levels for simplicity
levels = ['SEX', 'YEAR']

# Simplify the dataframe building function
def build_hierarchical_dataframe(df, levels):
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value'])
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value'])
        dfg = df.groupby(levels[i:]).size().reset_index(name='value')
        df_tree['id'] = dfg[level].copy()
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i+1]].copy()
        else:
            df_tree['parent'] = 'total'
        df_tree['value'] = dfg['value']
        df_all_trees = pd.concat([df_all_trees, df_tree], ignore_index=True)
        
    total = pd.Series(dict(id='total', parent='', 
                           value=df.shape[0]))  # Count total rows as the root value
    df_all_trees = pd.concat([df_all_trees, pd.DataFrame(total).T], ignore_index=True)
    return df_all_trees

df_all_trees = build_hierarchical_dataframe(df, levels)

fig = go.Figure()

fig.add_trace(go.Sunburst(
    ids=df_all_trees['id'],
    parents=df_all_trees['parent'],
    values=df_all_trees['value'],
    hovertemplate='<b>%{label} </b> <br> Value: %{value}<br> Percentage of Total: %{percent:.2%}',
    maxdepth=2
))

fig.update_layout(margin=dict(t=10, b=10, r=10, l=10))

st.plotly_chart(fig)


# Load your data
df = pd.read_csv("TOTAL1.csv")

# Display the DataFrame in Streamlit
st.dataframe(df)


import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode


def build_aggrid_table(df, col_defs=None):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(enabled=False)
    gb.configure_default_column(resizable=True, filter=False, sortable=True)

    grid_options = gb.build()

    # Apply custom column defs if provided
    if col_defs:
        grid_options["columnDefs"] = col_defs
    else:
        grid_options["autoSizeStrategy"] = {"type": "fitCellContents"}


    row_style = JsCode("""
        function(params) {
            if (params.node.rowIndex % 2 === 0) {
                return {'background-color': '#ffc1c1', 'color': 'black'};
            } else {
                return {'background-color': '#ffffff', 'color': 'black'};
            }
        }
    """)
    grid_options["getRowStyle"] = row_style

    custom_css = {
        ".ag-header-cell": {
            "background-color": "#1976d2 !important",
            "color": "white !important",
            "font-weight": "bold !important",
            "text-align": "center"
        }
    }

    return AgGrid(
        df,
        gridOptions=grid_options,
        height=340,
        allow_unsafe_jscode=True,
        custom_css=custom_css
    )
    
def render_player_card(player_row, stat_label, stat_value):
    """
    Render a single player card with a modern and clean design.
    """
    player_name = player_row["Name"]
    code = player_row["photo_code"]
    photo_url = f"https://resources.premierleague.com/premierleague25/photos/players/110x140/{code}.png"

    st.markdown(
        f"""
        <div style="
            font-family: 'Segoe UI', Roboto, sans-serif;
            background: #fff0f5;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            border: 1px solid #e1e4e8;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 15px;
        ">
            <img src="{photo_url}" style="
                width: 80px;
                height: 82px;
                border-radius: 50%;
                border: 3px solid #f0f0f0;
                margin-bottom: 15px;
                object-fit: cover;
                object-position: 0 -5%;
            "><br>
            <strong style="
                font-size: 1.1em;
                font-weight: 600;
                color: #333;
                display: block;
                margin-bottom: 5px;
            ">{player_name}</strong>
            <span style="font-size: 0.8em; color: #6a737d;">
                {stat_label}: 
                <span style="color: #000; font-weight: 700;">{stat_value}</span>
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
def render_title_with_bg(title_text):
    """
    Renders a centered title with a light background and rounded corners.
    """
    st.markdown(
        f"""
        <div style="
            padding: 1px; 
            border-radius: 10px; 
            text-align: center; 
            margin-bottom: 10px;
            border: 1px solid #white;
        ">
            <h2 style="
                font-family: 'Segoe UI', Roboto, sans-serif; 
                color: white; 
                font-weight: 700;
                font-size: 24px;
                margin: 0;
            ">{title_text}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
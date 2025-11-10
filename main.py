import streamlit as st
st.set_page_config(page_title='home', layout='wide')
st.markdown('<h2 style="text-align: center;">Numerical Methods using streamlit webapp</h2>', unsafe_allow_html=True)
st.markdown('<h4 style="text-align: center;">A guide for your complex formulas</h4>',  unsafe_allow_html=True)
st.divider()
with st.container(horizontal_alignment='center', width='stretch'):
    method = st.selectbox(label='choose a method',width=600,
             options=['bisection method', 
                    'newton\'s ralph method',
                    'secant method',
                    'fixed point iteration method'])
    if method == 'bisection method':
        with st.form(key= 'bisection_method_form', width=600):
            formula = st.text_input(label='Enter your formula')
            col1, col2 = st.columns(spec=[1,1])
            col1.number_input(label= 'x1')
            col1.number_input(label='number of iteration', step=1)
            col2.number_input(label= 'x2')
            col2.number_input(label='tolerance value')
            st.form_submit_button()
    elif method == 'newton\'s ralph method':
        with st.form(key= 'newton_method_form', width=600):
            formula = st.text_input(label='Enter your formula')
            col1, col2 = st.columns(spec=[1,1])
            col2.number_input(label='tolerance value')
            col1.number_input(label='number of iteration', step=1)
            st.form_submit_button()
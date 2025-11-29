import streamlit as st
import sympy as sp
import pandas as pd
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
    if method in ['bisection method', 'secant method']:
        with st.form(key= 'bisection_method_form', width=600):
            col1, col2 = st.columns(spec=(12,1))
            formula = st.text_input(label='Enter your formula')
            col3, col4 = st.columns(spec=[1,1])
            x1 = col3.number_input(label= 'x1', value=None, format="%0.9f")
            i = col3.number_input(label='number of iteration', step=1, value=None)
            x2 = col4.number_input(label= 'x2', value=None, format="%0.9f")
            fixed_tolerance_value = col4.number_input(label='tolerance value')
            sumbitted = st.form_submit_button(width='stretch')
    elif method in ['newton\'s ralph method', 'fixed point iteration method']:
        with st.form(key= 'newton_method_form', width=600):
            formula = st.text_input(label='Enter your formula')
            initial_point = st.number_input(label='initial number')
            col1, col2 = st.columns(spec=[1,1])
            col2.number_input(label='tolerance value')
            col1.number_input(label='number of iteration', step=1)
            sumbitted =st.form_submit_button(width='stretch') 
   
class calculation:
    def __init__(self, formula, x1, x2, i=None, tolerance_value=None):
        self.formula = formula
        self.x1 = x1
        self.x2 = x2
        self.i = i
        self.tolerance_value = tolerance_value
        self.x = sp.symbols('x')
        self.variable = sp.simplify(formula)
        self.x1_answer = self.variable.subs(self.x, x1)
        self.output = {}
    def iteration(self, formula, x1, x2, i=None, tolerance_value=None):
        pass
    def appending(self, x1_data, x1_answer_data, x2_data, x2_answer_data, **kwargs):
        self.out_put = {'x1': x1_data, 
                   'value at x1' : x1_answer_data, 
                   'x2': x2_data, 
                   'value at x2': x2_answer_data}
        if kwargs is not None:
            self.out_put.update(kwargs)
        df = pd.DataFrame(self.out_put, index=range(1, len(x1_data) + 1, 1))
        return df
class bisection(calculation):
    def __init__(self, formula, x1, x2, i=None, tolerance_value=None):
        super().__init__(formula, x1, x2, i, tolerance_value)
        self.x2_answer = self.variable.subs(self.x, x2)
        self.x1_data = []
        self.x2_data = []
        self.x1_answer_data = []
        self.x2_answer_data = []
        self.x3 = float((self.x1 + self.x2) / 2)
        self.x3_data = []
        self.x3_answer = self.variable.subs(self.x, self.x3)
        self.x3_answer_data = []
        self.tolerance_value = (self.x2 - self.x1) / 2
        self.tolerance_value_data = []
    def evaluating_by_iteration(self):
        zero = lambda x, y: 'x1' if x == 0 else 'x2'
        if self.x1 is None or self.x2 is None or self.i is None:
            return f'enter the '
        elif self.x1_answer * self.x2_answer > 0:
            return 'zero is not found in the range'
        elif self.x1_answer * self.x2_answer == 0:
            return f'zero is found on {(zero(self.x1_answer, self.x2_answer))}'
        elif self.i is not None:
            for iter in range(self.i):
                self.x1_data.append(self.x1)
                self.x2_data.append(self.x2)
                self.x3_data.append(self.x3)
                self.x1_answer_data.append(self.x1_answer)
                self.x2_answer_data.append(self.x2_answer)
                self.x3_answer_data.append(self.x3_answer)
                self.tolerance_value_data.append(self.tolerance_value)
                if self.x3_answer == 0:
                    break
                elif self.x1_answer * self.x3_answer > 0:
                    self.x1 = self.x3
                    self.x3 = (self.x1 + self.x2) / 2
                    self.x3_answer = self.variable.subs(self.x, self.x3)
                    self.x1_answer = self.variable.subs(self.x, self.x1)
                    self.tolerance_value = (self.x2 - self.x1) / 2
                else:
                    self.x2 = self.x3
                    self.x3 = (self.x1 + self.x2) / 2
                    self.x3_answer = self.variable.subs(self.x, self.x3)
                    self.x2_answer = self.variable.subs(self.x, self.x2)
                    self.tolerance_value = (self.x2 - self.x1) / 2
            kwargs = {'x3': self.x3_data, 'value at x3': self.x3_answer_data, 'tolerance value': self.tolerance_value_data}
            bitch  = self.appending(self.x1_data, self.x1_answer_data, self.x2_data, self.x2_answer_data, **kwargs)
            return bitch
    def evaluating_by_tolerance_value(self):
        while fixed_tolerance_value > self.tolerance_value:
            pass

becalculate = bisection(formula, x1, x2, i)
kwargs = {'hello': [1,4,5]}

if sumbitted:
    if method == 'bisection method':
        if i is not None:
            
            st.write(becalculate.evaluating_by_iteration())
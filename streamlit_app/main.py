import streamlit as st
import sympy as sp
import pandas as pd
st.set_page_config(page_title='home', layout='wide')
st.markdown('<h2 style="text-align: center;">Numerical Methods using streamlit webapp</h2>', 
            unsafe_allow_html=True)
st.markdown('<h4 style="text-align: center;">A guide for your complex formulas</h4>',  
            unsafe_allow_html=True)
st.divider()

with st.container(horizontal_alignment='center', width='stretch'):
    method = st.selectbox(label='choose a method',width=600,
             options=['bisection method', 
                    'newton raphson method',
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
            fixed_tolerance_value = col4.number_input(label='tolerance value', 
                                                      value=None, 
                                                      format="%0.13f")
            sumbitted = st.form_submit_button(width='stretch')
    elif method in ['newton raphson method', 'fixed point iteration method']:
        with st.form(key= 'newton_method_form', width=600):
            formula = st.text_input(label='Enter your formula')
            x1 = st.number_input(label='initial number', value= None)
            col1, col2 = st.columns(spec=[1,1])
            fixed_tolerance_value = col2.number_input(label='tolerance value', value=None, format="%0.13f" )
            i = col1.number_input(label='number of iteration', step=1, value=None)
            sumbitted =st.form_submit_button(width='stretch') 
   
class calculation:
    def __init__(self, formula, x1, x2, i=None, tolerance_value=None):
        self.formula = formula
        self.x1 = x1
        self.x2 = x2
        self.i = i
        self.x = sp.symbols('x')
        self.variable = sp.simplify(formula)
        self.x1_answer = self.variable.subs(self.x, x1)
        self.x1_data = []
        self.x1_answer_data = []
        self.tolerance_value_data = []
        self.x2_data = []
        self.x2_answer_data = []
        self.fixed_tolerance_value = fixed_tolerance_value
        self.output = {}
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
        self.x3 = float((self.x1 + self.x2) / 2)
        self.x3_data = []
        self.x3_answer = self.variable.subs(self.x, self.x3)
        self.x3_answer_data = []
        self.tolerance_value = (self.x2 - self.x1) / 2
    def solving_the_equation(self):
        nothing = lambda x, y: 'x1' if x1 is None else 'x2'
        zero = lambda x, y: 'x1' if x == 0 else 'x2'
        if self.x1 is None or self.x2 is None:
            return f'enter the {nothing}'
        elif self.x1_answer * self.x2_answer > 0:
            return 'zero is not found in the range'
        elif self.x1_answer * self.x2_answer == 0:
            return f'zero is found on {(zero(self.x1_answer, self.x2_answer))}'
        elif i is not None:
            return self.evaluating_by_iteration()
        else:
            return self.evaluating_by_tolerance_value()
    def the_iteration(self, x1, x2, x3, x1_answer, x2_answer, x3_answer, tolerance_value, i = 1):
        self.x1_data.append(x1)
        self.x2_data.append(x2)
        self.x3_data.append(x3)
        self.x1_answer_data.append(x1_answer)
        self.x2_answer_data.append(x2_answer)
        self.x3_answer_data.append(x3_answer)
        self.tolerance_value_data.append(tolerance_value)
        if tolerance_value <= self.fixed_tolerance_value or i == self.i:
            kwargs = {'x3': self.x3_data, 
                    'value at x3': self.x3_answer_data, 
                    'tolerance value': self.tolerance_value_data}
            df  = self.appending(self.x1_data, 
                                self.x1_answer_data, 
                                self.x2_data, 
                                self.x2_answer_data, 
                                **kwargs)
            return df
        if x1_answer * x3_answer > 0:
            new_x1, new_x2 = x3, x2
        else:
            new_x1, new_x2 = x1, x3
        new_x3 = (new_x1 + new_x2) / 2
        return self.the_iteration(
            new_x1, new_x2, new_x3,
            self.variable.subs(self.x, new_x1),
            self.variable.subs(self.x, new_x2),
            self.variable.subs(self.x, new_x3),
            abs(new_x2 - new_x1) / 2, i + 1)
    def evaluating_by_iteration(self):
        return self.the_iteration(self.x1, 
                                self.x2, 
                                self.x3, 
                                self.x1_answer, 
                                self.x2_answer, 
                                self.x3_answer, 
                                self.tolerance_value)
    def evaluating_by_tolerance_value(self):
        return self.the_iteration(self.x1, 
                                self.x2, 
                                self.x3, 
                                self.x1_answer, 
                                self.x2_answer, 
                                self.x3_answer, 
                                self.tolerance_value)
    
class newton_raphson(calculation):
    def __init__(self, formula, x1, i=None, tolerance_value=None):
        super().__init__(formula, x1, i, tolerance_value)
        self.f_x = self.variable.subs(self.x, x1)
        self.derivative_formula = sp.diff(self.formula, self.x)
        self.derivative_formula = sp.simplify(self.derivative_formula)
        self.df_x = self.derivative_formula.subs(self.x, x1)
        self.x2 = self.x1 - (self.f_x / self.df_x)
        self.x2_answer = self.variable.subs(self.x, self.x2)
        self.tolerance_value = abs(self.x2 - self.x1)
    def solving_the_equation(self):
        zero = lambda x, y: 'x1' if x == 0 else 'x2'
        if self.x1 is None:
            return f'enter the x1 value'
        elif i is not None:
            return self.evaluating_by_iteration()
        else:
            return self.evaluating_by_tolerance_value()
    def the_iteration(self, x1, x2, x1_answer, x2_answer, tolerance_value, i = 1):
        self.x1_data.append(x1)
        self.x2_data.append(x2)
        self.x1_answer_data.append(x1_answer)
        self.x2_answer_data.append(x2_answer)
        self.tolerance_value_data.append(tolerance_value)
        if tolerance_value <= self.fixed_tolerance_value or i == self.i:
            kwargs = {'tolerance value': self.tolerance_value_data}
            df  = self.appending(self.x1_data, 
                                self.x1_answer_data, 
                                self.x2_data, 
                                self.x2_answer_data, 
                                **kwargs)
            return df
        new_x1 = x2
        self.f_x = self.variable.subs(self.x, new_x1)
        self.df_x = self.derivative_formula.subs(self.x, new_x1)
        new_x2 = new_x1 - (self.f_x / self.df_x)
        return self.the_iteration(
            new_x1, new_x2,
            self.variable.subs(self.x, new_x1),
            self.variable.subs(self.x, new_x2),
            abs(new_x2 - new_x1), i + 1)
    def evaluating_by_iteration(self):
        return self.the_iteration(self.x1,
                                self.x2,   
                                self.x1_answer, 
                                self.x2_answer, 
                                self.tolerance_value)
    def evaluating_by_tolerance_value(self):
        return self.the_iteration(self.x1,
                                self.x2, 
                                self.x1_answer,  
                                self.x2_answer, 
                                self.tolerance_value)
        

if method == 'bisection method':
    becalculate_for_bisection = bisection(formula, x1, x2, i, fixed_tolerance_value)
becalculate_for_newton = newton_raphson(formula, x1, i, fixed_tolerance_value)

if sumbitted:
    if method == 'bisection method':
        st.write(becalculate_for_bisection.solving_the_equation())
    elif method == 'newton raphson method':
        st.write(becalculate_for_newton.solving_the_equation())
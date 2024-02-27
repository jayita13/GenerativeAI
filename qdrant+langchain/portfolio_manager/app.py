import streamlit as st
import earning_report_analysis
import stock_price_evaluator

selected_company = st.selectbox(
    'Select your stock from portfolio list',
    ('Alphabet', 'Apple', 'Tesla', 'Microsoft', 'Walmart'))

st.write('You selected:', selected_company)
if st.button('Performance Report'):
    analysed_report = earning_report_analysis.get_company_analysis(selected_company)
    price_performance = stock_price_evaluator.get_daily_price_performance(selected_company)
    final_user_report = analysed_report + "\n\n" + price_performance
    st.write(final_user_report)
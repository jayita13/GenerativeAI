import gradio as gr
import earning_report_analysis
import stock_price_evaluator

def analyze_stock(selected_company):
    analysed_report = earning_report_analysis.get_company_analysis(selected_company)
    price_performance = stock_price_evaluator.get_daily_price_performance(selected_company)
    final_user_report = analysed_report + "\n\n" + price_performance
    return final_user_report

dropdown = gr.Dropdown(['Alphabet', 'Apple', 'Tesla', 'Microsoft', 'Walmart'], 
                label="Select your stock from portfolio list")
output_text = gr.Textbox()

def get_report(selected_company):
    return analyze_stock(selected_company)

demo = gr.Interface(fn=get_report, inputs=[dropdown], 
                    outputs=output_text, 
                    title="Stock Performance Report")
# demo.launch()

import openai
import pandas as pd
import db_stocks_news as news
openai.api_key = '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'

def user_req():
    num_stocks = 3
    return num_stocks

if __name__ == "__main__":

    stock_df = pd.read_excel('src/atradebot/SP_500_Companies.xlsx')
    symbols = stock_df['Symbol'].tolist()
    stock_df['sentiment_counter'] = 0

    for result in news.ResultSet:
        text_to_analyze = result[1] + ' ' + result[5]
        prompt = f"Analyze the sentiment of the following text and provide a one-word sentiment: '{text_to_analyze}'"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            prompt = prompt
        )
        sentiment = (response.choices[0].text.strip()).lower()
        if (sentiment == "positive"):
            sentiment_num = 1
        elif (sentiment == "negative"):
            sentiment_num = -1
        elif (sentiment_num == "neutral"):
            sentiment_num = 0
        
        sent_count_index_x = symbols.index(result[0])
        stock_df.at[sent_count_index_x, 'sentiment_counter'] += sentiment_num
    
    
    num_stocks = user_req()
    largest_values = stock_df['sentiment_counter'].nlargest(num_stocks)

    # Convert to a DataFrame with index numbers and values
    result_df = pd.DataFrame({
        'Index': largest_values.index,
        'Value': largest_values.values
    })
    
    
    for i in list(result_df['Index']):
        print("Stock Name:",stock_df[i]["symbol"])
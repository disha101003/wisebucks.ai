import requests

API_URL = "https://api-inference.huggingface.co/models/ahmedrachid/FinancialBERT-Sentiment-Analysis"
API_TOKEN = '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'
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Choose which test case to run below:

testA = ' Apple today announced financial results for its fiscal 2023 third quarter ended July 1, 2023. The Company posted quarterly revenue of $81.8 billion, down 1 percent year over year, and quarterly earnings per diluted share of $1.26, up 5 percent year over year. ' \
        'We are happy to report that we had an all-time revenue record in Services during the June quarter, driven by over 1 billion paid subscriptions, and we saw continued strength in emerging markets thanks to robust sales of iPhone,” said Tim Cook, Apple’s CEO. “From education to the environment, we are continuing to advance our values, while championing innovation that enriches the lives of our customers and leaves the world better than we found it.' \
        'Our June quarter year-over-year business performance improved from the March quarter, and our installed base of active devices reached an all-time high in every geographic segment,” said Luca Maestri, Apple’s CFO. “During the quarter, we generated very strong operating cash flow of $26 billion, returned over $24 billion to our shareholders, and continued to invest in our long-term growth plans.' \
        'Apple’s board of directors has declared a cash dividend of $0.24 per share of the Company’s common stock. The dividend is payable on August 17, 2023 to shareholders of record as of the close of business on August 14, 2023.'

testB = 'Revenues for the quarter and nine months grew 4% and 8%, respectively. ' \
        '• Diluted earnings per share (EPS) from continuing operations for the quarter was a loss of $0.25' \
        'compared to income of $0.77 in the prior-year quarter. ' \
        '• Excluding certain items(1), diluted EPS for the quarter was $1.03, down from $1.09 in the prioryear quarter. ' \
        '• EPS from continuing operations for the nine months ended July 1, 2023 decreased to $1.14 from' \
        '$1.66 in the prior-year period. ' \
        '• Excluding certain items(1), diluted EPS for the nine months ended July 1, 2023 decreased to $2.94' \
        'from $3.22 in the prior-year period.'


def sort_sentiment(list_dict):
    new_list = [{}, {}, {}]
    max_val = 0
    max = ''
    for dict in list_dict:
        if dict['label'] == 'positive':
            if dict['score'] > max_val:
                max = 'positive'
                max_val = dict['score']
            new_list[0] = dict
        elif dict['label'] == 'neutral':
            if dict['score'] > max_val:
                max = 'neutral'
                max_val = dict['score']
            new_list[1] = dict
        else:
            if dict['score'] > max_val:
                max = 'negative'
                max_val = dict['score']
            new_list[2] = dict

    return new_list, max, max_val


# the double for loop separates sentences and their main clauses.

for i in testB.split('. '):
    for j in i.split('and '):
        print(j + '\n')
        output = query({
            "inputs": f"{j}",
        })
        result, max, max_val = sort_sentiment(output[0])
        print(max, f"{round(max_val, 3) * 100}%")
        # print(result[0])
        # print(result[1])
        # print(result[2])
        print('')

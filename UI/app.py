from flask import Flask, render_template, request
import pickle
import json
import pandas as pd

app = Flask(__name__, template_folder="template")

app.config['SECRET_KEY'] = "mysecretkey"

@app.route('/', methods=["GET", "POST"])
def main_page():
    print('---Opening File---')
    dominant_topic_df = pickle.load(open('vader_no_neutrals.pkl', 'rb'))
    print('---File Opened---')
    topic_dict = {'Network & Storage': 0, 'Multimedia': 2, 'Screen': 3, 'Battery': 5, 'Pricing': 7}
    if request.method == "GET":
        categories = topic_dict.keys()
        all_phones = sorted(list(set(dominant_topic_df['phone_model'])))
        return render_template('home.html', categories=categories, all_phones=all_phones)
    else:
        if 'category' in request.form:
            print('---Reading Category---')
            user_cat = request.form['category']
            topic_num = topic_dict[user_cat]

            user_select_df = dominant_topic_df[dominant_topic_df['Dominant Topic'] == topic_num].sort_values(by='compound', ascending=False)
            top_5 = user_select_df.iloc[:5]
            bot_5 = user_select_df.iloc[-5:]
            top_bot_5 = {'pos': top_5.to_json(orient='records'), 'neg':bot_5.to_json(orient='records')}
            print(top_bot_5)

            return top_bot_5

        elif 'model' in request.form:
            print('---Reading Phone Model---')
            user_model = request.form['model']
            model_select = dominant_topic_df[dominant_topic_df['phone_model'] == user_model]
            overall_review_dict = {}

            for title, topic in topic_dict.items():
                user_df = model_select[model_select['Dominant Topic'] == topic]
                review_len = len(user_df)
                if review_len == 0:
                    overall_review_dict[title] = ['No Reviews', review_len]
                else:
                    overall_review_dict[title] = [round(user_df['compound'].mean(), 2), review_len]
            
            print(overall_review_dict)
            return json.dumps(overall_review_dict)
            


if __name__ == '__main__':
    app.run(debug=True, port=3000)

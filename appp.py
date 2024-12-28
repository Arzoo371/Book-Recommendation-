from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

# Load pre-trained data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('sim.pkl', 'rb'))

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
        book_name=list(popular_df['Book-Title'].values),
        author=list(popular_df['Book-Author'].values),
        image=list(popular_df['Image-URL-M'].values),
        votes=list(popular_df['num_ratings'].values),
        rating= list(popular_df['avg_rating'].values)
    )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]



    similar_items = sorted(list(enumerate(similarity_scores[index])), reverse=True, key=lambda x: x[1])[1:5]
    data = []
    for i in similar_items:
        item = []

        temp_df = (books[books['Book-Title'] == pt.index[i[0]]])
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)
    return render_template('recommend.html', data=data)
if __name__ == '__main__':  # Fixed typo in the conditional
    app.run(debug=True)
from flask import Flask, request, redirect

app = Flask(__name__)

#이러한 정보를 데이터베이스에 저장하여 관리함
topics = [
    {'id' : 1, 'title' : 'Americano', 'body' : 'Americano is ..'},
    {'id' : 2, 'title' : 'Latte', 'body' : 'Latte is ...'},
    {'id' : 3, 'title' : 'Caffe Mocha', 'body' : 'Mocha is ...'}
]

def template(contents, title, body, id=None):
    contextUI = ''
    if id != None:
        contextUI = f'''
            <li><a href="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}" method="POST"><input type="submit" value="delete"></form></li>
        '''
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">Coffee</a></h1>
            <ol>
                {contents}
            </ol>
            <h2>{title}</h2>
                <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
                </ul>
            {body}
        </body>
    </html>
    '''

def getContents():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags

@app.route('/')
def index():
    
    return template(getContents(), "Welcome", "Hello, Coffee")

@app.route('/read/<int:id>/')
def read(id):
    title = ''
    body = ''
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break
    print(title, body)
    return template(getContents(), title, body, id)

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
            '''
        return template(getContents(), 'create', content)
    elif request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id': len(topics)+1, 'title': title, 'body':body}
        topics.append(newTopic)
        url = '/read/'+ str(newTopic['id'])+'/'

        return redirect(url)

@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    title = ''
    body = ''
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break

    if request.method == 'GET':
        content = f'''
            <form action="/update/{id}" method="POST">
                <p><input type="text" name="title" placeholder="title" value="{title}"></p>
                <p><textarea name="body" placeholder="body">{body}</textarea></p>
                <p><input type="submit" value="update"></p>
            </form>
            '''
        return template(getContents(), 'update', content)
    elif request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break

        
        url = '/read/'+ str(id)+'/'

        return redirect(url)

@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    return redirect('/')


app.run(port=5000, debug=True)
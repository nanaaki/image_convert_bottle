from bottle import route, run, request
from PIL import Image

@route('/test')
def test():
    html = '\
    <p><form enctype="multipart/form-data" action="/upload" method="post"></p>\
    <p>  <input name="data" type="file"></p>\
    <p>  <input name="submit" value="generate" type="submit"></p>\
    <p></form></p>'
    return html

@route('/upload', method='POST')
def upload():
    data = request.files.data
    data.save('./tmp.png', overwrite=True)
    p = Image.open('./tmp.png')
    gray = p.convert('L')
    bw = gray.point(lambda x: 0 if x<128 else 1, '1')
    res = []
    x, y = bw.size
    for j in range(y):
        res.append(','.join([str(bw.getpixel((i,j))) for i in range(x)]))
    return '\n'.join(res)


if __name__ == '__main__':
    run(host='127.0.0.1', port=9000)

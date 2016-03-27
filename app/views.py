#!flask/bin/python
import six
from flask import Flask, jsonify, abort, request, make_response, url_for
import requests
from bs4 import BeautifulSoup
import urlparse
from app import app

#app = Flask(__name__, static_url_path="")


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'],
                                      _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@app.route('/api/thumbnail/process', methods=['POST'])
def process():
  images = []
  url = request.form['url']
  result = requests.get(url)
  data = result.text
  soup = BeautifulSoup(data, 'html.parser')
  og_image = (soup.find('meta', property='og:image') or
                      soup.find('meta', attrs={'name': 'og:image'}))
  if og_image and og_image['content']:
    images.append(og_image['content'])
    print og_image['content']
    
  thumbnail_spec = soup.find('link', rel='image_src')
  if thumbnail_spec and thumbnail_spec['href']:
    images.append(thumbnail_spec['href'])
    print thumbnail_spec['href']
        
  for img in soup.find_all("img", class_="a-dynamic-image"):
    if "sprite" not in img["src"]:
      images.append(img['src'])
      print img['src']
  
  if len(images) > 0:
    return jsonify({'error': 'null', 'data': {'thumbnails': images }, 'message':'success'})
  return jsonify({'error': '1', 'data':'', 'message':'Unable to extract thumbnails'})


if __name__ == '__main__':
    app.run(debug=True)
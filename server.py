import time
import json
from gevent.pywsgi import WSGIServer
from flask import Flask, Response, render_template, stream_with_context
from gevent import monkey
monkey.patch_all()

""" 
Flask server for the web interface
The data is read from lyrics.json and streamed from the server to the client
"""


app = Flask(__name__)

##############################


@app.route("/")
def render_index():
    return render_template("spotify.html")

##############################


@app.route("/listen")
def listen():

    def respond_to_client():
        while True:
            with open("lyrics.json", "r") as f:
                song_info = json.load(f)["data"]
                print(song_info)

                _data = json.dumps(
                    {"title": song_info["title"],
                     "lyrics": song_info["lyrics"],
                     "id": f"https://open.spotify.com/embed/track/{song_info['id']}"
                     })

                yield f"id: 1\ndata: {_data}\nevent: online\n\n"
            time.sleep(0.5)
    return Response(respond_to_client(), mimetype='text/event-stream')


##############################
if __name__ == "__main__":
    # app.run(port=80, debug=True)
    http_server = WSGIServer(("localhost", 80), app)
    http_server.serve_forever()

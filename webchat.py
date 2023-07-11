from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
import time

import GPT
from emotion_analysis import clf_emotion

app = Flask(__name__)
app.config["SECRET_KEY"] = "msc2023sjq"
socketio = SocketIO(app)

bot_name = "Azure"
rooms = {}

def generate_unique_code(Length):
    while True:
        code = ""
        for _ in range(Length):
            code += random.choice(ascii_uppercase)

        if code not in rooms:
            break
    
    return code

@app.route("/", methods = ['POST', 'GET'])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error = "Please enter a name.", code=code, name=name)
        
        if join != False and not code:
            return render_template("home.html", error = "Please enter a room code.", code=code, name=name)
        
        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages":[]}
        elif code not in rooms:
            return render_template("home.html", error = "Room dose not exist.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name

        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code = room, messages = rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return
    
    content = {
        "name":session.get("name"),
        "message":data["data"]
    }
    
    send(content, to=room)
    rooms[room]["messages"].append(content)

    # 收集用户历史数据
    user_history = []
    for msg in rooms[room]["messages"]:
        if msg["name"] == session.get("name"):
            user_history.append(msg["message"])

    # ==============generate responses from GPT with the content=============
    gpt_response= GPT.chat(user_inputs = user_history) 
    # gpt_response= str(user_history) 
    # ==============generate emotion class of current sentense =============
    class_response, _ = clf_emotion(data["data"])
    # 后续可以尝试将分类结果作为prompt信息使用*************************
    # 
    response = '(' + class_response + ')  ' + gpt_response
    # time.sleep(2) # simulate for real chating by waiting 2s
    send({"name":bot_name, "message":response}, to=room) #发送到界面

    bot_content = {
        "name":bot_name,
        "message":response
    }
    rooms[room]["messages"].append(bot_content)

    print("=========================")
    print(rooms[room]["messages"]) #[{'name': 'sss', 'message': 'asdasdasd'}, {'name': 'Azure', 'message': 'Hello! How can I help you today?'}]
    # print(f"{session.get('name')} said: {data['data']}")

@socketio.on('connect')
def connect(auth):
    room = session.get('room')
    name = session.get('name')
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    
    join_room(room)
    send({"name":"System", "message": "{} has entered the room".format(name)}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} has joined the room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get('room')
    name = session.get('name')
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -=1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name":"System", "message": "{} has left the room".format(name)}, to=room)
    print(f"{name} has left room {room}")
    

if __name__ == "__main__":
    socketio.run(app, debug=True)


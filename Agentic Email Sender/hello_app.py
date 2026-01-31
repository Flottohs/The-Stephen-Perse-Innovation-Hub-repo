from flask import Flask, render_template, request
from email_sender import send_email
from text_agent import init_agent, initiate_agent

app = Flask(__name__)

agent = 0
global_count = 0

@app.route('/', methods=["POST", "GET"])
def hello():
    global global_count
    if request.method == "POST":
        input=request.form['getsinput']
        action_result = initiate_agent(agent, input)
        if action_result == True:
            global_count += 1

        return render_template("hello.html", is_sent='Email sent successfully!' if action_result == True else 'Sent failed...', no_emails_sent=global_count)

    return render_template("hello.html", no_emails_sent=global_count)

if __name__ == '__main__':

    agent = init_agent()
    app.run()

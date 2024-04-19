import googleimagescraper
import youtube
import imageai
import weather
import cai


NAME = "HAM-R: "

SECURITY_OPTION = "12345"

Wikipidia = "true"
Wolfarm = "true"
ImageGeneration = "true"
Weather = "true"
_AI = "true"
YTdriver = None

Personality = "Assistant"

def web_main():
    from flask import Flask, render_template, jsonify, request

    app = Flask(__name__, template_folder="interface", static_folder="interface")

    @app.route('/user/setting', methods=['POST'])
    def receive_settings_from_frontend():
        global Wikipidia, Wolfarm, ImageGeneration, Weather, _AI, ai, Personality
        data = request.get_json()
        Wikipidia = data.get("wikipidia")
        Wolfarm = data.get("wolfarm")
        ImageGeneration = data.get('image_generation')
        Weather = data.get('weather')
        _AI = data.get('ai')

        if (Personality != data.get("personality")):
            Personality = data.get("personality")
            cai.set_mode(Personality)            
            return {'msg': "I will be your " +  Personality + " now."}
        return {'msg': ""}

   
    @app.route('/user/message', methods=['POST'])
    def receive_data_from_frontend():
        global Wikipidia, Wolfarm, ImageGeneration, Weather, _AI, ai, Personality, YTdriver
        data_received = request.get_json()
        message = data_received.get('message')

        msg1 = ""
        path = "" 
        msg2 = ""
        ss = "false"
        if YTdriver != None: YTdriver.quit()
        
        if ("show me" in message or "picture of" in message):
            if (ImageGeneration == "true"):
                path = imageai.query(message, "interface/")

                if path != "":
                    msg1 = "Here is the generated image:",
                else:
                    print("COULDN'T GENERATE, COLLECTING FROM GOOGLE")
                    try:
                        path =  "interface/" + googleimagescraper.Download(message, 1, "./interface/")[0]
                    except Exception as e:
                        print(e)
                        msg1 = "Couldn't generate the image at this moment"
            else:
                 msg1 = "Image Generation is turned off"
        
        elif ("weather" in message):
            if (Weather == "true"):
                msg1 = weather.weather()
            else:
                msg1 = "Weather is disabled"

        elif ("sing" in message or "youtube" in message):
            YTdriver = youtube.open(youtube.APIsearch("white tee")[0]['url'], True)
            msg1 = "Singing your song..."
        
        elif ("who is" in message):
            message = message.split('and')[0]
            message = message.replace("who is", "")
            path = ""

            if (ImageGeneration == "true"):
                path = "interface/" + googleimagescraper.Download(message, 1, "./interface/")[0]

            msg1 = "Here is the image of the person:"
            msg2 = cai.message(message)
        
        elif (SECURITY_OPTION in message):
            ss = "true"
            msg1 = "Showing the security option"
        else: 
            if (_AI == "true"):
                msg1 = cai.message(message)
                
            else:
                msg1 = "Sorry, I am disabled for now. Cannot help you out"

        data_to_send = {
            'message': msg1,
            'path': path,
            'ending': msg2,
            'showSetting' : ss
        }

        return jsonify(data_to_send)

    @app.route('/')
    def home():
        return render_template('index.html')

    if __name__ == '__main__':
        app.run(debug=True)

imageai.close()

if __name__ == "__main__":
    web_main()
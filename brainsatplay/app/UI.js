class UI{

    static id = String(Math.floor(Math.random()*1000000))

    constructor(label, session) {

        // Generic Plugin Attributes
        this.label = label
        this.session = session
        this.params = {}

        // UI Identifier
        this.props = {
            id: String(Math.floor(Math.random()*1000000)),
            timestamps: {
                startStream: null,
                stop: null,
                startVideo: null, 
            },
            video: null
        }

        this.connected = true
        this.packagedData = null

        // Port Definition
        this.ports = {
            default: {},
        }
    }

    init = () => {
        // Simply define the HTML template
        let HTMLtemplate = () => {return `
            <div id='${this.props.id}' style='height:100%; width:100%; display: flex; align-items: center; justify-content: center;'>
                <div>
                    <button id="musebutton" class="brainsatplay-default-button">Connect Muse</button>
                    <input type='file' id="${this.props.id}load"></input>
                    <video width="320" height="240" id="${this.props.id}video-container" controls></video>
                    <div id="${this.props.id}myVideo"></div>
                </div>
            </div>`
        }


        let setupHTML = () => {

            let load = document.getElementById(`${this.props.id}load`)
            load.onchange = (res) => {

                this.props.video = load.files[0]
                
                if (this.connected == true) {
              
                    this._handleVideoLoad()

                }

            }
            
            let video = document.getElementById(`${this.props.id}video-container`)

            video.addEventListener('play', (event) => {
                this.props.timestamps.startVideo = Date.now()
                console.log(this.props.timestamps.startVideo); 
              }, { once: true })

            video.onended = (res) => {
                // this.props.timestamps.stop = Date.now()
                // const millis = this.props.timestamps.stop - this.props.timestamps.start

                // console.log(`seconds elapsed = ${Math.floor(millis / 1000)}`);
                this._onVideoStop()
            }
        }

        return {HTMLtemplate, setupHTML}
    }

    default = (input) => {
        return input
    }

    deinit = () => {}

    _handleVideoLoad = () => {

        var video = document.getElementById(`${this.props.id}video-container`);
        console.log(video)
        var fileUrl = window.URL.createObjectURL(this.props.video);

        video.src = fileUrl;

    }

    _onVideoStop = () => {
         // Detect when Video Stops
         this.props.timestamps.stop = Date.now()


         // Grab Data from B@P
         let data = this.session.atlas.data.eeg
         console.log(data)
        //  Object.keys(data).forEach((prop)=> console.log(prop));

         let timestamps = JSON.stringify(this.props.timestamps);

        
         let formData = new FormData();
         formData.append('timestamps', timestamps)
         formData.append('video', this.props.video)
         formData.append('data', JSON.stringify(data))

         this.packagedData = formData

         var element = document.getElementById(this.props.id)
         var btn = document.createElement("BUTTON");  
         btn.type = "button";
         btn.innerHTML = "submit your session";                   
         element.appendChild(btn);  
         
         btn.onclick = (e) => {
            
            e.preventDefault() // does nothing, i'm guessing that the page isn't refreshing because there is now a button of type button
            this._postForm()

            // return false;
        

        }
    }


        
        //  formData.addEventListener("submit", (event) => {
        //     event.preventDefault();
        //   });

    _postForm = () => {

        let url = 'http://127.0.0.1:5000/form-example'
        //  Send to server
        //  fetch(url, {method: 'POST', body: myString, headers: {'Content-Type': 'application/json', "Access-Control-Allow-Origin": "http://127.0.0.1:5000/"} }).then(res => {
         fetch(url, {method: 'POST', body: this.packagedData, headers: {"Access-Control-Allow-Origin": "http://127.0.0.1:5000/"} })
        .then(res => {

            return res.blob();

        })
        .then(blob => {

            let objectURL = URL.createObjectURL(blob);
           
            var c = document.getElementById (`${this.props.id}myVideo`);
            // Create an element <video>
            var v = document.createElement ("video");
            // Set the attributes of the video
            v.src = objectURL;
            v.controls = true;
            // Add the video to <div>
            c.appendChild (v);


        })
        .catch((error) => {

        console.error('Error:', error);
        
        });

        // return false; //preventing form reload

    }

    _deviceConnected = () => {
        let museButton = document.getElementById(`${this.props.id}`).querySelector(`[id="musebutton"]`)
        museButton.style.display = 'none'
        this.connected = true
        this.props.timestamps.startStream = Date.now()
        if (this.props.video !== null) {

            this._handleVideoLoad()

        }

    }
}
export {UI}

// when stream connects, file loads
//if file is not available, file doesn't load

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
            video: null,
            objectURL: null
        }

        this.pages = {
            div1: null,
            div2: null,
            div3: null,
            div4: null
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
                <div id='${this.props.id}div1' style='z-index: 4; position: absolute; transition: opacity 1s;'>
                    <button id="musebutton" class="brainsatplay-default-button">Connect Muse</button>
                    <input type='file' id="${this.props.id}load"></input>
                </div>
                <div id='${this.props.id}div2' style='z-index: 3; position: absolute; opacity: 0; transition: opacity 1s;'>
                    <video width="320" height="240" id="${this.props.id}video-container" controls></video>
                </div>
                <div id='${this.props.id}div3' style='z-index: 2; position: absolute; opacity: 0; transition: opacity 1s;'>
                </div>
                <div id='${this.props.id}div4' style='z-index: 1; position: absolute; opacity: 0; transition: opacity 1s;'>
                    <div id="${this.props.id}myVideo"></div>
                </div>
            </div>`
        }


        let setupHTML = () => {

            this.pages.div1 = document.getElementById(`${this.props.id}div1`)
            this.pages.div2 = document.getElementById(`${this.props.id}div2`)
            this.pages.div3 = document.getElementById(`${this.props.id}div3`)
            this.pages.div4 = document.getElementById(`${this.props.id}div3`)

            let load = document.getElementById(`${this.props.id}load`)
            load.onchange = (res) => {

                this.props.video = load.files[0]
                
                if (this.connected == true) {
                    
                    // let div1 = document.getElementsById(`${this.props.id}div1`)
                    // let div2 = document.getElementById(`${this.props.id}div2`)

                    this._setOpacity(this.pages.div1, this.pages.div2)
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

    _setOpacity = (inp, out) => {
        inp.style.opacity = "0";
        out.style.opacity = "1";
        inp.style.display = 'none';
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

         var btn = document.createElement("BUTTON");  
         btn.type = "button";
         btn.innerHTML = "Download the interesting bits!";                   
         this.pages.div2.appendChild(btn);  
         
         btn.onclick = (e) => {
            
            e.preventDefault() // does nothing, i'm guessing that the page isn't refreshing because there is now a button of type button
            this._postForm()

            // return false;
        

        }
    }

    _download = (url, ref) => {
        const a = document.createElement('a')
        a.href = url
        a.download = url.split('/').pop()
        ref.appendChild(a)
        a.click()
        ref.removeChild(a)
    }

    _createEditLink = (blob, ref) => {
        this.props.objectURL = window.URL.createObjectURL(blob);
           
        // Create an element <video>
        let v = document.createElement ("video");
        // Set the attributes of the video
        v.src = this.props.objectURL;
        v.controls = true;
        v.height = 240;
        v.width = 320;
        // Add the video to <div>
        ref.appendChild (v);
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

            console.log(res.type)
            console.log(res)
            return res.blob();

        })
        .then(blob => {
            
            console.log(blob)

            let c = document.getElementById (`${this.props.id}myVideo`);
            //Create new video element.
            this._createEditLink(blob, c)

            // Create anchor element.
            this._download(this.props.objectURL, c)

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
            
            this._setOpacity(this.pages.div1, this.pages.div2)
            this._handleVideoLoad()

        }

    }
}
export {UI}

// when stream connects, file loads
//if file is not available, file doesn't load

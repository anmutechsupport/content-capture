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
            objectURL: null,
            loader: null,
            loadButton: null
        }

        this.pages = {
            div1: null,
            div2: null,
            div3: null,
            div4: null,
            currdiv: null
        }

        this.connected = false
        this.packagedData = null
        this.packagedVid = null
        this.interestPoints = null

        // Port Definition
        this.ports = {
            default: {},
        }
    }

    init = () => {
        // Simply define the HTML template
        let HTMLtemplate = () => {return `
        <link rel="stylesheet" href="style.css">
            <div id='${this.props.id}' style='height:100%; width:100%; display: flex; align-items: center; justify-content: center;'>
                <div class="pages" id='${this.props.id}div1' style='z-index: 5; position: relative; top: -125px'>
                    <img src="mindframelogo.svg" style="position: relative; top: 115px;">
                    <h1 style="text-align: center; position: relative; top: 15px;"> MindFrames </h1>
                    <div>
                        <p>
                        MindFrame uses your brainwaves to generate montages of 
                        <br>parts that you find interesting in a video! 
                        <br>
                        <br>Mp4 files are currently the only container type that is supported.
                        <br>This application requires a Muse 2 EEG headband.   
                        </p>
                    </div>
                    <div style='display: flex; gap: 20px; position: relative; top: 10px;'>
                        <button style='position: relative; top: -18px;' id="musebutton" class="brainsatplay-default-button">Connect Muse</button>
                        <input type='file' id="${this.props.id}load" accept=".mp4" ></input>
                    </div>
                </div>
                <div class="pages" id='${this.props.id}div2' style='z-index: 4; opacity: 0;'>
                    <h1 style="text-align: left;"> MindFrames </h1>
                    <video id="${this.props.id}video-container" controls></video>
                    <div id='${this.props.id}divchild2' style='display: flex; flex-direction: row; gap: 15px;'>
                        <h3 style='color: blue;' >Watch the video. Make sure not to move around!</h3>
                    </div>
                </div>
                <div class="pages" id='${this.props.id}div3' style='z-index: 3; opacity: 0;'>
                    <div class="spinning" id="${this.props.id}loading"></div>
                    <div>
                        <p> Please hold until the edited video compiles. </p>
                    </div>
                </div>
                <div class="pages" id='${this.props.id}div4' style='z-index: 2; opacity: 0;'>
                    <h1 id='${this.props.id}endesc' style="text-align: left;"> MindFrames </h1>
                </div>
                <div class="pages" id='${this.props.id}div5' style='z-index: 1; opacity: 0;'>
                    <h1> The download failed, please try again. </h1>
                </div>
            </div>`
        }


        let setupHTML = () => {

            this.pages.div1 = document.getElementById(`${this.props.id}div1`)
            this.pages.div2 = document.getElementById(`${this.props.id}div2`)
            this.pages.div3 = document.getElementById(`${this.props.id}div3`)
            this.pages.div4 = document.getElementById(`${this.props.id}div4`)
            this.pages.div5 = document.getElementById(`${this.props.id}div5`)

            this.props.loader = document.getElementById(`${this.props.id}loading`);

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

            video.addEventListener('ended', (event) => {
                this._onVideoStop()
              }, { once: true })

            // video.onended = (res) => {
            //     // this.props.timestamps.stop = Date.now()
            //     // const millis = this.props.timestamps.stop - this.props.timestamps.start

            //     // console.log(`seconds elapsed = ${Math.floor(millis / 1000)}`);
            //     this._onVideoStop()
            // }
        }

        return {HTMLtemplate, setupHTML}
    }

    default = (input) => {
        return input
    }

    deinit = () => {}

    // showing loading
    _displayLoading = (loader) => {
        loader.classList.add("display");
    
    }

    // hiding loading 
    _hideLoading = (loader) => {
        loader.classList.remove("display");
    }


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
        out.style.display = "";
        this.pages.currdiv = out;
    }

    _onVideoStop = () => {
         // Detect when Video Stops
         this.props.timestamps.stop = Date.now()


         // Grab Data from B@P
         let data = this.session.atlas.data.eeg
         console.log(data)
        //  Object.keys(data).forEach((prop)=> console.log(prop));
        
         let formData = new FormData();
         formData.append('timestamps', JSON.stringify(this.props.timestamps))
         formData.append('data', JSON.stringify(data))

         let formData1 = new FormData();
         formData1.append('video', this.props.video)

         this.packagedData = formData
         this.packagedVid = formData1
       

         let divref = document.getElementById(`${this.props.id}divchild2`)
         this.props.loadButton = document.createElement("BUTTON");  
         this.props.loadButton.type = "button";
         this.props.loadButton.innerHTML = "Download the interesting bits!";    
         this.props.loadButton.className = "brainsatplay-default-button";               
         divref.appendChild(this.props.loadButton);  
         
         this.props.loadButton.onclick = (e) => {
            
            e.preventDefault()
            this._setOpacity(this.pages.currdiv, this.pages.div3) // does nothing, i'm guessing that the page isn't refreshing because there is now a button of type button
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

    _createEditVideo = (blob, ref) => {
        this.props.objectURL = window.URL.createObjectURL(blob);
           
        // Create an element <video>
        let v = document.createElement ("video");
        // Set the attributes of the video
        v.src = this.props.objectURL;
        v.controls = true;
        // Add the video to <div>
        ref.appendChild(v);
    }
        
        //  formData.addEventListener("submit", (event) => {
        //     event.preventDefault();
        //   });

    _postForm = () => {

        let urlLabels = 'http://127.0.0.1:5000/labels'
        let urlCompile = 'http://127.0.0.1:5000/compile'
        this._displayLoading(this.props.loader)

         fetch(urlLabels, {method: 'POST', body: this.packagedData, headers: {"Access-Control-Allow-Origin": "http://127.0.0.1:5000/"} })
        .then(response => response.json())
        .then(data => {

            console.log(data)
            this.interestPoints = data
            this.packagedVid.append('labels', JSON.stringify(data))

            return fetch(urlCompile, {method: 'POST', body: this.packagedVid, headers: {"Access-Control-Allow-Origin": "http://127.0.0.1:5000/"} })
        })
        .then(res => {

            console.log(res.type)
            console.log(res)
            return res.blob();

        })
        .then(blob => {
            
            this._hideLoading(this.props.loader)
            console.log(blob)

            // let c = document.getElementById (`${this.props.id}myVideo`);
            //Create new video element.
            this._setOpacity(this.pages.currdiv, this.pages.div4)

            // let endesc = document.getElementById(`${this.props.id}endesc`)
            let interestCount = document.createElement('p')
            let timePoints = []
            this.interestPoints.forEach((value, i) => {
                if (value == 1) timePoints.push(i*20);
            })

            interestCount.append(document.createTextNode(`Your video has compiled. In total, MindFrame found that you were interested ${this.interestPoints.filter(x => x === 1).length} times. 
            \nThese are the time points you found interesting in seconds: ${timePoints}
            \nMindFrame parses together 20 second sequences after the timepoints above.`))
            interestCount.style.textAlign = "left";
            interestCount.style.whiteSpace = "pre";
            interestCount.style.lineHeight = "80%"
            this.pages.div4.appendChild(interestCount)

            this._createEditVideo(blob, this.pages.div4)

            // Create anchor element.
            this._download(this.props.objectURL, this.pages.div4)

        })
        .catch((error) => {

        console.error('Error:', error);

        this._setOpacity(this.pages.currdiv, this.pages.div5)

        this.props.loadButton.innerHTML = "Retry Download"
        this.props.loadButton.style.margin = "auto"
        this.pages.currdiv.appendChild(this.props.loadButton)

        
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

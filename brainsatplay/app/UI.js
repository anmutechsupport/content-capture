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
                start: null,
                stop: null
            },
            video: null
        }

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
                    <video id="${this.props.id}video-container" controls></video>
                </div>
            </div>`
        }


        let setupHTML = () => {
            let load = document.getElementById(`${this.props.id}load`)
            load.onchange = (res) => {

                // console.log(this.props.id) // this is the load element id, it is the same element used in the _handleVideoLoad
                this._handleVideoLoad(load.files[0])
                console.log(this.props.timestamps.start)
            }
            
            let video = document.getElementById(`${this.props.id}video-container`)
            video.onplaying = (res) => {
                this.props.timestamps.start = Date.now()
                console.log(this.props.timestamps.start = Date.now()); 
            }

            video.onended = (res) => {
                this.props.timestamps.stop = Date.now()
                const millis = this.props.timestamps.stop - this.props.timestamps.start

                console.log(`seconds elapsed = ${Math.floor(millis / 1000)}`);
                // this._onVideoStop()
            }
        }

        return {HTMLtemplate, setupHTML}
    }

    default = (input) => {
        return input
    }

    deinit = () => {}

    _handleVideoLoad = (file) => {
        // console.log(this.props.id)
        this.props.timestamps.start = Date.now()
        this.props.video = file
        console.log(this.props.video)


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
 
         let url = ''
         let body = {
             data, 
             timestamps: this.props.timestamps,
             video: this.props.video
         }
 
         // Send to server
         fetch(url, {method: 'POST', body}).then(res => {
 
             // Get Video Back
             console.log(res)
             
             // Display Video
             
         })
    }

    _deviceConnected = () => {
        let museButton = document.getElementById(`${this.props.id}`).querySelector(`[id="musebutton"]`)
        museButton.style.display = 'none'
        this._onVideoStop()
    }
}
export {UI}

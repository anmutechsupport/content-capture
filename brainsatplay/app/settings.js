

import {UI} from './UI.js'

export const settings = {
        name: "Anush Project",
        devices: ["EEG"],
        author: "Anush",
        description: "",
        categories: ["WIP"],
        instructions: "",
        display: {
                "production":false
        },
        graph: {
                "nodes":[
                        {id: 'ui', class: UI, params: {}}
                ],
                "edges":[]
        },
        // editor: {
        //         "parentId":"brainsatplay-studio",
        //         "show":true,
        //         "style":"\n position: block;\n z-index: 9;\n "
        // },
        connect: {
        filter: [
                "Muse 2"
                // , 'OpenBCI Cyton'
                ],
        toggle: 'musebutton',
        autoselect: {device: 'Muse 2'},
        onconnect: () => {
                settings.graph.nodes.find(n => {
                if (n.id === 'ui'){
                        n.instance._deviceConnected()
                }       
        })}
        }
};
### **MindFrames: Summarize Videos Using Your Brain**

# **TLDR. OF SOLUTION.**

***Keep the Memorable Parts, Leave the rest***

Isn't it annoying when you spend hours on hours watching podcasts, but a day after, you can't remember a single thing? Personally, this is the worst feeling in the world, knowing that all those tidbits of wisdom and knowledge you just heard a day ago are now down the drain of your dreaded memory. 

But guess what? We have the technology today to pinpoint when you're interested as you consume content, through a neuroimaging technique called Electroencephalography (EEG).  Using the EEG electrodes from the Muse 2 headset, I created a web app that compiles a summary reel of a video that you watched based on when you were interested. This allows you to save those tidbits of information that you actually found useful. 

# THE PROJECT BREAKDOWN.

[Changing the way we Save Video with our Minds](https://anushmutyala.medium.com/mindframes-changing-the-way-we-save-video-8bc64761f19)

# PROJECT RECREATION.

How to Recreate the Web App on Your Computer Locally.

## Step 1.

```bash
cd pyProcessing 
pip install -r requirements.txt
python flaskv1.py
```

Once you've cloned the repo, you should set up the flask server which handles all signal classification. All the dependencies used can be found and installed through the requirements.txt file. Please ensure that you are using the latest stable version of python. 

## Step 2.

[https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)

To host the application, use the Visual Studio Code Live Server plugin or any other local server hosting plugin in your preferable IDE/visual editor. The brainsatplay/index.html is the page that you want to host using the local server.

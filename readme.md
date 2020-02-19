# PyBot 
This is a Twitterbot. Built to run on Kubernetes and also uses Pure Service Orchestrator for persistent data.

Take a look at the code in ./bots
- autoreply.py - code to reply to mentions
- config.py - sets the API connection
- followFollowers_data.py - Follows anyone that follows you, then writes some of their recent tweets to a CSV on a pure-file FlashBlade filesystem
- followFollowers.py - All the followback with no data collection
- tweet_game_score.py - future
- tweet_game_setup.py - future

## Testing the code on your machine
### Prereqs
- python3
- twitter account with API keys
- Pure Service Orchestrator and working Kubernetes


### Step 1
```
pip install -r requirements.txt
```

### Step 2
Create env variables for each key. The config.py will pull from the local OS. In this case your local machine.
```
export CONSUMER_KEY='some key'
export CONSUMER_SECRET='some secret'
export ACCESS_TOKEN='some token'
export ACCESS_TOKEN_SECRET='some token secret'
```
For the autoreply.py and favretweet.py you need a search key too.
```
export SEARCH_KEY='then thing I search for'
```
**Be careful, if you are testing the favretweet.py program and use a common word for search you will see many many likes and retweets.**

### Step 3
Run the code.
If all is working you will see logs and action on twitter.
```
$ ./autoreply.py 
```
Example:
```
INFO:root:API created
INFO:root:Retrieving mentions
INFO:root:1222564855921758209
INFO:root:1222564855921758209
INFO:root:1222564855921758209
INFO:root:1222564855921758209
INFO:root:1222564855921758209
INFO:root:1222564855921758209
INFO:root:1222564855921758209
INFO:root:1222564855921758209
INFO:root:1222564855921758209
INFO:root:1222564855921758209
INFO:root:1222564855921758209
INFO:root:1222564855921758209
INFO:root:1222564855921758209
INFO:root:1222564855921758209
INFO:root:1222564855921758209
INFO:root:1222564855921758209
INFO:root:Searching for purestorage kubernetes
INFO:root:Retrieving mentions
INFO:root:1222564855921758209
INFO:root:Waiting...
```
It will continue to run so hit control-C to exit.

### Run py-bot in Kubernetes
[Kubernetes and Container Readme](k8sreadme.md)

### More info

[My Blog 2vcps.io](https://blog.2vcps.io)

[Follow me @jon_2vcps](https://twitter.com/jon_2vcps)



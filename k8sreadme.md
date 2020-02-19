# PyBot in a Container
This is a Twitterbot. Built to run on Kubernetes and also uses Pure Service Orchestrator for persistent data.

Take a look at the code in ./bots
- autoreply.py - code to reply to mentions
- config.py - sets the API connection
- followFollowers_data.py - Follows anyone that follows you, then writes some of their recent tweets to a CSV on a pure-file FlashBlade filesystem
- followFollowers.py - All the followback with no data collection
- tweet_game_score.py - future
- tweet_game_setup.py - future

# Py-bot In Kubernetes

### Prereqs
- python3
- twitter account with API keys
- Pure Service Orchestrator and working Kubernetes [How to install Pure Service Orchestator CSI Plugin](https://github.com/purestorage/helm-charts)


### Step 1
Build the docker image and push to your own repo. Make sure you are authenticated to your internal repo. 
```
$ docker build -t yourrepo/you/py-bot:v1 .
$ docker push yourrepo/you/py-bot:v1
```
### Step 2
Create a secret in your k8s environment with the keys are variables. ***Side note: this is the only methond I found to not break the keys when storing in K8s. If you have a functioning way to do it better let me know.***

edit env-secret.yaml with your keys from twitter and the search terms. 
```
kubectl apply -f env-secret.yaml
```
Verify the keys are in your cluster.
```
kuebctl describe secret twitter-api-secret
```

### Step 3
Edit deployment.yaml and deploy the app. In my example I have 3 different deployments and one pvc. If you play to not capture data make sure to change the followback deployment to launch followFollowers.py and not followFollowers_data.py. Addiotionally, remove the PVC information if you are not using it.

Be sure to change the image for each deployemnt to your local repository path.
Notice that the autoreply deployment uses the env variable search_key2 and favretweet deployment will use search_key1. This allows each app to seach on different terms.

**Be careful, if you are testing the favretweet.py program and use a common word for search you will see many many likes and retweets.**

Now deploy
```
kubectl apply -f deployment.yaml

kubectl get pod

NAME                          READY   STATUS    RESTARTS   AGE
autoreply-df85944d5-b9gs9     1/1     Running   0          47h
favretweet-7758fb86c7-56b9q   1/1     Running   0          47h
followback-75bd88dbd8-hqmlr   1/1     Running   0          47h

kubectl logs favretweet-7758fb86c7-56b9q

INFO:root:API created
INFO:root:Processing tweet id 1229439090803847168
INFO:root:Favoriting and RT tweet Day off. No pure service orchestrator today. Close slack Jon, do it now.
INFO:root:Processing tweet id 1229439112966311936
INFO:root:Processing tweet id 1229855750702424066
INFO:root:Favoriting and RT tweet In Pittsburgh. Taking about... Pure Service Orchestrator. No surprise there.  #PSO #PureStorage
INFO:root:Processing tweet id 1229855772789460992
INFO:root:Processing tweet id 1230121679881371648
INFO:root:Favoriting and RT tweet I nearly never repost press releases, but until I can blog on it.  @PureStorage and Pure Service Orchestrator join… https://t.co/A6wxvFUUY7
INFO:root:Processing tweet id 1230121702509531137

kuebctl logs followback-75bd88dbd8-hqmlr

INFO:root:Waiting... 300s
INFO:root:Retrieving and following followers
INFO:root:purelyDB
INFO:root:PreetamZare
INFO:root:josephbreynolds
INFO:root:PureBob
INFO:root:MercerRowe
INFO:root:will_weeams
INFO:root:JeanCarlos237
INFO:root:dataemilyw
INFO:root:8arkz
```

### More info

[My Blog 2vcps.io](https://blog.2vcps.io)

[Follow me @jon_2vcps](https://twitter.com/jon_2vcps)



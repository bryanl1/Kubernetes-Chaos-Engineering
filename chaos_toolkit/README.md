# Chaos Toolkit Demonstration
# Files
- Dockerfile.txt: contains the settings for the kubernetes pods. Denotes app.py and which port to use
- app.py: the main service code you would be running
- Deployment.json: defines the kubernetes service options to deploy
- Experiment.json: the main chaos toolkit definitions, 
- original/ : this folder contains the starting settings for kubernetes
- fix/: an additional kubernetes file to add later

## Prerequisites

1. Install and run Kubernetes with Docker locally. I used minikube : https://minikube.sigs.k8s.io/docs/
The files here should work with just some editing of certain values, for values such as your service IP address and version of the software where needed.

## Steps

1. app.py defines which port your service will run on, I have set 8080
2. Notice the replicas in the Deployment.json that will set the pods to 3
3. Also your apiVersion Deployment.json may need to be adjusted to a more current version
4. Make sure name and service are what you like, like "myservice"
5. Deploy this specification using 'kubectl apply -f original/' which will use the settings in the folder
## Making the experiment
6. Chaos Experiment: ou will need to name it, declare your conditions, declare values to monitor, declare fixes
7. In experiment.json in "title" describe what test this experiment will be running for
8. Also, under description, you can add more detailed information
9. In 'experiment.json' define the "steady state hypothesis" with tolerance 200
10. Set the type to probe 1 and provider type to http
11. Under url set your current kubernetes endpoint of your service
12. Set a  timeout, like 3, so that the system doesn't hang, tells how long to wait
13. (Optionally) In the second probe, set type to python, this tells it to run arbitrary python code
14. Under module and func, set to your python module that you would want to use and the function to call, then any arguments you want to pass in
- the steady state has define a probe where the system is detecing for a HTTP 200 code within 3 seconds and all three are 'Running'
## Adding chaos conditions
15. Use 'pip install chaostoolkit-kubernetes' to install chaos toolkit for kubernetes
16. In experiment.json add a JS array called 'method' after the steady state hypothesis
```Javascript
"steady-state-hypothesis": {
 //...
},
"method": [ {
 "type": "action",
}]
```
17. Then add the name:  "name: "drain_node", and under "provider" you can put "type":"python" to have the block run arbitrary python code
18. Under arguments you mut change the name to the actual name of a node, using "kubectl get nodes"
```Javascript
"arguments": {
 "name": "the name of a current noode in your cluster",
 "delete_pods_with_local_storage": true
 }
```
## Rollback
 Chaos Toolkit allows the addition of rollbacks, which are automatic actionas that your experiement can run to undo experiments after they are done. Uncordon node enables the scheduling of new pods onto a previously drained or cordoned node \
20. You can add another section for this in the experiment by calling it rollbacks, 
```Javascript
"rollbacks": [
 {
    "type": "action",
    "name": "uncordon_node",
    "provider": {
        "type": "python",
        "module": "chaosk8s.node.actions",
        "func": "uncordon_node",
        "arguments": {
            "name": "your node name"
            }
        }
 }
]
```
## Running the experiment
21. Use 'kubectl apply -f ./original' to apply the Kubernetes service with 3 pod instances.
22. Then use 'chaos run experiment.json' to run the whole experiment

## Applying a fix
23. Fixes are opportunities to get creative with Kubernetes features. This example uses a Disruption Budget (https://kubernetes.io/docs/concepts/workloads/pods/disruptions/) Which specifies the minimum number of pods that must be in a ready state at a given moment. 
24. Make a new Kubernetes settings json file called budget.json, or whatever is appropriate
```Javascript
{
	"apiVersion": "your api version",
	"kind": "PodDisruptionBudget",
	"metadata": {
		"name": "my-app-budget"
	},
	"spec": {
		"minAvailable": 3,
		"selector": {
			"matchLabels": {
				"name": "your-app name"
			}
		}
	}
}
```
25. Apply it using 'kubectl apply -f ./fix', this will protect the pods by this Disruption Budget and running chaos run would allow it to pass

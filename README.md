 kubectl create deployment todo-app --image=eplol/todo-app:0.3

 kubectl get logs todo-app

 kubectl port-forward todo-app-659dfcb5f4-l225z 8000:8000
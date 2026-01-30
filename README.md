
k3d cluster create --api-port 6550 -p '9080:80@loadbalancer' -p '9443:443@loadbalancer' --agents 2 --k3s-arg '--disable=traefik@server:*'
istioctl install --set profile=ambient --set values.global.platform=k3d

curl -L https://istio.io/downloadIstio | sh -
cd istio-1.28.3
export PATH=$PWD/bin:$PATH

istioctl install --set profile=ambient --skip-confirmation


kubectl get crd gateways.gateway.networking.k8s.io &> /dev/null || \
kubectl apply --server-side -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.4.0/experimental-install.yaml


kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml
kubectl apply -f samples/bookinfo/platform/kube/bookinfo-versions.yaml
kubectl apply -f samples/bookinfo/gateway-api/bookinfo-gateway.yaml
kubectl annotate gateway bookinfo-gateway networking.istio.io/service-type=ClusterIP --namespace=default


$ kubectl port-forward svc/bookinfo-gateway-istio 8080:80


http://localhost:8080/productpage

kubectl label namespace default istio.io/dataplane-mode=ambient
kubectl apply -f samples/addons/prometheus.yaml
kubectl apply -f samples/addons/kiali.yaml
for i in $(seq 1 100); do curl -sSI -o /dev/null http://localhost:8080/productpage; done

kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: productpage-ztunnel
  namespace: default
spec:
  selector:
    matchLabels:
      app: productpage
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/default/sa/bookinfo-gateway-istio
EOF

kubectl apply -f samples/curl/curl.yaml

kubectl exec deploy/curl -- curl -s "http://productpage:9080/productpage"
istioctl waypoint apply --enroll-namespace --wait
kubectl get gtw waypoint

kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: productpage-waypoint
  namespace: default
spec:
  targetRefs:
  - kind: Service
    group: ""
    name: productpage
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/default/sa/curl
    to:
    - operation:
        methods: ["GET"]
EOF


kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: productpage-ztunnel
  namespace: default
spec:
  selector:
    matchLabels:
      app: productpage
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/default/sa/bookinfo-gateway-istio
        - cluster.local/ns/default/sa/waypoint
EOF



kubectl apply -f - <<EOF
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: reviews
spec:
  parentRefs:
  - group: ""
    kind: Service
    name: reviews
    port: 9080
  rules:
  - backendRefs:
    - name: reviews-v1
      port: 9080
      weight: 90
    - name: reviews-v2
      port: 9080
      weight: 10
EOF


kubectl exec deploy/curl -- sh -c "for i in \$(seq 1 100); do curl -s http://productpage:9080/productpage | grep reviews-v.-; done"


kubectl label namespace default istio.io/use-waypoint-
istioctl waypoint delete --all
kubectl label namespace default istio.io/dataplane-mode-
kubectl delete httproute reviews
kubectl delete authorizationpolicy productpage-viewer
kubectl delete -f samples/curl/curl.yaml
kubectl delete -f samples/bookinfo/platform/kube/bookinfo.yaml
kubectl delete -f samples/bookinfo/platform/kube/bookinfo-versions.yaml
kubectl delete -f samples/bookinfo/gateway-api/bookinfo-gateway.yaml
istioctl uninstall -y --purge
kubectl delete namespace istio-system
kubectl delete -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.4.0/experimental-install.yaml

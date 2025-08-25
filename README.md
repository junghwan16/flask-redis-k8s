### 1분 배포

```bash
# 1. Docker Compose로 로컬 테스트
docker-compose up --build

# 2. Kubernetes 배포 (Minikube 예시)
minikube start
docker build -t counter-app:latest .
minikube image load counter-app:latest
kubectl apply -f k8s/
kubectl port-forward -n counter-app svc/counter-app-service 8080:80

# 3. API 테스트
curl http://localhost:8080/health
```

## 🚢 Kubernetes 배포

### 옵션 1: Minikube (추천 - 로컬 개발)

```bash
# Minikube 설치 및 시작
brew install minikube
minikube start

# 이미지 로드
docker build -t counter-app:latest .
minikube image load counter-app:latest

# 배포
kubectl apply -f k8s/

# 상태 확인
kubectl get all -n counter-app
```

### 옵션 2: K3s

```bash
# K3s 설치
curl -sfL https://get.k3s.io | sh -

# 이미지 import
docker save counter-app:latest | sudo k3s ctr images import -

# 배포
kubectl apply -f k8s/
```

### 배포 확인 및 테스트

```bash
# Pod 상태 확인
kubectl get pods -n counter-app

# 서비스 확인
kubectl get svc -n counter-app

# Port Forward
kubectl port-forward -n counter-app svc/counter-app-service 8080:80

# API 테스트
curl http://localhost:8080/health
curl http://localhost:8080/api/v1/counters/test
curl -X POST -H "Content-Type: application/json" -d '{"amount": 5}' \
  http://localhost:8080/api/v1/counters/test/increment
```

### 스케일링

```bash
# 수동 스케일링
kubectl scale deployment counter-app -n counter-app --replicas=5

# 자동 스케일링 (HPA)
kubectl autoscale deployment counter-app -n counter-app \
  --min=2 --max=10 --cpu-percent=80

# 스케일링 상태 확인
kubectl get hpa -n counter-app
```

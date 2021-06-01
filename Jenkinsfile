
podTemplate(yaml: """
kind: Pod
spec:
  serviceAccountName: jenkins
  containers:
  - name: kustomize
    image: trow.kube-public:31000/kustomize:3.4
    command:
    - cat
    tty: true
    env:
    - name: IMAGE_TAG
      value: ${BUILD_NUMBER}
  - name: kubectl
    image: gcr.io/cloud-builders/kubectl
    command:
    - cat
    tty: true
    env:
    - name: IMAGE_TAG
      value: ${BUILD_NUMBER}
  - name: kaniko
    image: gcr.io/kaniko-project/executor:debug-539ddefcae3fd6b411a95982a830d987f4214251
    imagePullPolicy: Always
    command:
    - /busybox/cat
    tty: true
    env:
    - name: DOCKER_CONFIG
      value: /root/.docker/
    - name: IMAGE_TAG
      value: ${BUILD_NUMBER}
    volumeMounts:
      - name: harbor-config
        mountPath: /root/.docker
  volumes:
    - name: harbor-config
      configMap:
        name: harbor-config
"""
  ) {

  node(POD_LABEL) {
    def myRepo = checkout scm
    def gitCommit = myRepo.GIT_COMMIT
    def gitBranch = myRepo.GIT_BRANCH
    stage('Build with Kaniko') {
      container('kaniko') {
        sh '/kaniko/executor -f `pwd`/Dockerfile -c `pwd` --skip-tls-verify --destination=harbor.sixwords.dev/library/py-bot:latest --destination=harbor.sixwords.dev/library/py-bot:v$BUILD_NUMBER'
      }
    }
    
    stage('Deploy and Kustomize') {
      container('kustomize') {
        sh "kubectl -n ${JOB_NAME} get pod"
        sh "kustomize edit set image harbor.sixwords.dev/library/py-bot:v${BUILD_NUMBER}"
        sh "kustomize build > builddeploy.yaml"
        sh "kubectl get ns ${JOB_NAME} || kubectl create ns ${JOB_NAME}"
        sh "kubectl -n ${JOB_NAME} apply -f builddeploy.yaml"
        sh "kubectl -n ${JOB_NAME} get pod"
      }
    }
    // stage('Deploy with kubectl') {
    //   container('kubectl') {
    //     // sh "kubectl -n ${JOB_NAME} get pod"
    //     // sh "kustomize version"
    //     sh "kubectl get ns ${JOB_NAME} || kubectl create ns ${JOB_NAME}"
    //     sh "kubectl -n ${JOB_NAME} apply -f deployment.yaml"
    //     sh "kubectl -n ${JOB_NAME} get pod"
    //   }
    // }
  }   
}
